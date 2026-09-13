# dharmaortho.my — Rebuild

A fresh, modern rebuild of Dr. Dharmalingam Muthiah's orthopaedic clinic
website, replacing the old PHP/Joomla-style site. Same real content, contact
details and doctor photo pulled from the live site — new design, faster pages,
and built the same way as click4techsolutions.com and the temple site
(static HTML → GitHub → Netlify), now with a full content management
dashboard so the clinic team can update the site without touching code.

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
  regenerate every page consistently. This is also the "source of truth"
  content that the CMS is seeded from — you no longer need to edit this
  file day-to-day once the CMS is set up (see below).
- `admin.html` + `assets/admin.js` — the CMS dashboard staff log into to
  edit the site.
- `assets/admin-config.js` — holds the Supabase project URL and public key
  the dashboard connects with (you fill this in once during setup).
- `js/cms-loader.js` — runs on every public page; fetches the latest saved
  content and overlays it on top of the page before `main.js` runs. If it
  can't reach the CMS for any reason, the page silently shows the original
  built-in content instead — visitors never see an error.
- `supabase/cms-schema.sql`, `supabase/cms-seed.sql` — one-time database
  setup scripts (see CMS setup below).
- `netlify/functions/` — the three small server-side functions the
  dashboard and public pages talk to (reading content, saving content,
  uploading photos).

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

## Content management system (CMS)

The site now has a full editing dashboard at `admin.html` (e.g.
`https://dharmaortho.my/admin.html`), covering:

- **Home Hero** — the eyebrow line, heading, description, both buttons, the
  3 stat numbers/labels, and the hero photo.
- **About Dr** — the bio paragraphs, credentials line, photo, the highlighted
  quote line, and the "Education, Fellowships & Special Interests" timeline
  (add/remove/reorder entries).
- **Services** — all 13 service pages: icon, title, short description,
  intro paragraphs, the "What We Treat" list, the closing banner, and
  whether each one shows as one of the 9 preview cards on the homepage. You
  can also add a brand-new service (it gets its own page automatically) or
  delete one.
- **Gallery** — the 9 clinical case cards: title, description, and photos
  (upload new ones, remove old ones — the first photo in each case is used
  as its cover image). You can add or delete whole cases too.
- **Contact Info** — address, phone/WhatsApp/email, business hours, and the
  Facebook/Instagram links used throughout the site.

Changes made in the dashboard go live on the public site within a few
seconds — no code edits, no waiting for a deploy.

**Not covered by the CMS** (these still require editing `build.py` and
re-running it, since they're one-time setup rather than day-to-day content):
the splash screen's photo/wording/timing, the booking form's time slots and
notification email, the contact/booking form notification emails, and the
"Explore Other Services" sidebar list shown on individual service pages.

### One-time setup

You (or whoever manages the Netlify/GitHub side) need to do this once
before the dashboard will work:

1. **Create a Supabase project** at [supabase.com](https://supabase.com)
   (the free tier is plenty for this site). Note down, from
   **Project Settings → API**: the **Project URL**, the **anon/public key**,
   and the **service_role key** (keep the service_role key secret — it's
   not the same as the public one).

2. **Run the database setup scripts.** In the Supabase dashboard, open the
   **SQL Editor**, paste in the full contents of `supabase/cms-schema.sql`
   and run it (creates the tables), then do the same with
   `supabase/cms-seed.sql` (loads in all of the site's current content as
   the starting point). Both are safe to re-run if needed.

3. **Add the Supabase keys to Netlify.** In the Netlify dashboard for this
   site: **Site configuration → Environment variables → Add a variable**,
   and add two:
   - `SUPABASE_URL` → the Project URL from step 1
   - `SUPABASE_SERVICE_ROLE_KEY` → the service_role key from step 1

   Redeploy the site once after adding these so the serverless functions
   pick them up.

4. **Fill in `assets/admin-config.js`** with the Project URL and the
   **anon/public** key (not the service_role key — that one only goes in
   Netlify, never in a file that ships to the browser):

   ```js
   window.CMS_CONFIG = {
     SUPABASE_URL: 'https://your-project.supabase.co',
     SUPABASE_ANON_KEY: 'your-anon-public-key',
   };
   ```

   Commit this file and redeploy (or edit it directly in GitHub — it
   contains no secrets, so it's fine for it to be in the repo).

5. **Create login accounts for staff.** There's no public sign-up page —
   accounts are created by you in the Supabase dashboard:
   **Authentication → Users → Add user**, enter their email and a password
   (or send an invite email, if you'd rather they set their own password).
   Each person you add this way can log into `admin.html` with that email
   and password. To remove someone's access later, delete their user there.

Once those five steps are done, anyone with a login can go to
`admin.html`, sign in, and start editing. If the dashboard ever can't be
reached (Supabase down, keys misconfigured, etc.), the public site is
unaffected — it just keeps showing the last content that was baked into
the pages by `build.py`.

## What's NOT in this phase

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
