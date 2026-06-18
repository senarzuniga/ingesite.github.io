// Netlify serverless function to send email notifications for video events.
// Uses SendGrid if SENDGRID_API_KEY is provided. Otherwise returns 204.

exports.handler = async function(event, context) {
  if (event.httpMethod !== 'POST') return { statusCode: 405, body: 'Method not allowed' };
  let payload = {};
  try { payload = JSON.parse(event.body || '{}'); } catch(e) { }

  const action = payload.action || payload.event || 'unknown';
  const file = payload.file || payload.filename || '';
  const ts = payload.timestamp || new Date().toISOString();

  const subject = `Video ${action} — ${file.split('/').pop()}`;
  const bodyText = `Action: ${action}\nFile: ${file}\nTime: ${ts}\nUser-Agent: ${event.headers['user-agent'] || ''}`;

  const SENDGRID_API_KEY = process.env.SENDGRID_API_KEY;
  const EMAIL_TO = process.env.EMAIL_TO || 'cgo@ingecart.es';
  const EMAIL_FROM = process.env.EMAIL_FROM || 'noreply@ingecart.es';

  if (SENDGRID_API_KEY) {
    try {
      const res = await fetch('https://api.sendgrid.com/v3/mail/send', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${SENDGRID_API_KEY}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          personalizations: [{ to: [{ email: EMAIL_TO }] }],
          from: { email: EMAIL_FROM },
          subject: subject,
          content: [{ type: 'text/plain', value: bodyText }]
        })
      });
      if (!res.ok) {
        const txt = await res.text();
        return { statusCode: 502, body: `SendGrid error: ${txt}` };
      }
      return { statusCode: 200, body: JSON.stringify({ ok: true }) };
    } catch (e) {
      return { statusCode: 500, body: String(e) };
    }
  }

  // If no provider configured, return 204 so client falls back to local server
  return { statusCode: 204, body: '' };
}
