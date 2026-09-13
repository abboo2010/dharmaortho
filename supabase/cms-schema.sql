-- dharmaortho.my — CMS schema
-- Run this once in the Supabase SQL Editor (Project → SQL Editor → New query → paste → Run).
-- Safe to re-run: every statement is idempotent (IF NOT EXISTS / ON CONFLICT DO NOTHING).
--
-- Design notes:
--   * Every table has Row Level Security ENABLED with NO policies for anon/authenticated.
--     That means the browser can never read or write these tables directly, even with a
--     leaked anon key — all reads/writes go through the Netlify Functions in
--     netlify/functions/, which use the SERVICE ROLE key (server-side only, bypasses RLS).
--   * Admin login uses Supabase Auth (real email+password accounts), not a shared password.
--     Create staff accounts via Supabase Dashboard → Authentication → Users → Add user
--     (see README.md "CMS setup" section) — there is no public sign-up form.
--   * A public Storage bucket ("dharmaortho-media") holds uploaded photos (gallery, hero,
--     about) so the built pages can just <img src="..."> them directly.

-- ---------------------------------------------------------------------------
-- Singletons (exactly one row each, id is always 1)
-- ---------------------------------------------------------------------------

create table if not exists cms_hero (
  id int primary key default 1 check (id = 1),
  eyebrow text not null default '',
  heading_line1 text not null default '',
  heading_em text not null default '',
  lede text not null default '',
  cta_primary_label text not null default '',
  cta_primary_href text not null default '',
  cta_secondary_label text not null default '',
  cta_secondary_href text not null default '',
  stat1_value text not null default '',
  stat1_label text not null default '',
  stat2_value text not null default '',
  stat2_label text not null default '',
  stat3_value text not null default '',
  stat3_label text not null default '',
  hero_image_url text not null default '',
  updated_at timestamptz not null default now()
);
alter table cms_hero enable row level security;

create table if not exists cms_about (
  id int primary key default 1 check (id = 1),
  credentials_line text not null default '',
  bio_para1 text not null default '',
  bio_para2 text not null default '',
  bio_highlight_bold text not null default '',
  bio_highlight_rest text not null default '',
  home_bio_para1 text not null default '',
  home_bio_para2 text not null default '',
  photo_url text not null default '',
  updated_at timestamptz not null default now()
);
alter table cms_about enable row level security;

create table if not exists cms_contact (
  id int primary key default 1 check (id = 1),
  address_lines jsonb not null default '[]'::jsonb,
  whatsapp_display text not null default '',
  whatsapp_href text not null default '',
  phone_display text not null default '',
  phone_href text not null default '',
  email text not null default '',
  facebook text not null default '',
  instagram text not null default '',
  hours jsonb not null default '[]'::jsonb,
  updated_at timestamptz not null default now()
);
alter table cms_contact enable row level security;

-- ---------------------------------------------------------------------------
-- Lists
-- ---------------------------------------------------------------------------

create table if not exists cms_timeline_items (
  id uuid primary key default gen_random_uuid(),
  place text not null default '',
  description text not null default '',
  sort_order int not null default 0,
  updated_at timestamptz not null default now()
);
alter table cms_timeline_items enable row level security;

create table if not exists cms_services (
  slug text primary key,
  icon text not null default '',
  title text not null default '',
  short text not null default '',
  intro jsonb not null default '[]'::jsonb,           -- array of paragraph strings
  includes_title text not null default '',
  includes jsonb not null default '[]'::jsonb,         -- array of {title, desc}
  closing_title text not null default '',
  closing_text text not null default '',
  show_on_home boolean not null default false,
  sort_order int not null default 0,
  updated_at timestamptz not null default now()
);
alter table cms_services enable row level security;

create table if not exists cms_gallery_cases (
  slug text primary key,
  title text not null default '',
  description text not null default '',
  images jsonb not null default '[]'::jsonb,           -- array of image URLs, first = cover
  sort_order int not null default 0,
  updated_at timestamptz not null default now()
);
alter table cms_gallery_cases enable row level security;

-- ---------------------------------------------------------------------------
-- Storage: public bucket for uploaded photos
-- ---------------------------------------------------------------------------

insert into storage.buckets (id, name, public)
values ('dharmaortho-media', 'dharmaortho-media', true)
on conflict (id) do nothing;

-- No storage.objects policies are added for anon/authenticated — all uploads go through
-- the password-protected cms-upload-image Netlify Function using the service role key.
-- The bucket itself is public so uploaded files are readable via their public URL.
