// Password-gated (well — Supabase-Auth-gated) generic CRUD for every CMS
// collection. Requires a valid Supabase Auth JWT (Authorization: Bearer ...)
// obtained by signing in on admin.html — there is no public sign-up, so any
// successfully-authenticated user is treated as an admin.
//
// Request body (POST, JSON): { collection, op, id?, data?, order? }
//   collection: 'hero' | 'about' | 'contact' | 'timeline' | 'services' | 'gallery' | 'gallery_videos'
//   op:
//     'update'  — singleton: { data }               list: { id, data }
//     'create'  — list only: { data }
//     'delete'  — list only: { id }
//     'reorder' — list only: { order: [id, id, ...] } — sets sort_order = array index
//
// Every collection has an explicit field whitelist below; any key in `data`
// outside that whitelist is silently dropped rather than reaching the DB.
const { getAdminClient, json, requireUser } = require('./_supabase');

const COLLECTIONS = {
  hero: {
    table: 'cms_hero', type: 'singleton', idValue: 1,
    fields: ['eyebrow', 'heading_line1', 'heading_em', 'lede', 'cta_primary_label', 'cta_primary_href',
      'cta_secondary_label', 'cta_secondary_href', 'stat1_value', 'stat1_label', 'stat2_value', 'stat2_label',
      'stat3_value', 'stat3_label', 'hero_image_url'],
  },
  about: {
    table: 'cms_about', type: 'singleton', idValue: 1,
    fields: ['credentials_line', 'bio_para1', 'bio_para2', 'bio_highlight_bold', 'bio_highlight_rest',
      'home_bio_para1', 'home_bio_para2', 'photo_url'],
  },
  contact: {
    table: 'cms_contact', type: 'singleton', idValue: 1,
    fields: ['address_lines', 'whatsapp_display', 'whatsapp_href', 'phone_display', 'phone_href', 'email',
      'facebook', 'instagram', 'hours'],
  },
  timeline: {
    table: 'cms_timeline_items', type: 'list', idField: 'id', autoId: true,
    fields: ['place', 'description', 'sort_order'],
  },
  services: {
    table: 'cms_services', type: 'list', idField: 'slug', autoId: false,
    fields: ['slug', 'icon', 'title', 'short', 'intro', 'includes_title', 'includes', 'closing_title',
      'closing_text', 'show_on_home', 'sort_order'],
  },
  gallery: {
    table: 'cms_gallery_cases', type: 'list', idField: 'slug', autoId: false,
    fields: ['slug', 'title', 'description', 'images', 'sort_order'],
  },
  gallery_videos: {
    table: 'cms_gallery_videos', type: 'list', idField: 'id', autoId: true,
    // source: 'youtube' | 'upload'. For 'youtube', youtube_id is the 11-char video id
    // (extracted client-side from the pasted URL); for 'upload', video_url is the
    // public Supabase Storage URL from cms-video-upload-url.js. thumbnail_url is
    // optional in both cases — YouTube videos default to their own thumbnail.
    fields: ['source', 'youtube_id', 'video_url', 'thumbnail_url', 'title', 'sort_order'],
  },
};

function pickWhitelisted(data, fields) {
  const out = {};
  if (!data) return out;
  fields.forEach((f) => {
    if (Object.prototype.hasOwnProperty.call(data, f)) out[f] = data[f];
  });
  return out;
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

  const { collection, op, id, data, order } = body;
  const cfg = COLLECTIONS[collection];
  if (!cfg) return json(400, { error: 'Unknown collection: ' + collection });

  const supabase = getAdminClient();

  try {
    if (cfg.type === 'singleton') {
      if (op !== 'update') return json(400, { error: 'Singletons only support "update"' });
      const clean = pickWhitelisted(data, cfg.fields);
      const { data: row, error } = await supabase
        .from(cfg.table)
        .update(clean)
        .eq('id', cfg.idValue)
        .select()
        .maybeSingle();
      if (error) throw error;
      return json(200, { ok: true, row });
    }

    // list-type collection
    if (op === 'create') {
      const clean = pickWhitelisted(data, cfg.fields);
      const { data: row, error } = await supabase.from(cfg.table).insert(clean).select().maybeSingle();
      if (error) throw error;
      return json(200, { ok: true, row });
    }

    if (op === 'update') {
      if (id === undefined || id === null) return json(400, { error: 'Missing id' });
      const clean = pickWhitelisted(data, cfg.fields);
      delete clean[cfg.idField]; // never allow renaming the primary key via update
      const { data: row, error } = await supabase
        .from(cfg.table)
        .update(clean)
        .eq(cfg.idField, id)
        .select()
        .maybeSingle();
      if (error) throw error;
      return json(200, { ok: true, row });
    }

    if (op === 'delete') {
      if (id === undefined || id === null) return json(400, { error: 'Missing id' });
      const { error } = await supabase.from(cfg.table).delete().eq(cfg.idField, id);
      if (error) throw error;
      return json(200, { ok: true });
    }

    if (op === 'reorder') {
      if (!Array.isArray(order)) return json(400, { error: 'Missing order array' });
      // Sequential, not parallel — smaller tables, and avoids surprising interleaving
      // if two reorders somehow race.
      for (let i = 0; i < order.length; i++) {
        const { error } = await supabase.from(cfg.table).update({ sort_order: i }).eq(cfg.idField, order[i]);
        if (error) throw error;
      }
      return json(200, { ok: true });
    }

    return json(400, { error: 'Unknown op: ' + op });
  } catch (e) {
    console.error('cms-crud error:', e);
    return json(500, { error: e.message || 'Server error' });
  }
};
