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
  var title = document.getElementById("formTitle"), sub = document.getElementById("formSub"),
      desc = document.getElementById("formDesc"), dl = document.getElementById("descLabel");
  var copy = {
    "Service call": ["For no heat, no cooling or anything urgent, call (810) 360-9664 and press 1, any hour.", "What's going on?", "For example: rooftop unit 2 is blowing warm air"],
    "Free Equipment Assessment": ["We walk your equipment and send a written condition report for every unit. No cost and no obligation.", "Tell us about your building", "For example: one-story office, 4 rooftop units, a few are 15+ years old"],
    "Quote": ["Tell us about the project. Attach drawings or photos if you have them, and we will follow up with questions or a price.", "Describe the project", "For example: replace two 10-ton rooftop units, or a 6,000 SF office build-out"],
    "Maintenance / tune-up": ["We schedule the visits so you never have to remember.", "What equipment do you have?", "For example: furnace and central air, or 6 rooftop units"]
  };
  function sync() {
    var t = f.querySelector('input[name="request_type"]:checked');
    var p = f.querySelector('input[name="property_type"]:checked');
    var tv = t ? t.value : "", pv = p ? p.value : "";
    f.classList.toggle("show-plans", tv === "Quote" || tv === "Free Equipment Assessment");
    f.classList.toggle("show-commercial", pv === "Commercial");
    if (title && titles[tv]) title.textContent = titles[tv];
    var al = document.getElementById("addrLabel"), st = document.getElementById("submitText");
    if (al) al.textContent = (tv === "Quote" || tv === "Free Equipment Assessment") ? "Project or building address" : "Service address";
    if (st) st.textContent = tv === "Quote" ? "Send project details" : tv === "Free Equipment Assessment" ? "Book my assessment" : "Send request";
    if (copy[tv]) { if (sub) sub.textContent = copy[tv][0]; if (dl) dl.textContent = copy[tv][1]; if (desc) desc.placeholder = copy[tv][2]; }
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
  var hero = document.querySelector(".page-hero");
  var heroImg = { "Quote": "rtu-crane.jpg", "Free Equipment Assessment": "exhaust-fan.jpg" };
  var _sync = sync;
  sync = function () {
    _sync();
    var c = f.querySelector('input[name="request_type"]:checked');
    if (hero) hero.style.setProperty("--hero", "url('/assets/img/" + ((c && heroImg[c.value]) || "service-tech.jpg") + "')");
  };
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
