document.documentElement.classList.add("js");

// Phone menu
(function () {
  var btn = document.querySelector(".menu-btn"), nav = document.getElementById("mainnav");
  if (!btn || !nav) return;
  btn.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  });
})();

// Request form: pre-select from ?type=, show only the fields that apply, retitle the page
(function () {
  var f = document.querySelector('form[name="service-request"]');
  if (!f) return;
  var map = { service: "Service call", assessment: "Free Equipment Assessment", quote: "Quote", maintenance: "Maintenance / tune-up" };
  var titles = { "Service call": "Request service", "Free Equipment Assessment": "Book a Free Equipment Assessment",
                 "Quote": "Request a quote", "Maintenance / tune-up": "Maintenance and tune-ups" };
  var title = document.getElementById("formTitle");
  function sync() {
    var t = f.querySelector('input[name="request_type"]:checked');
    var p = f.querySelector('input[name="property_type"]:checked');
    var tv = t ? t.value : "", pv = p ? p.value : "";
    f.classList.toggle("show-plans", tv === "Quote" || tv === "Free Equipment Assessment");
    f.classList.toggle("show-commercial", pv === "Commercial");
    if (title && titles[tv]) title.textContent = titles[tv];
  }
  var t = new URLSearchParams(location.search).get("type");
  if (t && map[t]) {
    var r = f.querySelector('input[name="request_type"][value="' + map[t] + '"]');
    if (r) r.checked = true;
    if (t === "assessment") {
      var c = f.querySelector('input[name="property_type"][value="Commercial"]');
      if (c) c.checked = true;
    }
  }
  f.addEventListener("change", sync);
  sync();
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
  }).catch(function () {});
})();
