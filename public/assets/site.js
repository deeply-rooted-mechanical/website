// Pre-selects the request type on /contact from ?type=service|assessment|quote
(function () {
  var f = document.querySelector('form[name="service-request"]');
  if (!f) return;
  var map = { service: "Service call", assessment: "Free Equipment Assessment", quote: "Quote", maintenance: "Maintenance / tune-up" };
  var t = new URLSearchParams(location.search).get("type");
  if (t && map[t]) {
    var r = f.querySelector('input[name="request_type"][value="' + map[t] + '"]');
    if (r) r.checked = true;
    if (t === "assessment") {
      var c = f.querySelector('input[name="property_type"][value="Commercial"]');
      if (c) c.checked = true;
    }
  }
})();

// Live Google rating + review count (Netlify function, cached daily).
// The numbers typed into the page stay as the fallback if the lookup fails.
(function () {
  var els = document.querySelectorAll("[data-g]");
  if (!els.length || !window.fetch) return;
  fetch("/api/google-rating").then(function (r) { return r.ok ? r.json() : null; }).then(function (d) {
    if (!d || !d.count) return;
    els.forEach(function (el) {
      var v = el.getAttribute("data-g") === "count" ? d.count : d.rating;
      if (v) el.textContent = v;
    });
    document.querySelectorAll('a[aria-label*="Google reviews"]').forEach(function (a) {
      a.setAttribute("aria-label", "Read our " + d.count + " Google reviews");
    });
  }).catch(function () {});
})();
