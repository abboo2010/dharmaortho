// Fetches live content from the CMS (Supabase, via a public Netlify Function)
// and overlays it onto this statically-built page. If the fetch fails — the
// site is being previewed outside Netlify (e.g. the Artifact preview, which
// has no serverless functions), the CMS hasn't been set up yet, or the
// network is down — the page silently keeps showing whatever build.py baked
// into the HTML, so nothing ever breaks.
//
// main.js (mobile nav, splash, forms, gallery lightbox, etc.) is loaded
// AFTER this finishes either way, so it always binds to the final DOM.
(function () {
  var prefix = window.CMS_PREFIX || '';

  function loadMainScript() {
    var s = document.createElement('script');
    s.src = prefix + 'js/main.js';
    document.body.appendChild(s);
  }

  function text(el, value) {
    if (el && value !== undefined && value !== null && value !== '') el.textContent = value;
  }

  function attr(el, name, value) {
    if (el && value) el.setAttribute(name, value);
  }

  // ---- Hero (home page only) ----
  function applyHero(hero) {
    if (!hero) return;
    text(document.getElementById('hero-eyebrow'), hero.eyebrow);
    text(document.getElementById('hero-heading-line1'), hero.heading_line1);
    text(document.getElementById('hero-heading-em'), hero.heading_em);
    text(document.getElementById('hero-lede'), hero.lede);
    var pri = document.getElementById('hero-cta-primary');
    if (pri) { text(pri, hero.cta_primary_label); attr(pri, 'href', hero.cta_primary_href); }
    var sec = document.getElementById('hero-cta-secondary');
    if (sec) { text(sec, hero.cta_secondary_label); attr(sec, 'href', hero.cta_secondary_href); }
    text(document.getElementById('hero-stat1-value'), hero.stat1_value);
    text(document.getElementById('hero-stat1-label'), hero.stat1_label);
    text(document.getElementById('hero-stat2-value'), hero.stat2_value);
    text(document.getElementById('hero-stat2-label'), hero.stat2_label);
    text(document.getElementById('hero-stat3-value'), hero.stat3_value);
    text(document.getElementById('hero-stat3-label'), hero.stat3_label);
    var img = document.getElementById('hero-image');
    if (img && hero.hero_image_url) img.src = hero.hero_image_url;
  }

  // ---- About (About Dr page + homepage mini-bio) ----
  function applyAbout(about) {
    if (!about) return;
    text(document.getElementById('about-credentials-line'), about.credentials_line);
    text(document.getElementById('about-bio-para1'), about.bio_para1);
    text(document.getElementById('about-bio-para2'), about.bio_para2);
    text(document.getElementById('about-highlight-bold'), about.bio_highlight_bold);
    text(document.getElementById('about-highlight-rest'), about.bio_highlight_rest);
    text(document.getElementById('home-about-para1'), about.home_bio_para1);
    text(document.getElementById('home-about-para2'), about.home_bio_para2);
    var aboutPhoto = document.getElementById('about-photo');
    if (aboutPhoto && about.photo_url) aboutPhoto.src = about.photo_url;
    var homePhoto = document.getElementById('home-about-photo');
    if (homePhoto && about.photo_url) homePhoto.src = about.photo_url;
  }

  // ---- Timeline (About Dr page) ----
  function applyTimeline(items) {
    var wrap = document.getElementById('about-timeline');
    if (!wrap || !items || !items.length) return;
    var sorted = items.slice().sort(function (a, b) { return a.sort_order - b.sort_order; });
    wrap.innerHTML = sorted.map(function (item) {
      return '<div class="timeline-item"><div class="place">' + escapeHtml(item.place) +
        '</div><div>' + escapeHtml(item.description) + '</div></div>';
    }).join('');
  }

  // ---- Contact info (sitewide: header, footer, contact page, booking, CTAs) ----
  function applyContact(contact) {
    if (!contact) return;
    Array.prototype.forEach.call(document.querySelectorAll('[data-cms-href="contact.whatsapp_href"]'), function (a) {
      attr(a, 'href', contact.whatsapp_href);
    });
    Array.prototype.forEach.call(document.querySelectorAll('[data-cms-href="contact.phone_href"]'), function (a) {
      attr(a, 'href', contact.phone_href);
    });
    Array.prototype.forEach.call(document.querySelectorAll('[data-cms-href="contact.email_mailto"]'), function (a) {
      if (contact.email) a.setAttribute('href', 'mailto:' + contact.email);
    });
    Array.prototype.forEach.call(document.querySelectorAll('[data-cms-href="contact.facebook"]'), function (a) {
      attr(a, 'href', contact.facebook);
    });
    Array.prototype.forEach.call(document.querySelectorAll('[data-cms-href="contact.instagram"]'), function (a) {
      attr(a, 'href', contact.instagram);
    });
    Array.prototype.forEach.call(document.querySelectorAll('[data-cms="contact.whatsapp_display"]'), function (s) { text(s, contact.whatsapp_display); });
    Array.prototype.forEach.call(document.querySelectorAll('[data-cms="contact.phone_display"]'), function (s) { text(s, contact.phone_display); });
    Array.prototype.forEach.call(document.querySelectorAll('[data-cms="contact.email"]'), function (s) { text(s, contact.email); });

    if (contact.address_lines && contact.address_lines.length) {
      var addrHtml = contact.address_lines.map(escapeHtml).join('<br>');
      var footerAddr = document.getElementById('footer-address-lines');
      if (footerAddr) footerAddr.innerHTML = addrHtml;
      var contactAddr = document.getElementById('contact-address-lines');
      if (contactAddr) contactAddr.innerHTML = addrHtml;
    }
    if (contact.hours && contact.hours.length) {
      var hoursEl = document.getElementById('contact-hours');
      if (hoursEl) {
        hoursEl.innerHTML = contact.hours.map(function (h) {
          return '<p><b>' + escapeHtml(h.label) + '</b><br>' + escapeHtml(h.value) + '</p>';
        }).join('');
      }
    }
  }

  // ---- Services: home preview grid / services index grid / about grid / nav dropdown / footer list ----
  function serviceHref(basePrefix, slug) { return basePrefix + 'services/' + slug + '.html'; }

  function applyServices(services) {
    if (!services || !services.length) return;
    var sorted = services.slice().sort(function (a, b) { return a.sort_order - b.sort_order; });

    var homeGrid = document.getElementById('home-services-grid');
    if (homeGrid) {
      var onHome = sorted.filter(function (s) { return s.show_on_home; });
      homeGrid.innerHTML = onHome.map(function (s) {
        return '<a href="' + serviceHref(prefix, s.slug) + '" class="card service-card">' +
          '<div class="icon">' + escapeHtml(s.icon) + '</div><h3>' + escapeHtml(s.title) + '</h3>' +
          '<p>' + escapeHtml(s.short) + '</p><span class="learn">Learn More</span></a>';
      }).join('');
    }

    var idxGrid = document.getElementById('services-index-grid');
    if (idxGrid) {
      idxGrid.innerHTML = sorted.map(function (s) {
        return '<a href="' + serviceHref(prefix, s.slug) + '" class="card services-index-card">' +
          '<div class="icon">' + escapeHtml(s.icon) + '</div><div><h3 style="margin-bottom:6px;">' +
          escapeHtml(s.title) + '</h3><p style="margin:0;font-size:.92rem;">' + escapeHtml(s.short) + '</p></div></a>';
      }).join('');
    }

    var aboutGrid = document.getElementById('about-services-grid');
    if (aboutGrid) {
      aboutGrid.innerHTML = sorted.map(function (s) {
        return '<div class="card services-index-card"><div class="icon">' + escapeHtml(s.icon) +
          '</div><div><h3 style="margin-bottom:4px;font-size:1.02rem;">' + escapeHtml(s.title) +
          '</h3><p style="margin:0;font-size:.9rem;">' + escapeHtml(s.short) + '</p></div></div>';
      }).join('');
    }

    var dropdown = document.getElementById('nav-services-dropdown');
    if (dropdown) {
      var navPrefix = dropdown.getAttribute('data-prefix') || prefix;
      var currentSlug = dropdown.getAttribute('data-current-slug') || '';
      dropdown.innerHTML = sorted.map(function (s) {
        var cls = s.slug === currentSlug ? ' class="active"' : '';
        return '<a href="' + serviceHref(navPrefix, s.slug) + '"' + cls + '>' + escapeHtml(s.icon) + ' ' + escapeHtml(s.title) + '</a>';
      }).join('');
    }

    var footerList = document.getElementById('footer-services-list');
    if (footerList) {
      var footerPrefix = footerList.getAttribute('data-prefix') || prefix;
      footerList.innerHTML = sorted.slice(0, 6).map(function (s) {
        return '<li><a href="' + serviceHref(footerPrefix, s.slug) + '">' + escapeHtml(s.title) + '</a></li>';
      }).join('');
    }

    // Service detail page: this page IS one specific service.
    var slug = document.body.getAttribute('data-service-slug');
    if (slug) {
      var svc = sorted.filter(function (s) { return s.slug === slug; })[0];
      if (svc) applyServiceDetail(svc);
    }
  }

  function applyServiceDetail(svc) {
    text(document.getElementById('service-icon'), svc.icon);
    text(document.getElementById('service-title'), svc.title);
    text(document.getElementById('service-breadcrumb-title'), svc.title);
    if (document.title) document.title = svc.title + ' | Dr. Dharmalingam Muthiah';

    var introEl = document.getElementById('service-intro');
    if (introEl && svc.intro && svc.intro.length) {
      introEl.innerHTML = svc.intro.map(function (p) { return '<p>' + escapeHtml(p) + '</p>'; }).join('');
    }
    text(document.getElementById('service-includes-title'), svc.includes_title);
    var includesEl = document.getElementById('service-includes');
    if (includesEl && svc.includes) {
      includesEl.innerHTML = svc.includes.map(function (inc) {
        return '<div class="card include-card"><h3>' + escapeHtml(inc.title) + '</h3><p>' + escapeHtml(inc.desc) + '</p></div>';
      }).join('');
    }
    text(document.getElementById('service-closing-title'), svc.closing_title);
    text(document.getElementById('service-closing-text'), svc.closing_text);
  }

  // ---- Gallery (case grid + lightbox data — must finish before main.js wires up clicks) ----
  function applyGallery(cases) {
    var grid = document.getElementById('gallery-case-grid');
    var dataEl = document.getElementById('gallery-data');
    if (!grid || !cases || !cases.length) return;
    var sorted = cases.slice().sort(function (a, b) { return a.sort_order - b.sort_order; });

    grid.innerHTML = sorted.map(function (c) {
      var images = c.images || [];
      var cover = images[0] || '';
      var count = images.length;
      return '<button class="case-card" type="button" data-case="' + escapeAttr(c.slug) + '" aria-label="View ' + escapeAttr(c.title) + ' photos">' +
        '<div class="case-card-media"><img src="' + escapeAttr(cover) + '" alt="' + escapeAttr(c.title) + '" loading="lazy">' +
        '<span class="case-count">' + count + ' photo' + (count !== 1 ? 's' : '') + '</span></div>' +
        '<div class="case-card-body"><h3>' + escapeHtml(c.title) + '</h3><p>' + escapeHtml(c.description) + '</p></div></button>';
    }).join('');

    if (dataEl) {
      var galleryData = {};
      sorted.forEach(function (c) { galleryData[c.slug] = { title: c.title, images: c.images || [] }; });
      dataEl.textContent = JSON.stringify(galleryData);
    }
  }

  function escapeHtml(str) {
    if (str === undefined || str === null) return '';
    return String(str).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function escapeAttr(str) { return escapeHtml(str); }

  function applyAll(data) {
    try {
      applyHero(data.hero);
      applyAbout(data.about);
      applyTimeline(data.timeline);
      applyContact(data.contact);
      applyServices(data.services); // also handles the current service detail page, if any
      applyGallery(data.gallery);
    } catch (e) {
      // Never let a CMS-overlay bug break the page — static fallback content stays visible.
      if (window.console && console.error) console.error('cms-loader: failed to apply content', e);
    }
  }

  fetch('/.netlify/functions/cms-content')
    .then(function (r) { if (!r.ok) throw new Error('cms-content ' + r.status); return r.json(); })
    .then(applyAll)
    .catch(function () { /* keep whatever build.py baked in — no CMS configured, or offline */ })
    .then(loadMainScript);
})();
