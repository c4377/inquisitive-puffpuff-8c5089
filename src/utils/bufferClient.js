// Thin client wrapper around the buffer-post Netlify function.
// The API key lives ONLY server-side; the browser just calls our function.

const FN = '/.netlify/functions/buffer-post';

// Fetch the user's Buffer channels (id + name + service) so they can pick one.
export const getBufferChannels = async () => {
  const res = await fetch(FN, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action: 'getChannels' }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Kanäle konnten nicht geladen werden.');
  // GraphQL shape: { data: { channels: [...] } }
  return data?.data?.channels || [];
};

// Send one post to Buffer. imageUrl must be a public URL (Supabase works).
// mode: 'addToQueue' (default) or 'draft'. service lets the function add
// network-specific metadata (e.g. Instagram requires a post type).
export const sendToBuffer = async ({ channelId, text, imageUrl, mode = 'addToQueue', service = '', igType = 'post' }) => {
  const res = await fetch(FN, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ channelId, text, imageUrl, mode, service, igType }),
  });
  const data = await res.json();
  if (!res.ok || data.error) throw new Error(data.error || 'Senden an Buffer fehlgeschlagen.');
  return data;
};
