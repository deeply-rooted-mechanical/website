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
