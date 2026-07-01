// Netlify serverless function: secure proxy to the Buffer GraphQL API.
//
// WHY THIS EXISTS: the Buffer API key must never live in the browser bundle
// (anyone could read it and post as you). This function runs server-side on
// Netlify, reads the key from an environment variable (BUFFER_API_KEY), and is
// the only place the key is ever used.
//
// SETUP (once, in the Netlify dashboard):
//   Site settings -> Environment variables -> add:
//     BUFFER_API_KEY = <your personal Buffer API key from
//                       https://publish.buffer.com/settings/api>
//
// The frontend calls this function with { channelId, text, imageUrl, mode }.
// mode: 'addToQueue' (default) | 'draft' | 'now' style handled via schedulingType.

const BUFFER_API = 'https://api.buffer.com';

exports.handler = async (event) => {
  // CORS preflight (same-origin on Netlify, but harmless to allow).
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 204, headers: cors(), body: '' };
  }
  if (event.httpMethod !== 'POST') {
    return resp(405, { error: 'Method not allowed' });
  }

  const apiKey = process.env.BUFFER_API_KEY;
  if (!apiKey) {
    return resp(500, { error: 'BUFFER_API_KEY ist nicht gesetzt (Netlify Environment Variables).' });
  }

  let body;
  try {
    body = JSON.parse(event.body || '{}');
  } catch (e) {
    return resp(400, { error: 'Ungültiger Request-Body.' });
  }

  const { channelId, text, imageUrl, mode } = body;

  // --- Special action: list channels (so the app can let the user pick one) ---
  if (body.action === 'getChannels') {
    // Buffer requires an organizationId to list channels. Step 1: get the org
    // (or use a configured fallback if the account query is unavailable).
    let organizationId = process.env.BUFFER_ORG_ID || '';
    if (!organizationId) {
      const orgQuery = `query { account { organizations { id name } } }`;
      const orgRes = await callBuffer(apiKey, orgQuery);
      if (!orgRes.ok) return resp(502, orgRes.data);
      if (orgRes.data?.errors?.length) {
        return resp(400, { error: orgRes.data.errors[0].message || 'Organisation konnte nicht geladen werden.' });
      }
      const orgs = orgRes.data?.data?.account?.organizations || [];
      if (!orgs.length) return resp(400, { error: 'Keine Buffer-Organisation gefunden.' });
      organizationId = orgs[0].id;
    }

    // Step 2: get channels for that organization.
    const chQuery = `query GetChannels {
      channels(input: { organizationId: ${JSON.stringify(organizationId)} }) {
        id
        name
        displayName
        service
      }
    }`;
    const chRes = await callBuffer(apiKey, chQuery);
    if (!chRes.ok) return resp(502, chRes.data);
    if (chRes.data?.errors?.length) {
      return resp(400, { error: chRes.data.errors[0].message || 'Kanäle konnten nicht geladen werden.' });
    }
    // Normalize to { channels: [...] } so the client stays simple.
    return resp(200, { data: { channels: chRes.data?.data?.channels || [] } });
  }

  // --- Default action: create a post ---
  if (!channelId) return resp(400, { error: 'channelId fehlt.' });
  if (!text && !imageUrl) return resp(400, { error: 'Text oder Bild erforderlich.' });

  // draft -> save as draft; otherwise add to the Buffer queue (automatic slot).
  const wantDraft = mode === 'draft';
  const assetsPart = imageUrl
    ? `assets: [{ image: { url: ${JSON.stringify(imageUrl)} } }]`
    : '';

  const mutation = `
    mutation CreatePost {
      createPost(input: {
        text: ${JSON.stringify(text || '')}
        channelId: ${JSON.stringify(channelId)}
        schedulingType: automatic
        mode: ${wantDraft ? 'draft' : 'addToQueue'}
        ${assetsPart}
      }) {
        ... on PostActionSuccess {
          post { id text }
        }
        ... on MutationError { message }
      }
    }`;

  const r = await callBuffer(apiKey, mutation);
  if (!r.ok) return resp(502, r.data);

  // Surface a GraphQL-level MutationError as a clean error to the app.
  const result = r.data?.data?.createPost;
  if (result && result.message) {
    return resp(400, { error: result.message });
  }
  return resp(200, { ok: true, post: result?.post || null });
};

async function callBuffer(apiKey, query) {
  try {
    const res = await fetch(BUFFER_API, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({ query }),
    });
    const data = await res.json();
    return { ok: res.ok, data };
  } catch (e) {
    return { ok: false, data: { error: String(e && e.message || e) } };
  }
}

function cors() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
  };
}
function resp(statusCode, obj) {
  return { statusCode, headers: { 'Content-Type': 'application/json', ...cors() }, body: JSON.stringify(obj) };
}
