// Minimal service worker.
//
// This file exists ONLY so Chrome/Android will recognize the site as a
// properly installable app (Chrome requires a registered service worker
// with a fetch handler before it offers "Install app" instead of the more
// limited "Add shortcut"). It deliberately does NOT cache anything -- every
// request is simply passed straight through to the network unchanged.
//
// This is intentional: the site's CMS-driven content (hero text, gallery,
// videos, admin dashboard, etc.) is loaded live via fetch calls to Netlify
// Functions and Supabase, and a caching service worker could easily end up
// serving stale/old content or an out-of-date admin dashboard, which is
// exactly the kind of "why isn't my change showing up" problem this project
// has already run into with plain browser caching. Keeping this worker a
// pure passthrough avoids introducing that risk entirely.
self.addEventListener('fetch', function (event) {
  event.respondWith(fetch(event.request));
});
