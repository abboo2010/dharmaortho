// Public endpoint: GET /.netlify/functions/cms-content
// Returns every piece of CMS content in one combined payload for the live
// site's assets/cms-loader.js to overlay onto the statically-built pages.
// No auth required — this is the same information the built pages already
// show, just fetched live instead of baked in at the last `python3 build.py`.
const { getAdminClient, json } = require('./_supabase');

exports.handler = async function (event) {
  if (event.httpMethod !== 'GET') {
    return json(405, { error: 'Method not allowed' });
  }

  try {
    const supabase = getAdminClient();

    const [hero, about, contact, timeline, services, gallery] = await Promise.all([
      supabase.from('cms_hero').select('*').eq('id', 1).maybeSingle(),
      supabase.from('cms_about').select('*').eq('id', 1).maybeSingle(),
      supabase.from('cms_contact').select('*').eq('id', 1).maybeSingle(),
      supabase.from('cms_timeline_items').select('*').order('sort_order', { ascending: true }),
      supabase.from('cms_services').select('*').order('sort_order', { ascending: true }),
      supabase.from('cms_gallery_cases').select('*').order('sort_order', { ascending: true }),
    ]);

    const firstError = [hero, about, contact, timeline, services, gallery].find((r) => r.error);
    if (firstError) {
      console.error('cms-content query error:', firstError.error);
      return json(500, { error: 'Failed to load content' });
    }

    return json(200, {
      hero: hero.data || null,
      about: about.data || null,
      contact: contact.data || null,
      timeline: timeline.data || [],
      services: services.data || [],
      gallery: gallery.data || [],
    });
  } catch (e) {
    console.error('cms-content error:', e);
    return json(500, { error: e.message || 'Server error' });
  }
};
