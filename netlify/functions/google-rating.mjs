// Live Google rating + review count for the website.
// The API key lives ONLY in Netlify (Site configuration > Environment variables):
//   GOOGLE_PLACES_API_KEY  (required, scope: Functions)
//   GOOGLE_PLACE_ID        (optional; if missing we look the business up by name)
// Never put the key in this repo - the repo is public.
// Netlify's CDN caches the answer for 24 hours, so Google is called about once a day.

const QUERY = "Deeply Rooted Mechanical, 102 E Grand River Ave, Brighton, MI 48116";

export default async () => {
  const key = process.env.GOOGLE_PLACES_API_KEY;
  if (!key) return json({ error: "not configured" }, 503, 300);
  const placeId = process.env.GOOGLE_PLACE_ID;
  try {
    let place;
    if (placeId) {
      const r = await fetch(`https://places.googleapis.com/v1/places/${encodeURIComponent(placeId)}`, {
        headers: { "X-Goog-Api-Key": key, "X-Goog-FieldMask": "id,displayName,rating,userRatingCount" },
      });
      if (!r.ok) throw new Error(`details ${r.status}`);
      place = await r.json();
    } else {
      const r = await fetch("https://places.googleapis.com/v1/places:searchText", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Goog-Api-Key": key,
          "X-Goog-FieldMask": "places.id,places.displayName,places.rating,places.userRatingCount",
        },
        body: JSON.stringify({ textQuery: QUERY, maxResultCount: 3 }),
      });
      if (!r.ok) throw new Error(`search ${r.status}`);
      const data = await r.json();
      place = (data.places || []).find((p) => /deeply rooted/i.test(p.displayName?.text || ""));
    }
    if (!place || typeof place.userRatingCount !== "number") throw new Error("place not found");
    return json({
      rating: Number(place.rating).toFixed(1),
      count: place.userRatingCount,
      placeId: place.id,
      checked: new Date().toISOString(),
    }, 200, 86400);
  } catch (e) {
    console.error("google-rating:", e.message);
    return json({ error: "lookup failed" }, 502, 600);
  }
};

function json(body, status, cdnSeconds) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "public, max-age=3600",
      "Netlify-CDN-Cache-Control": `public, durable, max-age=${cdnSeconds}, stale-while-revalidate=604800`,
    },
  });
}

export const config = { path: "/api/google-rating" };
