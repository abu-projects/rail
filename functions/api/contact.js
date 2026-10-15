const models = new Map([
  ['', 'General enquiry'], ['truischjanid', 'Truischjanid'], ['lopper', 'Lopper'],
  ['muetterschwandenberg', 'Muetterschwandeberg'], ['wichelsee', 'Wichelsee'],
]);
const reply = (status, ok = false) => Response.json({ ok }, {
  status, headers: { 'Cache-Control': 'no-store' },
});

export async function onRequest({ request, env }) {
  if (request.method !== 'POST') return reply(405);
  const origin = new URL(request.url).origin;
  if (request.headers.get('Origin') !== origin) return reply(403);
  if (!request.headers.get('Content-Type')?.startsWith('application/json')) return reply(415);
  if (Number(request.headers.get('Content-Length')) > 16000) return reply(413);
  let data;
  try {
    const body = await request.text();
    if (new TextEncoder().encode(body).length > 16000) return reply(413);
    data = JSON.parse(body);
  } catch { return reply(400); }
  if (!data || typeof data !== 'object' || Array.isArray(data)) return reply(400);
  // A hidden field catches simple form bots without sending a message.
  if (data.website) return reply(200, true);
  const { name, email, message, model = '' } = data;
  if ([name, email, message, model].some(value => typeof value !== 'string')) return reply(400);
  if (!name.trim() || name.length > 100 || /[\r\n\x00]/.test(name)
    || email.length > 254 || !/^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/.test(email)
    || !message.trim() || message.length > 3000 || message.includes('\x00')
    || !models.has(model)) return reply(400);
  if (!env.RESEND_API_KEY || !env.CONTACT_TO_EMAIL || !env.CONTACT_FROM_EMAIL) return reply(503);
  try {
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: env.CONTACT_FROM_EMAIL,
        to: [env.CONTACT_TO_EMAIL],
        reply_to: email.trim(),
        subject: `RAIL website enquiry: ${models.get(model)}`,
        text: `Name: ${name.trim()}\nEmail: ${email.trim()}\nModel: ${models.get(model)}\n\n${message.trim()}`,
      }),
      signal: AbortSignal.timeout(10000),
    });
    if (!response.ok) return reply(502);
    const result = await response.json();
    if (!result.id) return reply(502);
    return reply(200, true);
  } catch { return reply(502); }
}
