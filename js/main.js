// Dr. Dharmalingam Muthiah — site scripts (mobile nav + dropdown handling)
//
// This file is loaded by js/cms-loader.js AFTER it applies any live CMS
// content, which usually happens well after DOMContentLoaded has already
// fired (fetch is async). ready() below runs the init immediately in that
// case, instead of registering a DOMContentLoaded listener that would never
// fire again.
function ready(fn) {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fn);
  } else {
    fn();
  }
}

ready(function () {
  var toggle = document.querySelector('.nav-toggle');
  var navLinks = document.querySelector('.nav-links');
  var scrim = document.querySelector('.nav-scrim');
  var body = document.body;

  function closeNav() {
    navLinks && navLinks.classList.remove('open');
    scrim && scrim.classList.remove('open');
    body.classList.remove('nav-open');
  }

  if (toggle && navLinks) {
    toggle.addEventListener('click', function () {
      navLinks.classList.toggle('open');
      scrim && scrim.classList.toggle('open');
      body.classList.toggle('nav-open');
    });
  }
  if (scrim) scrim.addEventListener('click', closeNav);

  // On mobile, tapping a "has-dropdown" label toggles its submenu instead of navigating away
  document.querySelectorAll('.has-dropdown > a').forEach(function (a) {
    a.addEventListener('click', function (e) {
      if (window.innerWidth <= 980) {
        e.preventDefault();
        a.parentElement.classList.toggle('open');
      }
    });
  });

  // Close mobile nav when a real link is followed
  document.querySelectorAll('.nav-links a:not(.has-dropdown > a)').forEach(function (a) {
    a.addEventListener('click', closeNav);
  });

  // ---------- Splash screen (home page only, once per browser session) ----------
  var splash = document.getElementById('splash-screen');
  if (splash) {
    var splashAlreadySeen = false;
    try { splashAlreadySeen = !!sessionStorage.getItem('dharma_splash_seen'); } catch (e) {}

    if (splashAlreadySeen) {
      // The inline head script already hid it via CSS before paint — just clean up the DOM.
      splash.parentNode && splash.parentNode.removeChild(splash);
    } else {
      body.classList.add('splash-active');

      var hideSplash = function () {
        if (splash.classList.contains('is-hiding')) return;
        splash.classList.add('is-hiding');
        body.classList.remove('splash-active');
        try { sessionStorage.setItem('dharma_splash_seen', '1'); } catch (e) {}
        setTimeout(function () {
          splash.parentNode && splash.parentNode.removeChild(splash);
        }, 650);
      };

      splash.addEventListener('click', hideSplash);
      setTimeout(hideSplash, 3200);
    }
  }

  // Contact form: submits to Netlify Forms via AJAX so the page never reloads
  var form = document.getElementById('contact-form');
  var formModal = document.getElementById('form-modal');

  function openFormModal(isError, title, message) {
    if (!formModal) return;
    formModal.classList.toggle('is-error', !!isError);
    var titleEl = formModal.querySelector('.form-modal-title');
    var messageEl = formModal.querySelector('.form-modal-message');
    if (titleEl) titleEl.textContent = title;
    if (messageEl) messageEl.textContent = message;
    formModal.hidden = false;
    document.body.classList.add('modal-open');
  }

  function closeFormModal() {
    if (!formModal) return;
    formModal.hidden = true;
    document.body.classList.remove('modal-open');
  }

  if (formModal) {
    formModal.querySelectorAll('[data-close]').forEach(function (el) {
      el.addEventListener('click', closeFormModal);
    });
    document.addEventListener('keydown', function (e) {
      if (!formModal.hidden && e.key === 'Escape') closeFormModal();
    });
  }

  var encode = function (data) {
    return Object.keys(data)
      .map(function (key) { return encodeURIComponent(key) + '=' + encodeURIComponent(data[key]); })
      .join('&');
  };

  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var submitBtn = form.querySelector('button[type="submit"]');
      var formData = {};
      new FormData(form).forEach(function (value, key) { formData[key] = value; });

      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Sending…'; }

      fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: encode(formData),
      })
        .then(function () {
          openFormModal(
            false,
            'Enquiry Sent',
            'Thank you — your enquiry has been sent. We will get back to you as soon as possible. For urgent matters, please WhatsApp us directly.'
          );
          form.reset();
        })
        .catch(function () {
          openFormModal(
            true,
            'Something Went Wrong',
            'Sorry, we couldn’t send your enquiry. Please try again or reach us on WhatsApp.'
          );
        })
        .finally(function () {
          if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = 'Submit'; }
        });
    });
  }

  // ---------- Booking form: date-aware time slots + Netlify Forms submit ----------
  var bookingForm = document.getElementById('booking-form');
  var slotsDataEl = document.getElementById('booking-slots-data');
  if (bookingForm && slotsDataEl) {
    var SLOTS = JSON.parse(slotsDataEl.textContent);
    var dateInput = document.getElementById('apt-date');
    var dateError = document.getElementById('date-error');
    var timeHint = document.getElementById('time-hint');
    var timeGrid = document.getElementById('time-slot-grid');
    var timeInput = document.getElementById('apt-time');
    var bookingSubmitBtn = bookingForm.querySelector('button[type="submit"]');

    // Earliest bookable date is tomorrow (local time-zone safe).
    var minDate = new Date();
    minDate.setDate(minDate.getDate() + 1);
    var pad = function (n) { return n < 10 ? '0' + n : '' + n; };
    var minDateStr = minDate.getFullYear() + '-' + pad(minDate.getMonth() + 1) + '-' + pad(minDate.getDate());
    dateInput.setAttribute('min', minDateStr);

    // NRIC / Passport No: auto-insert dashes as xxxxxx-xx-xxxx while the patient
    // is typing an NRIC (digits only). Passport numbers (containing letters)
    // are left as typed, since they don't follow that pattern.
    var nricInput = document.getElementById('nric');
    if (nricInput) {
      nricInput.addEventListener('input', function () {
        var raw = nricInput.value;
        if (/[a-zA-Z]/.test(raw)) return; // looks like a passport number — don't reformat
        var digits = raw.replace(/\D/g, '').slice(0, 12);
        var formatted = digits;
        if (digits.length > 8) {
          formatted = digits.slice(0, 6) + '-' + digits.slice(6, 8) + '-' + digits.slice(8);
        } else if (digits.length > 6) {
          formatted = digits.slice(0, 6) + '-' + digits.slice(6);
        }
        nricInput.value = formatted;
        var nricErrorEl = document.getElementById('nric-error');
        if (nricErrorEl) nricErrorEl.hidden = true;
      });
    }

    function clearSlots() {
      timeGrid.innerHTML = '';
      timeInput.value = '';
    }

    function renderSlots(list) {
      clearSlots();
      list.forEach(function (slot) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'time-slot';
        btn.textContent = slot;
        btn.addEventListener('click', function () {
          timeGrid.querySelectorAll('.time-slot').forEach(function (b) { b.classList.remove('selected'); });
          btn.classList.add('selected');
          timeInput.value = slot;
        });
        timeGrid.appendChild(btn);
      });
    }

    dateInput.addEventListener('change', function () {
      if (!dateInput.value) return;
      var parts = dateInput.value.split('-').map(Number);
      var picked = new Date(parts[0], parts[1] - 1, parts[2]);
      var weekday = picked.getDay(); // 0 = Sunday, 6 = Saturday

      if (weekday === 0) {
        dateError.hidden = false;
        timeHint.textContent = 'Pick a date above to see available time slots.';
        clearSlots();
        return;
      }
      dateError.hidden = true;
      timeHint.textContent = 'Select an available time slot below.';
      renderSlots(weekday === 6 ? SLOTS.saturday : SLOTS.weekday);
    });

    var nricError = document.getElementById('nric-error');

    function isValidNricOrPassport(value) {
      if (/[a-zA-Z]/.test(value)) return value.trim().length >= 5; // treat as passport
      return /^\d{6}-\d{2}-\d{4}$/.test(value); // must be a complete NRIC
    }

    bookingForm.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!dateInput.value || !dateError.hidden) {
        dateError.hidden = false;
        return;
      }
      if (!timeInput.value) {
        timeHint.textContent = 'Please select a time slot before submitting.';
        return;
      }
      if (nricInput && nricError && !isValidNricOrPassport(nricInput.value)) {
        nricError.hidden = false;
        nricInput.focus();
        return;
      }
      if (nricError) nricError.hidden = true;
      var formData = {};
      new FormData(bookingForm).forEach(function (value, key) { formData[key] = value; });

      if (bookingSubmitBtn) { bookingSubmitBtn.disabled = true; bookingSubmitBtn.textContent = 'Sending…'; }

      fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: encode(formData),
      })
        .then(function () {
          openFormModal(
            false,
            'Booking Request Sent',
            'Thank you — we’ve received your requested date and time. Our clinic team will contact you shortly to confirm your appointment.'
          );
          bookingForm.reset();
          clearSlots();
          timeHint.textContent = 'Pick a date above to see available time slots.';
        })
        .catch(function () {
          openFormModal(
            true,
            'Something Went Wrong',
            'Sorry, we couldn’t send your booking request. Please try again or reach us on WhatsApp.'
          );
        })
        .finally(function () {
          if (bookingSubmitBtn) { bookingSubmitBtn.disabled = false; bookingSubmitBtn.textContent = 'Request Appointment'; }
        });
    });
  }

  // ---------- Gallery: Photo/Video tabs ----------
  var tabs = document.querySelectorAll('.gallery-tab');
  if (tabs.length) {
    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        tabs.forEach(function (t) {
          t.classList.remove('active');
          t.setAttribute('aria-selected', 'false');
        });
        tab.classList.add('active');
        tab.setAttribute('aria-selected', 'true');
        var target = tab.getAttribute('data-tab');
        document.querySelectorAll('.gallery-panel').forEach(function (panel) {
          panel.hidden = panel.getAttribute('data-panel') !== target;
        });
      });
    });
  }

  // ---------- Gallery: case-photo lightbox ----------
  var dataEl = document.getElementById('gallery-data');
  var lightbox = document.getElementById('lightbox');
  if (dataEl && lightbox) {
    var galleryData = JSON.parse(dataEl.textContent);
    var lbImg = lightbox.querySelector('.lightbox-img');
    var lbTitle = lightbox.querySelector('.lightbox-title');
    var lbCount = lightbox.querySelector('.lightbox-count');
    var currentCase = null;
    var currentIndex = 0;

    function renderLightbox() {
      var c = galleryData[currentCase];
      lbImg.src = c.images[currentIndex];
      lbImg.alt = c.title;
      lbTitle.textContent = c.title;
      lbCount.textContent = (currentIndex + 1) + ' / ' + c.images.length;
    }

    function openLightbox(slug) {
      if (!galleryData[slug]) return;
      currentCase = slug;
      currentIndex = 0;
      renderLightbox();
      lightbox.hidden = false;
      body.style.overflow = 'hidden';
    }

    function closeLightbox() {
      lightbox.hidden = true;
      body.style.overflow = '';
    }

    function step(delta) {
      var c = galleryData[currentCase];
      currentIndex = (currentIndex + delta + c.images.length) % c.images.length;
      renderLightbox();
    }

    document.querySelectorAll('.case-card').forEach(function (card) {
      card.addEventListener('click', function () {
        openLightbox(card.getAttribute('data-case'));
      });
    });
    lightbox.querySelectorAll('[data-close]').forEach(function (el) {
      el.addEventListener('click', closeLightbox);
    });
    lightbox.querySelector('.lightbox-prev').addEventListener('click', function () { step(-1); });
    lightbox.querySelector('.lightbox-next').addEventListener('click', function () { step(1); });
    document.addEventListener('keydown', function (e) {
      if (lightbox.hidden) return;
      if (e.key === 'Escape') closeLightbox();
      if (e.key === 'ArrowLeft') step(-1);
      if (e.key === 'ArrowRight') step(1);
    });
  }
});
