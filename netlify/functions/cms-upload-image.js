// Authenticated image upload for the CMS (hero photo, about photo, gallery photos).
// Expects a JSON POST: { filename, contentType, dataBase64, folder? }
// dataBase64 is the file's raw bytes, base64-encoded (the admin dashboard resizes/
// compresses in the browser first, same pattern used for the other two sites' CMS).
// Uploads to the public "dharmaortho-media" Storage bucket and returns its public URL.
const { getAdminClient, json, requireUser } = require('./_supabase');

const MAX_BYTES = 8 * 1024 * 1024; // 8MB safety cap
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];

function safeName(name) {
  return String(name || 'upload')
    .toLowerCase()
    .replace(/[^a-z0-9.\-]+/g, '-')
    .replace(/-+/g, '-')
    .slice(-120);
}

exports.handler = async function (event) {
  if (event.httpMethod !== 'POST') {
    return json(405, { error: 'Method not allowed' });
  }

  const user = await requireUser(event);
  if (!user) {
    return json(401, { error: 'Not authenticated' });
  }

  let body;
  try {
    body = JSON.parse(event.body || '{}');
  } catch (e) {
    return json(400, { error: 'Invalid JSON body' });
  }

  const { filename, contentType, dataBase64, folder } = body;
  if (!dataBase64 || !contentType) {
    return json(400, { error: 'Missing dataBase64 or contentType' });
  }
  if (ALLOWED_TYPES.indexOf(contentType) === -1) {
    return json(400, { error: 'Unsupported image type: ' + contentType });
  }

  let buffer;
  try {
    buffer = Buffer.from(dataBase64, 'base64');
  } catch (e) {
    return json(400, { error: 'Invalid base64 data' });
  }
  if (buffer.length === 0 || buffer.length > MAX_BYTES) {
    return json(400, { error: 'Image must be between 1 byte and 8MB' });
  }

  const safeFolder = ['hero', 'about', 'gallery'].indexOf(folder) !== -1 ? folder : 'misc';
  const path = `${safeFolder}/${Date.now()}-${safeName(filename)}`;

  try {
    const supabase = getAdminClient();
    const { error: uploadError } = await supabase.storage
      .from('dharmaortho-media')
      .upload(path, buffer, { contentType, upsert: false });
    if (uploadError) throw uploadError;

    const { data: pub } = supabase.storage.from('dharmaortho-media').getPublicUrl(path);
    return json(200, { ok: true, url: pub.publicUrl, path });
  } catch (e) {
    console.error('cms-upload-image error:', e);
    return json(500, { error: e.message || 'Upload failed' });
  }
};
