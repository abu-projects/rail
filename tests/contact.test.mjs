import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';

// Import the Pages module as ESM without changing the static site's package setup.
const source = await readFile(new URL('../functions/api/contact.js', import.meta.url), 'utf8');
const { onRequest } = await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);
const fields = { name: 'Test rider', email: 'rider@example.com', model: 'wichelsee', message: 'A test enquiry.' };
const env = { RESEND_API_KEY: 'test-only', CONTACT_TO_EMAIL: 'owner@example.com', CONTACT_FROM_EMAIL: 'RAIL <website@railcycles.ch>' };
function context(data = fields, options = {}) {
  return { env, request: new Request('https://railcycles.ch/api/contact', {
    method: 'POST', headers: { Origin: 'https://railcycles.ch', 'Content-Type': 'application/json', ...options.headers },
    body: typeof data === 'string' ? data : JSON.stringify(data),
  }) };
}

test('valid enquiry reaches the configured recipient and replies to the visitor', async t => {
  let sent;
  t.mock.method(globalThis, 'fetch', async (_url, options) => {
    sent = JSON.parse(options.body);
    return Response.json({ id: 'accepted-message' });
  });
  const response = await onRequest(context({ ...fields, to: 'attacker@example.com' }));
  assert.equal(response.status, 200);
  assert.deepEqual(await response.json(), { ok: true });
  assert.deepEqual(sent.to, ['owner@example.com']);
  assert.equal(sent.reply_to, fields.email);
  assert.ok(sent.text.includes(fields.message));
  assert.ok(sent.subject.includes('Wichelsee'));
});

test('invalid or cross-origin submissions never reach the email service', async t => {
  let calls = 0;
  t.mock.method(globalThis, 'fetch', async () => { calls++; throw new Error('Unexpected send'); });
  for (const [data, options, status] of [
    [{ ...fields, name: ' ' }, {}, 400],
    [{ ...fields, email: 'rider@example.com\nBcc: other@example.com' }, {}, 400],
    [{ ...fields, message: 'x'.repeat(3001) }, {}, 400],
    [{ ...fields, model: 'unknown' }, {}, 400],
    ['{', {}, 400],
    [fields, { headers: { Origin: 'https://other.example' } }, 403],
    [{ ...fields, website: 'spam.example' }, {}, 200],
  ]) assert.equal((await onRequest(context(data, options))).status, status);
  assert.equal(calls, 0);
});

test('HTML enquiries display visitor markup as text and preserve message line breaks', async t => {
  let sent;
  t.mock.method(globalThis, 'fetch', async (_url, options) => {
    sent = JSON.parse(options.body);
    return Response.json({ id: 'accepted-message' });
  });
  const data = { ...fields, name: '<img src=x onerror=alert(1)>', message: 'Size <54> & "custom"\n<script>alert(1)</script>' };
  assert.equal((await onRequest(context(data))).status, 200);
  assert.ok(sent.html.includes('&lt;img src=x onerror=alert(1)&gt;'));
  assert.ok(sent.html.includes('Size &lt;54&gt; &amp; &quot;custom&quot;<br>&lt;script&gt;alert(1)&lt;/script&gt;'));
  assert.ok(!sent.html.includes('<script>'));
  assert.ok(!sent.html.includes('<img'));
  assert.ok(sent.text.includes(data.message));
});

test('provider rejection or network failure never reports successful sending', async t => {
  for (const result of ['rejected', 'network', 'missing-id']) {
    const mock = t.mock.method(globalThis, 'fetch', async () => {
      if (result === 'network') throw new Error('timeout');
      return Response.json(result === 'missing-id' ? {} : { message: 'rejected' }, { status: result === 'rejected' ? 429 : 200 });
    });
    const response = await onRequest(context());
    assert.equal(response.status, 502);
    assert.deepEqual(await response.json(), { ok: false });
    mock.mock.restore();
  }
});
