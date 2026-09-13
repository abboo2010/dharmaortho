// Authenticated video-upload preparation for the CMS Gallery Videos tab.
//
// Video files are typically far larger than the 8MB cap used for images in
// cms-upload-image.js, and routing a big file's bytes through a Netlify
// Function as a base64 JSON body would run into that function's own request
// size limits. So this function does NOT touch the video's bytes at all —
// it just asks Supabase Storage for a short-lived SIGNED UPLOAD URL for one
// specific path, and returns that to the browser. The browser then uploads
// the actual file straight to Supabase Storage (see assets/admin.js's
// uploadVideo(), which calls supabase-js's storage.uploadToSignedUrl()) —
// the file never passes through this function or any Netlify server.
//
// Expects a JSON POST: { filename, contentType }
// Returns: { path, token, signedUrl, publicUrl }
//
// Note: Supabase projects have a project-wide max upload file size (Project
// Settings -> Storage -> "Global file size limit", commonly 50MB by default
// on the free tier). A signed upload URL is still bound by that limit, so a
// very large video file needs the limit raised in the Supabase dashboard
// first, or the upload will fail with a "file too large" error from Storage
// itself (not from this function).
const { getAdminClient, json, requireUser } = require('./_supabase');

const ALLOWED_TYPES = ['video/mp4', 'video/webm', 'video/quicktime', 'video/ogg', 'video/x-m4v'];

function safeName(name) {
  return String(name || 'video')
    .toLowerCase()
    .replace(/[^a-z0-9.\-]+/g, '-')
    .replace(/-+/g, '-')
    .slice(-140);
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

  const { filename, contentType } = body;
  if (!contentType || ALLOWED_TYPES.indexOf(contentType) === -1) {
    return json(400, { error: 'Unsupported video type: ' + contentType + '. Use MP4, WebM, MOV or OGG.' });
  }

  const path = `videos/${Date.now()}-${safeName(filename)}`;

  try {
    const supabase = getAdminClient();
    const { data, error } = await supabase.storage.from('dharmaortho-media').createSignedUploadUrl(path);
    if (error) throw error;

    const { data: pub } = supabase.storage.from('dharmaortho-media').getPublicUrl(path);
    return json(200, { ok: true, path: data.path, token: data.token, signedUrl: data.signedUrl, publicUrl: pub.publicUrl });
  } catch (e) {
    console.error('cms-video-upload-url error:', e);
    return json(500, { error: e.message || 'Could not prepare upload' });
  }
};
