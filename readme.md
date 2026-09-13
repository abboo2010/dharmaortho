# dharmaortho.my — Rebuild (Phase 1: Static Redesign)

A fresh, modern static rebuild of Dr. Dharmalingam Muthiah's orthopaedic clinic
website, replacing the old PHP/Joomla-style site. Same real content, contact
details and doctor photo pulled from the live site — new design, faster pages,
and built the same way as click4techsolutions.com and the temple site
(static HTML → GitHub → Netlify).

## What's inside

- `index.html`, `about.html`, `services.html`, `gallery.html`, `contact.html`,
  `book-consultation.html`
- `services/` — 13 individual service detail pages (Hip Replacement, VELYS™
  Robotic-Assisted Knee Replacement, Joint Replacement, Trauma, Hand & Ankle,
  Paediatric, Bone/Soft Tissue Tumours, etc.)
- `css/styles.css` — shared design system (navy/gold palette, Fraunces + Inter fonts)
- `js/main.js` — mobile nav + contact form handling
- `images/` — doctor portrait, real logo, and a full 32-photo case gallery
  (9 clinical cases) pulled from the live site, plus a generated favicon
- `build.py` — the generator script. All page content lives in one Python
  file (`SERVICES` list + page functions), so future text edits are a
  find-and-replace in `build.py` followed by `python3 build.py` to
  regenerate every page consistently.

## How to deploy (same flow as click4techsolutions.com)

1. Push this folder's contents to the GitHub repo for dharmaortho.my
   (or a new repo if you're starting fresh).
2. Connect that repo to Netlify (or update the existing site's repo).
3. No build command needed — this is plain static HTML/CSS/JS, so set the
   publish directory to the repo root.
4. Point the dharmaortho.my domain at the Netlify site (same DNS pattern
   used for click4techsolutions.com).

## Contact form (Netlify Forms)

The "Send an Enquiry" form on `contact.html` is wired to Netlify Forms —
no backend code needed, since Netlify detects the form's `data-netlify="true"`
attribute at deploy time and captures every submission automatically. To
receive them by email:

1. Deploy the site to Netlify (see below) and submit the form once from the
   live site so Netlify registers it.
2. In the Netlify dashboard: **Site configuration → Forms → Form notifications
   → Add notification → Email notification**, and set it to
   `enquiry@dharmaortho.my`.
3. That's it — every future submission auto-emails that address, and all
   submissions also stay logged under **Forms** in the Netlify dashboard as
   a backup. A hidden honeypot field is included for basic spam filtering.

WhatsApp itself can't receive form submissions directly (no plain API for
that) — the "Chat on WhatsApp" buttons stay as click-to-chat links for
visitors who prefer to message directly.

## Booking a consultation (Netlify Forms)

Every "Book Consultation" button site-wide now goes to `book-consultation.html`
instead of the plain contact page. It's a 3-step form: Patient's Details,
then a date picker, then a grid of time slots that updates automatically
based on the weekday picked:

- **Monday–Friday:** 09:00, 09:30, 10:00, 10:30, 11:00, 11:30 AM, 12:00,
  12:30, 02:00, 02:30, 03:00, 03:30 PM
- **Saturday:** 09:00, 09:30, 10:00, 10:30, 11:00, 11:30 AM, 12:00, 12:30 PM
- **Sunday** is blocked — picking a Sunday shows an inline message asking
  for Monday–Saturday instead.

To change the hours or slot times later, edit the `BOOKING_SLOTS` dict near
the top of `build.py` and re-run it — no need to touch the page markup.

Like the contact form, this uses Netlify Forms (form name `booking`) so it
needs the same one-time setup, as a **separate** notification pointed at a
different inbox:

1. Deploy/redeploy the site and submit the booking form once from the live
   site so Netlify registers it as a distinct form (separate from `contact`).
2. In the Netlify dashboard: **Site configuration → Forms → Form
   notifications → Add notification → Email notification**, and set it to
   `appointment@dharmaortho.my`.

Every submission includes a clear note (on-page and in the confirmation
popup) that it's a request, not a confirmed appointment — the clinic team
still follows up to lock in the exact time.

## Splash screen (home page)

The homepage (`index.html`) now opens with a brief animated splash — the
clinic logo, Dr. Dharmalingam Muthiah's name, and the VELYS™/knee photo
fading in on a navy background, with a "Tap anywhere to continue" hint.

- It auto-advances into the homepage after ~3.2 seconds, or a visitor can
  tap/click anywhere to skip straight in.
- It only shows once per browser session — using it again, or navigating
  back to the homepage, won't replay it until the browser is closed and
  reopened (it uses `sessionStorage`, not a permanent cookie).
- It only lives on `index.html`, not on the other pages.
- To change the photo, replace `images/velys-splash.png` and re-run
  `python3 build.py`. To change the wording/name, or how long it displays
  before auto-advancing, edit `splash_html()` and the `setTimeout(hideSplash, 3200)`
  line in `js/main.js`.

## What's NOT in this phase

- No backend/CMS yet — text edits currently mean editing `build.py` and
  re-running it. A Supabase-backed content dashboard (like the one on
  click4techsolutions.com and the temple site) is a natural next step
  once you're happy with this design — just say the word.
- The Gallery page now has a full Photo Gallery (32 real case photos across
  9 cases, with a lightbox) and a Video Gallery section — the video section
  is built and styled but shows "Coming Soon" placeholders, since there are
  no videos live on the source site yet. Send me video files/links (or say
  the word) whenever you have them and I'll drop them straight in.

## Notes on content

All copy (services, About Dr, contact info, business hours) was pulled
directly from the live dharmaortho.my site so nothing was invented. Icons
are emoji placeholders — happy to swap in a custom icon set if you'd
prefer a more premium look there.
