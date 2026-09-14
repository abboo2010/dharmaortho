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

    const [hero, about, contact, timeline, services, gallery, galleryVideos, homeExtra] = await Promise.all([
      supabase.from('cms_hero').select('*').eq('id', 1).maybeSingle(),
      supabase.from('cms_about').select('*').eq('id', 1).maybeSingle(),
      supabase.from('cms_contact').select('*').eq('id', 1).maybeSingle(),
      supabase.from('cms_timeline_items').select('*').order('sort_order', { ascending: true }),
      supabase.from('cms_services').select('*').order('sort_order', { ascending: true }),
      supabase.from('cms_gallery_cases').select('*').order('sort_order', { ascending: true }),
      supabase.from('cms_gallery_videos').select('*').order('sort_order', { ascending: true }),
      supabase.from('cms_home_extra').select('*').eq('id', 1).maybeSingle(),
    ]);

    const firstError = [hero, about, contact, timeline, services, gallery].find((r) => r.error);
    if (firstError) {
      console.error('cms-content query error:', firstError.error);
      return json(500, { error: 'Failed to load content' });
    }
    // gallery_videos and home_extra are checked separately and degrade to an empty
    // result rather than failing the whole response — both tables are newer than the
    // rest of the schema, so a site that hasn't run their migration yet just falls
    // back to whatever the static build.py output shows, instead of breaking the CMS.
    if (galleryVideos.error) {
      console.error('cms-content gallery_videos query error (table missing/migration not run?):', galleryVideos.error);
    }
    if (homeExtra.error) {
      console.error('cms-content home_extra query error (table missing/migration not run?):', homeExtra.error);
    }

    return json(200, {
      hero: hero.data || null,
      about: about.data || null,
      contact: contact.data || null,
      timeline: timeline.data || [],
      services: services.data || [],
      gallery: gallery.data || [],
      gallery_videos: galleryVideos.error ? [] : (galleryVideos.data || []),
      home_extra: homeExtra.error ? null : (homeExtra.data || null),
    });
  } catch (e) {
    console.error('cms-content error:', e);
    return json(500, { error: e.message || 'Server error' });
  }
};
