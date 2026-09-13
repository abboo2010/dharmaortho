// Shared Supabase admin client for Netlify Functions.
// Uses the SERVICE ROLE key — this file must never run in the browser, only
// inside Netlify Functions (server-side). It bypasses Row Level Security by
// design, since these functions are the only sanctioned way to read/write
// the cms_* tables (see supabase/cms-schema.sql for why RLS has no policies).
const { createClient } = require('@supabase/supabase-js');

function getAdminClient() {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) {
    throw new Error('Missing SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY environment variables.');
  }
  return createClient(url, key, { auth: { persistSession: false } });
}

function json(statusCode, body) {
  return {
    statusCode,
    headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Access-Control-Allow-Origin': '*',
    },
    body: JSON.stringify(body),
  };
}

// Verifies the Authorization: Bearer <jwt> header against Supabase Auth.
// Returns the authenticated user, or null if the token is missing/invalid.
// Any signed-in Supabase Auth user counts as an admin — accounts are only
// ever created by an existing admin via the Supabase Dashboard, there is no
// public sign-up route, so "has an account" already means "is staff".
async function requireUser(event) {
  const auth = event.headers.authorization || event.headers.Authorization || '';
  const token = auth.startsWith('Bearer ') ? auth.slice(7) : null;
  if (!token) return null;
  try {
    const supabase = getAdminClient();
    const { data, error } = await supabase.auth.getUser(token);
    if (error || !data || !data.user) return null;
    return data.user;
  } catch (e) {
    return null;
  }
}

module.exports = { getAdminClient, json, requireUser };
