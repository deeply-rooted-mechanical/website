// Netlify runs this automatically for every VERIFIED form submission (spam is filtered out before it runs).
// It forwards the "service-request" form to Rooted (crm.deeplyrootedhvac.com/api/webform), where it becomes a service call,
// quote request, maintenance call or assessment for Chase. Rooted texts Chase and posts to Teams.
// Needs env var WEBFORM_KEY (set by Matt in Netlify, Production only - never in this public repo). With no key it does nothing,
// so deploy previews never send anything to Rooted. The Netlify email to Service@ still goes out either way.
const ROOTED = process.env.ROOTED_WEBFORM_URL || "https://crm.deeplyrootedhvac.com/api/webform";

export default async (req) => {
  let body;
  try { body = await req.json(); } catch (e) { return new Response("bad body", { status: 400 }); }
  const p = (body && body.payload) || {};
  if (p.form_name !== "service-request") return new Response("not forwarded (other form)");
  const key = process.env.WEBFORM_KEY;
  if (!key) { console.log("WEBFORM_KEY not set - submission not sent to Rooted"); return new Response("no key"); }
  const d = p.data || {};
  const file = d.attachment;
  const attachment_url = typeof file === "string" ? file : (file && file.url) || "";
  const out = {
    submissionId: p.id || "", request_type: d.request_type, property_type: d.property_type, description: d.description,
    first_name: d.first_name, last_name: d.last_name, phone: d.phone, email: d.email, company: d.company,
    street: d.street, city: d.city, zip: d.zip, urgency: d.urgency, preferred_day: d.preferred_day, preferred_time: d.preferred_time,
    preferred_contact: d.preferred_contact, sms_consent_service: d.sms_consent_service, sms_consent_marketing: d.sms_consent_marketing,
    attachment_url, source: d.source || "Website",
  };
  // one retry - a lost request means a missed customer
  for (let i = 0; i < 2; i++) {
    try {
      const r = await fetch(ROOTED, { method: "POST", headers: { "content-type": "application/json", "x-webform-key": key }, body: JSON.stringify(out) });
      const t = await r.text();
      console.log("Rooted answered", r.status, t.slice(0, 300));
      if (r.ok) return new Response("sent");
    } catch (e) { console.log("Rooted not reached:", String(e)); }
    await new Promise(res => setTimeout(res, 1500));
  }
  return new Response("Rooted did not accept it - the Service@ email still has the request", { status: 502 });
};
