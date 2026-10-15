const models = new Map([
  ['', 'General enquiry'], ['truischjanid', 'Truischjanid'], ['lopper', 'Lopper'],
  ['muetterschwandenberg', 'Muetterschwandeberg'], ['wichelsee', 'Wichelsee'],
]);
const reply = (status, ok = false) => Response.json({ ok }, {
  status, headers: { 'Cache-Control': 'no-store' },
});

const escapeHtml = value => value.replace(/[&<>"']/g, character => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
})[character]);

function enquiryHtml(name, email, model, message) {
  const safeName = escapeHtml(name.trim());
  const safeEmail = escapeHtml(email.trim());
  const safeModel = escapeHtml(model || 'Allgemeine Anfrage');
  const safeMessage = escapeHtml(message.trim()).replace(/\r\n|\r|\n/g, '<br>');
  const replyUrl = escapeHtml(`mailto:${encodeURIComponent(email.trim())}`);
  return `<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Neue Anfrage · RAIL Cycles</title></head>
<body style="margin:0;padding:0;background-color:#eeeee9;color:#171717;font-family:Arial,Helvetica,sans-serif;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">Neue Website-Anfrage von ${safeName} · ${safeModel}</div>
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color:#eeeee9;"><tr><td align="center" style="padding:32px 16px;">
<table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="width:100%;max-width:600px;">
<tr><td bgcolor="#0b0b0b" style="padding:32px;color:#f4f4f1;">
<a href="https://www.railcycles.ch" style="font-size:38px;line-height:1;font-weight:900;letter-spacing:4px;text-decoration:none;color:#f4f4f1;">RAIL<span style="color:#aeb6a5;">.</span></a>
<p style="margin:14px 0 0;font-size:11px;letter-spacing:2px;color:#b8b8b2;">HAND GMACHT · SWISS CUSTOM BICYCLES</p></td></tr>
<tr><td bgcolor="#ffffff" style="padding:32px;border-bottom:1px solid #e6e6df;">
<p style="margin:0 0 12px;font-size:11px;font-weight:bold;letter-spacing:2px;color:#65705c;">KONTAKTFORMULAR</p>
<h1 style="margin:0 0 12px;font-size:30px;line-height:1.2;">Neue Anfrage.</h1>
<p style="margin:0;font-size:16px;line-height:1.6;color:#60605b;">${safeName} hat dir über die RAIL Website geschrieben.</p></td></tr>
<tr><td bgcolor="#ffffff" style="padding:24px 32px;">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="font-size:15px;line-height:1.6;">
<tr><td width="100" valign="top" style="padding:7px 12px 7px 0;color:#73736c;">Name</td><td style="padding:7px 0;word-break:break-word;">${safeName}</td></tr>
<tr><td width="100" valign="top" style="padding:7px 12px 7px 0;color:#73736c;">E-Mail</td><td style="padding:7px 0;word-break:break-word;"><a href="${replyUrl}" style="color:#171717;text-decoration:underline;">${safeEmail}</a></td></tr>
<tr><td width="100" valign="top" style="padding:7px 12px 7px 0;color:#73736c;">Interesse</td><td style="padding:7px 0;font-weight:bold;">${safeModel}</td></tr></table></td></tr>
<tr><td bgcolor="#ffffff" style="padding:0 32px 32px;">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0"><tr><td bgcolor="#f4f4ef" style="padding:24px;border-left:3px solid #aeb6a5;">
<p style="margin:0 0 12px;font-size:11px;font-weight:bold;letter-spacing:2px;color:#65705c;">NACHRICHT</p>
<p dir="auto" style="margin:0;font-size:16px;line-height:1.75;overflow-wrap:anywhere;word-break:break-word;">${safeMessage}</p></td></tr></table>
<table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin-top:28px;"><tr><td bgcolor="#0b0b0b" style="padding:15px 24px;"><a href="${replyUrl}" style="color:#ffffff;text-decoration:none;font-size:14px;font-weight:bold;">Auf die Anfrage antworten &rarr;</a></td></tr></table>
<p style="margin:16px 0 0;font-size:12px;line-height:1.6;color:#73736c;">Du kannst auch direkt auf diese E-Mail antworten.</p></td></tr>
<tr><td style="padding:24px 8px;font-size:12px;line-height:1.7;color:#73736c;">RAIL Cycles · Von Hand gebaut. Für deinen Weg.<br><a href="https://www.railcycles.ch" style="color:#73736c;">www.railcycles.ch</a></td></tr>
</table></td></tr></table></body></html>`;
}

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
        html: enquiryHtml(name, email, model ? models.get(model) : '', message),
      }),
      signal: AbortSignal.timeout(10000),
    });
    if (!response.ok) return reply(502);
    const result = await response.json();
    if (!result.id) return reply(502);
    return reply(200, true);
  } catch { return reply(502); }
}
