(function () {
  'use strict';

  var cfg = window.CMS_CONFIG || {};
  var sb = window.supabase.createClient(cfg.SUPABASE_URL, cfg.SUPABASE_ANON_KEY);

  var loginScreen = document.getElementById('login-screen');
  var appScreen = document.getElementById('app-screen');
  var loginForm = document.getElementById('login-form');
  var loginError = document.getElementById('login-error');
  var loginBtn = document.getElementById('login-btn');
  var userEmailEl = document.getElementById('user-email');
  var logoutBtn = document.getElementById('logout-btn');
  var sidebar = document.getElementById('sidebar');
  var mainEl = document.getElementById('main');

  var CONTENT = null;     // last-fetched combined content (see cms-content.js)
  var activeTab = 'hero';

  // ---------------------------------------------------------------------
  // Auth
  // ---------------------------------------------------------------------

  function showLogin() {
    appScreen.style.display = 'none';
    loginScreen.style.display = 'flex';
  }

  function showApp(user) {
    loginScreen.style.display = 'none';
    appScreen.style.display = 'block';
    userEmailEl.textContent = (user && user.email) || '';
    loadContentAndRender();
  }

  sb.auth.getSession().then(function (res) {
    var session = res.data && res.data.session;
    if (session) showApp(session.user);
    else showLogin();
  });

  loginForm.addEventListener('submit', function (e) {
    e.preventDefault();
    loginError.textContent = '';
    loginBtn.disabled = true;
    loginBtn.textContent = 'Signing in…';
    var email = document.getElementById('login-email').value.trim();
    var password = document.getElementById('login-password').value;
    sb.auth.signInWithPassword({ email: email, password: password }).then(function (res) {
      loginBtn.disabled = false;
      loginBtn.textContent = 'Sign In';
      if (res.error) {
        loginError.textContent = res.error.message || 'Sign in failed.';
        return;
      }
      showApp(res.data.user);
    });
  });

  logoutBtn.addEventListener('click', function () {
    sb.auth.signOut().then(showLogin);
  });

  // ---------------------------------------------------------------------
  // API helpers
  // ---------------------------------------------------------------------

  function authHeader() {
    return sb.auth.getSession().then(function (res) {
      var token = res.data && res.data.session && res.data.session.access_token;
      return token ? { Authorization: 'Bearer ' + token } : {};
    });
  }

  function fetchContent() {
    return fetch('/.netlify/functions/cms-content').then(function (r) {
      if (!r.ok) throw new Error('Failed to load content (' + r.status + ')');
      return r.json();
    });
  }

  function crud(collection, op, extra) {
    var body = Object.assign({ collection: collection, op: op }, extra || {});
    return authHeader().then(function (headers) {
      return fetch('/.netlify/functions/cms-crud', {
        method: 'POST',
        headers: Object.assign({ 'Content-Type': 'application/json' }, headers),
        body: JSON.stringify(body),
      }).then(function (r) {
        return r.json().then(function (json) {
          if (!r.ok) throw new Error(json.error || 'Request failed (' + r.status + ')');
          return json;
        });
      });
    });
  }

  function uploadImage(file, folder) {
    return resizeImage(file, 1600, 0.85).then(function (result) {
      return authHeader().then(function (headers) {
        return fetch('/.netlify/functions/cms-upload-image', {
          method: 'POST',
          headers: Object.assign({ 'Content-Type': 'application/json' }, headers),
          body: JSON.stringify({
            filename: file.name,
            contentType: result.contentType,
            dataBase64: result.base64,
            folder: folder,
          }),
        }).then(function (r) {
          return r.json().then(function (json) {
            if (!r.ok) throw new Error(json.error || 'Upload failed');
            return json;
          });
        });
      });
    });
  }

  // Downscales + re-encodes an image file client-side before it ever reaches
  // the network, so a phone photo doesn't blow past the upload function's cap.
  function resizeImage(file, maxDim, quality) {
    return new Promise(function (resolve, reject) {
      var img = new Image();
      var url = URL.createObjectURL(file);
      img.onload = function () {
        var scale = Math.min(1, maxDim / Math.max(img.width, img.height));
        var w = Math.round(img.width * scale);
        var h = Math.round(img.height * scale);
        var canvas = document.createElement('canvas');
        canvas.width = w;
        canvas.height = h;
        canvas.getContext('2d').drawImage(img, 0, 0, w, h);
        var contentType = file.type === 'image/png' ? 'image/png' : 'image/jpeg';
        var dataUrl = canvas.toDataURL(contentType, quality);
        URL.revokeObjectURL(url);
        resolve({ base64: dataUrl.split(',')[1], contentType: contentType });
      };
      img.onerror = function () {
        URL.revokeObjectURL(url);
        reject(new Error('Could not read image file'));
      };
      img.src = url;
    });
  }

  // ---------------------------------------------------------------------
  // Small DOM helpers
  // ---------------------------------------------------------------------

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === 'text') node.textContent = attrs[k];
      else if (k === 'html') node.innerHTML = attrs[k];
      else if (k.indexOf('on') === 0 && typeof attrs[k] === 'function') node.addEventListener(k.slice(2), attrs[k]);
      else node.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) { if (c) node.appendChild(c); });
    return node;
  }

  function field(labelText, inputEl) {
    return el('div', { class: 'field' }, [el('label', { text: labelText }), inputEl]);
  }

  function textInput(value) {
    var i = el('input', { type: 'text' });
    i.value = value || '';
    return i;
  }

  function textArea(value, rows) {
    var t = el('textarea', { rows: rows || 3 });
    t.value = value || '';
    return t;
  }

  function statusMsg(container, text, isError) {
    var s = container.querySelector('.save-status');
    if (!s) return;
    s.textContent = text;
    s.className = 'save-status' + (isError ? ' error' : '');
    if (!isError) setTimeout(function () { if (s.textContent === text) s.textContent = ''; }, 2500);
  }

  // ---------------------------------------------------------------------
  // Tab: Hero (singleton)
  // ---------------------------------------------------------------------

  function renderHero() {
    var h = CONTENT.hero || {};
    mainEl.innerHTML = '';
    mainEl.appendChild(el('h2', { text: 'Home Hero' }));
    mainEl.appendChild(el('p', { class: 'hint', text: 'The big banner at the very top of the homepage.' }));

    var card = el('div', { class: 'card' });
    var eyebrow = textInput(h.eyebrow);
    var line1 = textInput(h.heading_line1);
    var em = textInput(h.heading_em);
    var lede = textArea(h.lede, 4);
    var ctaPL = textInput(h.cta_primary_label), ctaPH = textInput(h.cta_primary_href);
    var ctaSL = textInput(h.cta_secondary_label), ctaSH = textInput(h.cta_secondary_href);
    var s1v = textInput(h.stat1_value), s1l = textInput(h.stat1_label);
    var s2v = textInput(h.stat2_value), s2l = textInput(h.stat2_label);
    var s3v = textInput(h.stat3_value), s3l = textInput(h.stat3_label);
    var imgUrl = textInput(h.hero_image_url);
    var imgPreview = el('img', { src: h.hero_image_url || '', style: 'max-width:220px;border-radius:8px;display:block;margin:8px 0;' });
    var imgFile = el('input', { type: 'file', accept: 'image/*' });

    card.appendChild(el('h3', { text: 'Heading' }));
    card.appendChild(el('div', { class: 'row' }, [field('Eyebrow (small label above heading)', eyebrow)]));
    card.appendChild(el('div', { class: 'row' }, [field('Heading — line 1', line1), field('Heading — emphasised part', em)]));
    card.appendChild(field('Description', lede));

    card.appendChild(el('h3', { text: 'Buttons', style: 'margin-top:22px;' }));
    card.appendChild(el('div', { class: 'row' }, [field('Primary button label', ctaPL), field('Primary button link', ctaPH)]));
    card.appendChild(el('div', { class: 'row' }, [field('Secondary button label', ctaSL), field('Secondary button link', ctaSH)]));

    card.appendChild(el('h3', { text: 'Stats row', style: 'margin-top:22px;' }));
    card.appendChild(el('div', { class: 'row' }, [field('Stat 1 value', s1v), field('Stat 1 label', s1l)]));
    card.appendChild(el('div', { class: 'row' }, [field('Stat 2 value', s2v), field('Stat 2 label', s2l)]));
    card.appendChild(el('div', { class: 'row' }, [field('Stat 3 value', s3v), field('Stat 3 label', s3l)]));

    card.appendChild(el('h3', { text: 'Hero photo', style: 'margin-top:22px;' }));
    card.appendChild(imgPreview);
    card.appendChild(field('Image URL', imgUrl));
    card.appendChild(field('Or upload a new photo', imgFile));

    imgFile.addEventListener('change', function () {
      if (!imgFile.files[0]) return;
      statusMsg(card, 'Uploading…');
      uploadImage(imgFile.files[0], 'hero').then(function (res) {
        imgUrl.value = res.url;
        imgPreview.src = res.url;
        statusMsg(card, 'Photo uploaded — remember to Save.');
      }).catch(function (e) { statusMsg(card, e.message, true); });
    });

    var saveBar = el('div', { class: 'save-bar' }, [
      el('button', { class: 'btn btn-primary', text: 'Save Changes', onclick: function () {
        crud('hero', 'update', {
          data: {
            eyebrow: eyebrow.value, heading_line1: line1.value, heading_em: em.value, lede: lede.value,
            cta_primary_label: ctaPL.value, cta_primary_href: ctaPH.value,
            cta_secondary_label: ctaSL.value, cta_secondary_href: ctaSH.value,
            stat1_value: s1v.value, stat1_label: s1l.value,
            stat2_value: s2v.value, stat2_label: s2l.value,
            stat3_value: s3v.value, stat3_label: s3l.value,
            hero_image_url: imgUrl.value,
          },
        }).then(function (res) { CONTENT.hero = res.row; statusMsg(card, 'Saved.'); })
          .catch(function (e) { statusMsg(card, e.message, true); });
      } }),
      el('span', { class: 'save-status' }),
    ]);
    card.appendChild(saveBar);
    mainEl.appendChild(card);
  }

  // ---------------------------------------------------------------------
  // Tab: About (singleton)
  // ---------------------------------------------------------------------

  function renderAbout() {
    var a = CONTENT.about || {};
    mainEl.innerHTML = '';
    mainEl.appendChild(el('h2', { text: 'About Dr' }));
    mainEl.appendChild(el('p', { class: 'hint', text: 'The doctor’s bio, shown on the About Dr page and (a shorter version) on the homepage.' }));

    var card = el('div', { class: 'card' });
    var credLine = textInput(a.credentials_line);
    var p1 = textArea(a.bio_para1, 3), p2 = textArea(a.bio_para2, 3);
    var hlBold = textInput(a.bio_highlight_bold), hlRest = textArea(a.bio_highlight_rest, 2);
    var homeP1 = textArea(a.home_bio_para1, 3), homeP2 = textArea(a.home_bio_para2, 3);
    var photoUrl = textInput(a.photo_url);
    var photoPreview = el('img', { src: a.photo_url || '', style: 'max-width:220px;border-radius:8px;display:block;margin:8px 0;' });
    var photoFile = el('input', { type: 'file', accept: 'image/*' });

    card.appendChild(el('h3', { text: 'About Dr page' }));
    card.appendChild(field('Credentials line (under the page heading)', credLine));
    card.appendChild(field('Bio — paragraph 1', p1));
    card.appendChild(field('Bio — paragraph 2', p2));
    card.appendChild(el('div', { class: 'row' }, [field('Highlight — bold lead-in', hlBold), field('Highlight — rest of sentence', hlRest)]));

    card.appendChild(el('h3', { text: 'Homepage mini-bio', style: 'margin-top:22px;' }));
    card.appendChild(field('Paragraph 1', homeP1));
    card.appendChild(field('Paragraph 2', homeP2));

    card.appendChild(el('h3', { text: 'Photo (shared by both)', style: 'margin-top:22px;' }));
    card.appendChild(photoPreview);
    card.appendChild(field('Image URL', photoUrl));
    card.appendChild(field('Or upload a new photo', photoFile));

    photoFile.addEventListener('change', function () {
      if (!photoFile.files[0]) return;
      statusMsg(card, 'Uploading…');
      uploadImage(photoFile.files[0], 'about').then(function (res) {
        photoUrl.value = res.url;
        photoPreview.src = res.url;
        statusMsg(card, 'Photo uploaded — remember to Save.');
      }).catch(function (e) { statusMsg(card, e.message, true); });
    });

    var saveBar = el('div', { class: 'save-bar' }, [
      el('button', { class: 'btn btn-primary', text: 'Save Changes', onclick: function () {
        crud('about', 'update', {
          data: {
            credentials_line: credLine.value, bio_para1: p1.value, bio_para2: p2.value,
            bio_highlight_bold: hlBold.value, bio_highlight_rest: hlRest.value,
            home_bio_para1: homeP1.value, home_bio_para2: homeP2.value, photo_url: photoUrl.value,
          },
        }).then(function (res) { CONTENT.about = res.row; statusMsg(card, 'Saved.'); })
          .catch(function (e) { statusMsg(card, e.message, true); });
      } }),
      el('span', { class: 'save-status' }),
    ]);
    card.appendChild(saveBar);
    mainEl.appendChild(card);
  }

  // ---------------------------------------------------------------------
  // Tab: Timeline (list — About Dr page's Education/Fellowships/Special Interests)
  // ---------------------------------------------------------------------

  function renderTimeline() {
    var items = (CONTENT.timeline || []).slice().sort(function (a, b) { return a.sort_order - b.sort_order; });
    mainEl.innerHTML = '';
    mainEl.appendChild(el('h2', { text: 'Timeline' }));
    mainEl.appendChild(el('p', { class: 'hint', text: 'The "Education, Fellowships & Special Interests" list on the About Dr page.' }));

    var listWrap = el('div', {});
    if (!items.length) listWrap.appendChild(el('p', { class: 'empty-note', text: 'No entries yet.' }));

    items.forEach(function (item, idx) {
      var placeInput = textInput(item.place);
      var descInput = textArea(item.description, 2);
      var itemCard = el('div', { class: 'list-item' });
      itemCard.appendChild(el('div', { class: 'list-item-head' }, [
        el('span', { class: 'title', text: item.place || '(untitled)' }),
        el('div', { class: 'list-item-actions' }, [
          el('button', { class: 'btn btn-outline btn-sm', text: '↑', onclick: function () { moveItem('timeline', items, idx, -1); } }),
          el('button', { class: 'btn btn-outline btn-sm', text: '↓', onclick: function () { moveItem('timeline', items, idx, 1); } }),
          el('button', { class: 'btn btn-danger btn-sm', text: 'Delete', onclick: function () {
            if (!confirm('Delete this timeline entry?')) return;
            crud('timeline', 'delete', { id: item.id }).then(loadContentAndRender);
          } }),
        ]),
      ]));
      itemCard.appendChild(field('Place / Title', placeInput));
      itemCard.appendChild(field('Description', descInput));
      itemCard.appendChild(el('div', { class: 'save-bar' }, [
        el('button', { class: 'btn btn-primary btn-sm', text: 'Save', onclick: function () {
          crud('timeline', 'update', { id: item.id, data: { place: placeInput.value, description: descInput.value } })
            .then(function () { statusMsg(itemCard, 'Saved.'); loadContentAndRender(); })
            .catch(function (e) { statusMsg(itemCard, e.message, true); });
        } }),
        el('span', { class: 'save-status' }),
      ]));
      listWrap.appendChild(itemCard);
    });

    mainEl.appendChild(listWrap);
    mainEl.appendChild(el('button', { class: 'btn btn-gold', text: '+ Add Entry', onclick: function () {
      crud('timeline', 'create', { data: { place: 'New Entry', description: '', sort_order: items.length } }).then(loadContentAndRender);
    } }));
  }

  function moveItem(collection, items, idx, dir) {
    var newIdx = idx + dir;
    if (newIdx < 0 || newIdx >= items.length) return;
    var ids = items.map(function (it) { return it.id !== undefined ? it.id : it.slug; });
    var tmp = ids[idx]; ids[idx] = ids[newIdx]; ids[newIdx] = tmp;
    crud(collection, 'reorder', { order: ids }).then(loadContentAndRender);
  }

  // ---------------------------------------------------------------------
  // Tab: Services (list, keyed by slug)
  // ---------------------------------------------------------------------

  function renderServices() {
    var items = (CONTENT.services || []).slice().sort(function (a, b) { return a.sort_order - b.sort_order; });
    mainEl.innerHTML = '';
    mainEl.appendChild(el('h2', { text: 'Services' }));
    mainEl.appendChild(el('p', { class: 'hint', text: '13 areas of practice — each has its own page. "Show on homepage" controls the 9 preview cards on the homepage.' }));

    items.forEach(function (svc, idx) {
      var expanded = false;
      var head = el('div', { class: 'list-item-head' }, [
        el('span', { class: 'title', text: (svc.icon || '') + '  ' + (svc.title || '(untitled)') }),
        el('div', { class: 'list-item-actions' }, [
          el('button', { class: 'btn btn-outline btn-sm', text: '↑', onclick: function () { moveItem('services', items, idx, -1); } }),
          el('button', { class: 'btn btn-outline btn-sm', text: '↓', onclick: function () { moveItem('services', items, idx, 1); } }),
          el('button', { class: 'btn btn-outline btn-sm', text: 'Edit', onclick: function () { toggleBody(); } }),
          el('button', { class: 'btn btn-danger btn-sm', text: 'Delete', onclick: function () {
            if (!confirm('Delete "' + svc.title + '"? This removes its page content from the CMS.')) return;
            crud('services', 'delete', { id: svc.slug }).then(loadContentAndRender);
          } }),
        ]),
      ]);
      var itemCard = el('div', { class: 'list-item' }, [head]);
      var body = el('div', { hidden: true });

      function toggleBody() { body.hidden = !body.hidden; body.querySelector && buildBody(); }

      function buildBody() {
        if (body.dataset.built) return;
        body.dataset.built = '1';

        var icon = textInput(svc.icon), title = textInput(svc.title), short = textArea(svc.short, 2);
        var showHome = el('input', { type: 'checkbox' }); showHome.checked = !!svc.show_on_home;

        body.appendChild(el('div', { class: 'row' }, [field('Icon (emoji)', icon), field('Title', title)]));
        body.appendChild(field('Short description (used on preview cards)', short));
        body.appendChild(el('label', { class: 'checkbox-row' }, [showHome, document.createTextNode('Show on homepage preview grid')]));

        body.appendChild(el('h3', { text: 'Intro paragraphs', style: 'margin-top:18px;' }));
        var introWrap = el('div', {});
        var introInputs = [];
        (svc.intro || []).forEach(function (p) { introInputs.push(addParagraphRow(introWrap, p, introInputs)); });
        body.appendChild(introWrap);
        body.appendChild(el('button', { class: 'btn btn-outline btn-sm', text: '+ Add paragraph', onclick: function () {
          introInputs.push(addParagraphRow(introWrap, '', introInputs));
        } }));

        var includesTitle = textInput(svc.includes_title);
        body.appendChild(el('h3', { text: '"What we treat" section', style: 'margin-top:18px;' }));
        body.appendChild(field('Section title', includesTitle));
        var includesWrap = el('div', {});
        var includeRows = [];
        (svc.includes || []).forEach(function (inc) { includeRows.push(addIncludeRow(includesWrap, inc.title, inc.desc, includeRows)); });
        body.appendChild(includesWrap);
        body.appendChild(el('button', { class: 'btn btn-outline btn-sm', text: '+ Add item', onclick: function () {
          includeRows.push(addIncludeRow(includesWrap, '', '', includeRows));
        } }));

        var closingTitle = textInput(svc.closing_title), closingText = textArea(svc.closing_text, 3);
        body.appendChild(el('h3', { text: 'Closing banner', style: 'margin-top:18px;' }));
        body.appendChild(field('Closing title', closingTitle));
        body.appendChild(field('Closing text', closingText));

        body.appendChild(el('div', { class: 'save-bar' }, [
          el('button', { class: 'btn btn-primary', text: 'Save Changes', onclick: function () {
            var intro = introInputs.filter(function (i) { return i.value.trim(); }).map(function (i) { return i.value.trim(); });
            var includes = includeRows
              .filter(function (r) { return r.title.value.trim(); })
              .map(function (r) { return { title: r.title.value.trim(), desc: r.desc.value.trim() }; });
            crud('services', 'update', {
              id: svc.slug,
              data: {
                icon: icon.value, title: title.value, short: short.value, show_on_home: showHome.checked,
                intro: intro, includes_title: includesTitle.value, includes: includes,
                closing_title: closingTitle.value, closing_text: closingText.value,
              },
            }).then(function () { statusMsg(body, 'Saved.'); loadContentAndRender(); })
              .catch(function (e) { statusMsg(body, e.message, true); });
          } }),
          el('span', { class: 'save-status' }),
        ]));
      }

      itemCard.appendChild(body);
      mainEl.appendChild(itemCard);
    });

    mainEl.appendChild(el('div', { class: 'card' }, [
      el('h3', { text: 'Add a new service' }),
      (function () {
        var slugInput = textInput(''), titleInput = textInput('');
        var wrap = el('div', {}, [
          el('div', { class: 'row' }, [field('URL slug (letters, numbers, dashes only)', slugInput), field('Title', titleInput)]),
          el('button', { class: 'btn btn-gold', text: '+ Add Service', onclick: function () {
            var slug = slugInput.value.trim().toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
            if (!slug || !titleInput.value.trim()) { alert('Please enter both a slug and a title.'); return; }
            crud('services', 'create', {
              data: {
                slug: slug, title: titleInput.value.trim(), icon: '\u{1FA7A}', short: '', intro: [],
                includes_title: '', includes: [], closing_title: '', closing_text: '',
                show_on_home: false, sort_order: items.length,
              },
            }).then(loadContentAndRender).catch(function (e) { alert(e.message); });
          } }),
        ]);
        return wrap;
      })(),
    ]));
  }

  function addParagraphRow(wrap, value, list) {
    var input = textArea(value, 2);
    var row = el('div', { class: 'subfield-row' }, [input, el('button', { class: 'btn btn-outline btn-sm', text: '✕', onclick: function () {
      wrap.removeChild(row);
      var i = list.indexOf(input); if (i !== -1) list.splice(i, 1);
    } })]);
    wrap.appendChild(row);
    return input;
  }

  function addIncludeRow(wrap, titleVal, descVal, list) {
    var titleInput = textInput(titleVal);
    var descInput = textArea(descVal, 2);
    var pair = { title: titleInput, desc: descInput };
    var row = el('div', { class: 'subfield-row', style: 'flex-direction:column;border:1px solid var(--line);border-radius:8px;padding:10px;' }, [
      field('Item title', titleInput),
      field('Item description', descInput),
      el('button', { class: 'btn btn-outline btn-sm', text: 'Remove item', onclick: function () {
        wrap.removeChild(row);
        var i = list.indexOf(pair); if (i !== -1) list.splice(i, 1);
      } }),
    ]);
    wrap.appendChild(row);
    return pair;
  }

  // ---------------------------------------------------------------------
  // Tab: Gallery (list, keyed by slug, each with an ordered photo array)
  // ---------------------------------------------------------------------

  function renderGallery() {
    var cases = (CONTENT.gallery || []).slice().sort(function (a, b) { return a.sort_order - b.sort_order; });
    mainEl.innerHTML = '';
    mainEl.appendChild(el('h2', { text: 'Gallery' }));
    mainEl.appendChild(el('p', { class: 'hint', text: 'Clinical case photos shown on the Gallery page. The first photo in each case is its cover image.' }));

    cases.forEach(function (c, idx) {
      var title = textInput(c.title), desc = textArea(c.description, 2);
      var images = (c.images || []).slice();
      var itemCard = el('div', { class: 'list-item' });
      itemCard.appendChild(el('div', { class: 'list-item-head' }, [
        el('span', { class: 'title', text: c.title || '(untitled case)' }),
        el('div', { class: 'list-item-actions' }, [
          el('button', { class: 'btn btn-outline btn-sm', text: '↑', onclick: function () { moveItem('gallery', cases, idx, -1); } }),
          el('button', { class: 'btn btn-outline btn-sm', text: '↓', onclick: function () { moveItem('gallery', cases, idx, 1); } }),
          el('button', { class: 'btn btn-danger btn-sm', text: 'Delete Case', onclick: function () {
            if (!confirm('Delete "' + c.title + '" and all its photos from the gallery?')) return;
            crud('gallery', 'delete', { id: c.slug }).then(loadContentAndRender);
          } }),
        ]),
      ]));
      itemCard.appendChild(field('Case title', title));
      itemCard.appendChild(field('Description', desc));

      var thumbGrid = el('div', { class: 'thumb-grid' });
      function renderThumbs() {
        thumbGrid.innerHTML = '';
        images.forEach(function (url, i) {
          thumbGrid.appendChild(el('div', { class: 'thumb' }, [
            el('img', { src: url, alt: '' }),
            el('button', { text: '✕', title: 'Remove photo', onclick: function () { images.splice(i, 1); renderThumbs(); } }),
          ]));
        });
      }
      renderThumbs();
      itemCard.appendChild(el('div', {}, [el('label', { text: 'Photos (first = cover)', style: 'display:block;font-size:.8rem;font-weight:600;margin-bottom:5px;color:var(--ink-soft);' }), thumbGrid]));

      var fileInput = el('input', { type: 'file', accept: 'image/*', multiple: 'multiple' });
      itemCard.appendChild(field('Add photo(s)', fileInput));
      fileInput.addEventListener('change', function () {
        var files = Array.prototype.slice.call(fileInput.files);
        if (!files.length) return;
        statusMsg(itemCard, 'Uploading ' + files.length + ' photo(s)…');
        Promise.all(files.map(function (f) { return uploadImage(f, 'gallery'); }))
          .then(function (results) {
            results.forEach(function (r) { images.push(r.url); });
            renderThumbs();
            statusMsg(itemCard, 'Uploaded — remember to Save.');
            fileInput.value = '';
          })
          .catch(function (e) { statusMsg(itemCard, e.message, true); });
      });

      itemCard.appendChild(el('div', { class: 'save-bar' }, [
        el('button', { class: 'btn btn-primary', text: 'Save Changes', onclick: function () {
          crud('gallery', 'update', { id: c.slug, data: { title: title.value, description: desc.value, images: images } })
            .then(function () { statusMsg(itemCard, 'Saved.'); loadContentAndRender(); })
            .catch(function (e) { statusMsg(itemCard, e.message, true); });
        } }),
        el('span', { class: 'save-status' }),
      ]));
      mainEl.appendChild(itemCard);
    });

    mainEl.appendChild(el('div', { class: 'card' }, [
      el('h3', { text: 'Add a new case' }),
      (function () {
        var slugInput = textInput(''), titleInput = textInput('');
        return el('div', {}, [
          el('div', { class: 'row' }, [field('URL slug (letters, numbers, dashes only)', slugInput), field('Case title', titleInput)]),
          el('button', { class: 'btn btn-gold', text: '+ Add Case', onclick: function () {
            var slug = slugInput.value.trim().toLowerCase().replace(/[^a-z0-9-]+/g, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
            if (!slug || !titleInput.value.trim()) { alert('Please enter both a slug and a title.'); return; }
            crud('gallery', 'create', { data: { slug: slug, title: titleInput.value.trim(), description: '', images: [], sort_order: cases.length } })
              .then(loadContentAndRender).catch(function (e) { alert(e.message); });
          } }),
        ]);
      })(),
    ]));
  }

  // ---------------------------------------------------------------------
  // Tab: Contact (singleton)
  // ---------------------------------------------------------------------

  function renderContact() {
    var c = CONTENT.contact || {};
    mainEl.innerHTML = '';
    mainEl.appendChild(el('h2', { text: 'Contact Info' }));
    mainEl.appendChild(el('p', { class: 'hint', text: 'Shown in the header, footer, Contact us page and booking form site-wide.' }));

    var card = el('div', { class: 'card' });
    var address = textArea((c.address_lines || []).join('\n'), 4);
    var waDisplay = textInput(c.whatsapp_display), waHref = textInput(c.whatsapp_href);
    var phDisplay = textInput(c.phone_display), phHref = textInput(c.phone_href);
    var email = textInput(c.email);
    var fb = textInput(c.facebook), ig = textInput(c.instagram);

    card.appendChild(field('Address (one line each)', address));
    card.appendChild(el('div', { class: 'row' }, [field('WhatsApp — displayed number', waDisplay), field('WhatsApp — wa.me link', waHref)]));
    card.appendChild(el('div', { class: 'row' }, [field('Clinic phone — displayed number', phDisplay), field('Clinic phone — tel: link', phHref)]));
    card.appendChild(field('Email', email));
    card.appendChild(el('div', { class: 'row' }, [field('Facebook URL', fb), field('Instagram URL', ig)]));

    card.appendChild(el('h3', { text: 'Business hours', style: 'margin-top:18px;' }));
    var hoursWrap = el('div', {});
    var hourRows = [];
    (c.hours || []).forEach(function (h) { hourRows.push(addHourRow(hoursWrap, h.label, h.value, hourRows)); });
    card.appendChild(hoursWrap);
    card.appendChild(el('button', { class: 'btn btn-outline btn-sm', text: '+ Add row', onclick: function () {
      hourRows.push(addHourRow(hoursWrap, '', '', hourRows));
    } }));

    card.appendChild(el('div', { class: 'save-bar', style: 'margin-top:18px;' }, [
      el('button', { class: 'btn btn-primary', text: 'Save Changes', onclick: function () {
        var lines = address.value.split('\n').map(function (l) { return l.trim(); }).filter(Boolean);
        var hours = hourRows.filter(function (r) { return r.label.value.trim(); }).map(function (r) { return { label: r.label.value.trim(), value: r.value.value.trim() }; });
        crud('contact', 'update', {
          data: {
            address_lines: lines, whatsapp_display: waDisplay.value, whatsapp_href: waHref.value,
            phone_display: phDisplay.value, phone_href: phHref.value, email: email.value,
            facebook: fb.value, instagram: ig.value, hours: hours,
          },
        }).then(function (res) { CONTENT.contact = res.row; statusMsg(card, 'Saved.'); })
          .catch(function (e) { statusMsg(card, e.message, true); });
      } }),
      el('span', { class: 'save-status' }),
    ]));
    mainEl.appendChild(card);
  }

  function addHourRow(wrap, labelVal, valueVal, list) {
    var labelInput = textInput(labelVal), valueInput = textInput(valueVal);
    var pair = { label: labelInput, value: valueInput };
    var row = el('div', { class: 'subfield-row' }, [
      field('Days', labelInput), field('Hours', valueInput),
      el('button', { class: 'btn btn-outline btn-sm', text: '✕', onclick: function () {
        wrap.removeChild(row);
        var i = list.indexOf(pair); if (i !== -1) list.splice(i, 1);
      } }),
    ]);
    wrap.appendChild(row);
    return pair;
  }

  // ---------------------------------------------------------------------
  // Tab switching + content loading
  // ---------------------------------------------------------------------

  var RENDERERS = { hero: renderHero, about: renderAbout, timeline: renderTimeline, services: renderServices, gallery: renderGallery, contact: renderContact };

  sidebar.addEventListener('click', function (e) {
    var btn = e.target.closest('button[data-tab]');
    if (!btn) return;
    activeTab = btn.getAttribute('data-tab');
    Array.prototype.forEach.call(sidebar.querySelectorAll('button'), function (b) { b.classList.toggle('active', b === btn); });
    render();
  });

  function render() {
    if (!CONTENT) return;
    (RENDERERS[activeTab] || renderHero)();
  }

  function loadContentAndRender() {
    mainEl.innerHTML = '<p class="hint">Loading…</p>';
    fetchContent().then(function (data) {
      CONTENT = data;
      render();
    }).catch(function (e) {
      mainEl.innerHTML = '';
      mainEl.appendChild(el('p', { class: 'save-status error', text: 'Could not load content: ' + e.message }));
    });
  }
})();
