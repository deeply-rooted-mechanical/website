#!/usr/bin/env python3
"""Builds the deeplyrootedhvac.com static site into ./public.

Edit content below, run `python3 build.py`, commit build.py + public/.
Netlify publishes public/ as-is on every push to main (no build step on Netlify).
This repo is PUBLIC: never put keys, passwords or business notes in it.
"""
import json, os, shutil, html, hashlib
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "public")
SITE = "https://deeplyrootedhvac.com"

NAME = "Deeply Rooted Mechanical"
LEGAL = "Deeply Rooted Mechanical LLC"
PHONE = "(810) 360-9664"
TEL = "+18103609664"
EMAIL = "Service@DeeplyRootedHVAC.com"
STREET = "102 E. Grand River Ave."
CITY, STATE, ZIP = "Brighton", "MI", "48116"
AREA = "all of Southeast Michigan"
LICENSE = "7118932"   # Michigan Mechanical Contractor License (exp. 08/31/2027)
FACEBOOK = "https://www.facebook.com/profile.php?id=61579592821615"
LINKEDIN = "https://www.linkedin.com/company/deeply-rooted-mechanical"
GOOGLE_PROFILE = "https://www.google.com/maps?cid=12884188372933293353"
GOOGLE_REVIEW = "https://g.page/r/CSk16NMP1c2yEAE/review"
GOOGLE_RATING = "5.0"
GOOGLE_COUNT = 95          # update when the count moves (checked 11/16/2026)
SLOGAN = "Rooted in Faith. Built on Trust. Thankful in All."
SLOGAN_HTML = "<span>Rooted in Faith.</span> <span>Built on Trust.</span> <span>Thankful in All.</span>"
VERSE = "Rooted and built up in Him, established in the faith, overflowing with thankfulness."
VERSE_REF = "Colossians 2:7"
# Bill Purcell tribute video on YouTube: "In Memory of Bill Purcell - Deeply Rooted Mechanical"
TRIBUTE_YOUTUBE = "7POdWOwnGcc"

e = html.escape


def ver(name):
    """Short content hash so browsers fetch new CSS/JS the moment it changes."""
    with open(os.path.join(ROOT, "assets", name), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]

# ---------- icons (simple line icons, currentColor) ----------
def icon(name, size=28):
    p = {
        "wrench": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3 17.8V21h3.2l6.3-6.3a4 4 0 0 0 5.2-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
        "clipboard": '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4h6v3H9z"/><path d="M8.5 13l2.2 2.2L15.5 10.5"/>',
        "building": '<path d="M4 21V5l8-3v19M12 9h8v12M7 8h2M7 12h2M7 16h2M15 13h2M15 17h2M2 21h20"/>',
        "duct": '<path d="M3 8h11a4 4 0 0 1 4 4v9M3 13h8a2 2 0 0 1 2 2v6M21 21h-6"/>',
        "flame": '<path d="M12 22c4 0 7-3 7-7 0-4-3-6-4-9-1 3-3 4-4 4 0-3-1-5-3-7 0 5-5 7-5 12 0 4 3 7 9 7z"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "snow": '<path d="M12 2v20M4 6l16 12M20 6L4 18M9 3l3 3 3-3M9 21l3-3 3 3"/>',
        "fan": '<circle cx="12" cy="12" r="2"/><path d="M12 10c0-4 1-7 4-7s2 5-2 7M14 12c4 0 7 1 7 4s-5 2-7-2M12 14c0 4-1 7-4 7s-2-5 2-7M10 12c-4 0-7-1-7-4s5-2 7 2"/>',
        "home": '<path d="M3 11l9-8 9 8M5 10v11h14V10M10 21v-6h4v6"/>',
        "thermo": '<path d="M14 14.8V5a2 2 0 0 0-4 0v9.8a4 4 0 1 0 4 0z"/><path d="M12 9v7"/>',
        "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4M8.5 15l2.2 2.2 4.8-4.7"/>',
        "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
        "percent": '<path d="M19 5L5 19"/><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="17" r="2.5"/>',
        "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
        "book": '<path d="M2 5h7a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H2zM22 5h-7a3 3 0 0 0-3 3v13a2 2 0 0 1 2-2h8z"/>',
        "cross": '<path d="M12 2v20M6 8h12"/>',
        "sun": '<path d="M2 20h20M5 20l5-8 3 4 2-3 4 7"/><circle cx="17" cy="6" r="2.5"/>',
        "heart": '<path d="M12 21s-8-5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 6-8 11-8 11z"/>',
        "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
        "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
        "star": '<path d="M12 2l3 6.5 7 .9-5.2 4.8 1.4 7L12 17.8 5.8 21.2l1.4-7L2 9.4l7-.9z"/>',
        "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
        "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    }[name]
    fill = "currentColor" if name == "star" else "none"
    return (f'<svg class="ic" width="{size}" height="{size}" viewBox="0 0 24 24" fill="{fill}" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>')

STARS = "".join(icon("star", 22) for _ in range(5))

PLANS = [
    ("Furnace and AC", "$495", "https://connect.intuit.com/portal/app/CommerceNetwork/view/scs-v1-d741d524baba4b41be768d5c2c191868422cca07cba14e92ac8d46c62c5ddaa0fe55ff92fabf47f3b2ccc54a9a123eab",
     "For homes with a furnace and central air conditioning.",
     ["Spring visit: your air conditioner checked and tuned before cooling season",
      "Fall visit: your furnace checked and tuned before heating season",
      "Priority scheduling when something goes wrong",
      "10% off parts and labor, plus reduced emergency visit premiums"]),
    ("Ductless Mini Split", "$295", "https://connect.intuit.com/portal/app/CommerceNetwork/view/scs-v1-77f76ac06b3a4b2fa6e25d38d558ec6f4161a28fa0c14a04b7bd1b167e8acaaed6dea995f78e476bbd780709297c07e6",
     "For homes heated and cooled by a ductless mini split.",
     ["Spring and fall visits to clean, check and tune your system",
      "Heating and cooling performance checked each season",
      "Priority scheduling when something goes wrong",
      "10% off parts and labor, plus reduced emergency visit premiums"]),
    ("Boiler", "$595", "https://connect.intuit.com/portal/app/CommerceNetwork/view/scs-v1-0bbab20d75cb4d25ac2c239e2003df9715a0741281614daf9bcada283a668c5d38213cd1c0f44802a84d909006a2a524",
     "For homes with boiler or radiant heat.",
     ["Two visits a year to check and tune your boiler",
      "Safety and performance checked before heating season",
      "Priority scheduling when something goes wrong",
      "10% off parts and labor, plus reduced emergency visit premiums"]),
]

TEAM = [("matt", "Matt Pastor", "Owner"), ("ken", "Ken Crider", "Superintendent"),
        ("chase", "Chase Fackler", "Service Manager"), ("don", "Don Sleep", "Service Technician"),
        ("james", "James Gore", "HVAC Installer"), ("nick", "Nick Mooney", "HVAC Installer")]

VALUES = [
    ("book", "A Teachable Spirit", "We never stop learning. We take joy in applying what we have learned and growing from what is next."),
    ("cross", "Faith", "We hold everything with open hands, trusting the One who holds tomorrow."),
    ("shield", "The Hard Right", "Integrity matters, even when no one is watching. We choose the hard right over the easy wrong."),
    ("sun", "The Bigger Picture", "Work is a gift, not our first priority. We strive for excellence but keep life and purpose in proper focus."),
    ("heart", "Servant-Leadership", "We lead by serving first, with humility, responsiveness and a can-do attitude toward our customers and our team."),
]


# kind: "c" = commercial customer, "r" = homeowner
REVIEWS = {
    "joe": ("Joe Legato", "Rooftop units", "c", "Deeply Rooted Mechanical has been fantastic to work with. I have had them replace one rooftop unit and repair two rooftop units. In both instances they were thorough, considerate of our property, considerate of our employees, and provided expert level of professionalism at every step of the process. The next time I am in need, Matt and his team will be my first call."),
    "andrew": ("Andrew Beach", "Office furnace", "c", "We called Deeply Rooted Mechanical the morning our furnace went out at our office. They were out same day to fix our furnace! Chase was super kind and personable as well as efficient. I highly recommend this company for all of your HVAC needs!"),
    "anthony": ("Anthony Progar", "Boiler repair", "r", "After our hydro-static boiler that provides radiant heat and hot water stopped working, we called Deeply Rooted Mechanical. We're extremely satisfied with the service. Chase showed up on time and listened as I explained the issue. He took his time looking things over and found a bad part which he replaced. The cost was very reasonable."),
    "steven": ("Steven Finlayson", "Furnace, AC and thermostat", "r", "We needed the works, new A/C condenser, new furnace, new thermostat, you name it, and we were very pleased not only with the upgrade in equipment, but with the service provided. Matt and his crew were polite, respectful of our time, and very professional."),
    "kathy": ("Kathy Flowers", "Heating repair", "r", "Chase and Deeply Rooted Mechanical helped me solve my complicated issues regarding my furnace problems and heat distribution throughout my home. He communicated well, with integrity and respect, and worked to address the issue in a way that was least expensive. Highly recommend them!"),
    "laura": ("Laura C", "Service call", "r", "Excellent service! Very prompt and professional! We called on a Monday afternoon and had a technician at our home by Tuesday afternoon to fix our system. They even talked me through how to turn off the water to my leaking humidifier via text Monday night."),
    "madeline": ("Madeline Dunn", "Furnace and ductwork", "r", "They fixed an overheating problem without adding extra lines and looked at the bigger picture. They were professional, took their shoes off, and even made sure my furnace didn't overheat. I interviewed three HVAC companies and definitely made the right choice. They treated us like family and offered a fair price."),
    "corey": ("Corey De Luca", "Service call", "r", "The owner Matt is hands down one of the nicest business owners I've interacted with. He listened to my concerns and explained everything thoroughly. The technician was extremely kind, knowledgeable and honest. I highly recommend them!"),
}

# Featured projects (Matt 11/16: names OK; only projects with real photos and confirmed facts).
PROJECTS = [
    ("library-crane.jpg", "building", "Springfield Township Library", "90-ton rooftop unit and heating and ventilating replacement, contracted direct with the township. Our largest project to date.", ["Rooftop units", "Owner direct", "Completed 2026"]),
    ("arbon-buildout.jpg", "duct", "Arbon Equipment", "9,000 SF office build-out. Design-build HVAC and ductwork with Schafer Construction.", ["Design-build", "Completed 2024"]),
    ("retail-rtu.jpg", "building", "Frames &amp; More", "Rooftop unit replacement: crane lift, setting and startup on an occupied retail building.", ["Rooftop units", "Retail"]),
]

MORE_WORK = [
    ("Agape Church", "20,000 SF new building, design-build", "In progress"),
    ("Puckmasters Ice Rink", "11,000 SF new building, design-build", "In progress"),
    ("Levin Courthouse", "HVAC in an occupied federal building", "2026"),
    ("Straits Corporation", "Rooftop unit replacements, owner direct", "2026"),
    ("Signarama Wixom", "Building HVAC", "2026"),
    ("Mt. Clemens Montessori Academy", "HVAC upgrades", "2026"),
    ("Oakpointe Church Milford", "10,000 SF addition", "2025"),
    ("Target Hartland", "Store remodel", "2025"),
    ("Hosel Rockets", "8,000 SF remodel", "2025"),
    ("Yudo", "4,500 SF office addition and shop renovation, design-build", "2025"),
]

CITIES = [
    ("Livingston County", ["Brighton", "Howell", "Hartland", "Pinckney", "Fowlerville"]),
    ("Oakland County", ["Novi", "Milford", "Highland", "Wixom", "Commerce", "Farmington Hills", "Troy"]),
    ("Genesee County", ["Fenton", "Linden", "Grand Blanc", "Flint"]),
    ("Wayne County", ["Livonia", "Northville", "Plymouth", "Canton", "Detroit"]),
]

TRUST = [
    ("shield", "Licensed and insured", f"MI Mechanical Contractor #{LICENSE}"),
    ("building", "90+ projects completed", "Established 2024"),
    ("check", "1-year workmanship guarantee", "Plus manufacturer warranties"),
    ("clock", "24/7 emergency service", f"Call {PHONE}, press 1"),
]

NAV = [("/", "Home", None),
       ("/commercial", "Commercial", [("/commercial", "Commercial HVAC"), ("/rtu-replacement", "Rooftop unit replacement"),
                                      ("/design-build", "Design-build and general contractors"), ("/projects", "Featured projects")]),
       ("/residential", "Residential", None),
       ("/commercial-maintenance", "Maintenance", [("/commercial-maintenance", "Commercial maintenance agreements"),
                                                    ("/rooted-assurance-program", "Home maintenance plans")]),
       ("/about-us", "About", None),
       ("/contact", "Contact", None)]


def schema():
    cities = [c for _, cs in CITIES for c in cs]
    return {
        "@context": "https://schema.org", "@type": "HVACBusiness", "@id": SITE + "/#business",
        "name": NAME, "legalName": LEGAL, "url": SITE + "/",
        "logo": SITE + "/assets/logo.png", "image": SITE + "/assets/img/rtu-crane.jpg",
        "telephone": PHONE, "email": EMAIL, "foundingDate": "2024",
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY,
                    "addressRegion": STATE, "postalCode": ZIP, "addressCountry": "US"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                       "opens": "07:00", "closes": "16:30"}],
        "areaServed": [{"@type": "AdministrativeArea", "name": n} for n in
                       ["Southeast Michigan"] + [c + ", MI" for c, _ in CITIES]] +
                      [{"@type": "City", "name": c + ", MI"} for c in cities],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": GOOGLE_RATING, "reviewCount": GOOGLE_COUNT},
        "knowsAbout": ["Commercial HVAC", "Rooftop unit (RTU) replacement", "Commercial HVAC maintenance agreements",
                       "Design-build HVAC", "Tenant build-out HVAC", "Sheet metal ductwork", "Boiler service",
                       "Ductless mini split systems", "Furnace repair", "Air conditioning repair"],
        "hasMap": GOOGLE_PROFILE, "slogan": SLOGAN, "sameAs": [FACEBOOK, LINKEDIN, GOOGLE_PROFILE],
    }


def service_schema(name, desc, path):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "description": desc,
            "serviceType": name, "url": SITE + path, "provider": {"@id": SITE + "/#business"},
            "areaServed": {"@type": "AdministrativeArea", "name": "Southeast Michigan"}}


def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def head(title, desc, path, extra):
    blocks = "".join(f'<script type="application/ld+json">{json.dumps(s)}</script>' for s in [schema()] + extra)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/assets/img/rtu-crane.jpg">
<meta name="theme-color" content="#14263d">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="stylesheet" href="/assets/style.css?v={ver('style.css')}">
{blocks}
</head>
<body>
"""


def header(path):
    items = []
    for h, t, sub in NAV:
        cur = ' aria-current="page"' if (h == path or (sub and any(s == path for s, _ in sub))) else ""
        if sub:
            subs = "".join(f'<a href="{s}"{" aria-current=\"page\"" if s == path else ""}>{st}</a>' for s, st in sub)
            items.append(f'<div class="has-sub"><a href="{h}"{cur}>{t} <span class="caret" aria-hidden="true"></span></a><div class="sub">{subs}</div></div>')
        else:
            items.append(f'<a href="{h}"{cur}>{t}</a>')
    return f"""<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
<span class="slogan-mini">Licensed and insured &middot; Serving all of Southeast Michigan</span>
<a href="tel:{TEL}">{icon("phone", 16)} {PHONE} &middot; Emergency service 24/7</a>
</div></div>
<header class="site"><div class="wrap">
<a class="brand" href="/"><img src="/assets/logo-sm.png" alt="{NAME} logo" width="56" height="56"><span class="brand-name"><b>Deeply Rooted</b><b>Mechanical</b></span></a>
<nav id="mainnav" aria-label="Main">{"".join(items)}</nav>
<a class="btn btn-navy hdr-cta" href="/contact?type=service">Request Service</a>
<a class="icon-btn hdr-call" href="tel:{TEL}" aria-label="Call {PHONE}">{icon("phone", 22)}</a>
<button class="icon-btn menu-btn" type="button" aria-controls="mainnav" aria-expanded="false" aria-label="Menu">{icon("menu", 24)}</button>
</div></header>
<main id="main">
"""


def footer():
    return f"""</main>
<section class="verse"><div class="wrap">
<p class="slogan-big">{SLOGAN_HTML}</p>
<p class="verse-text">"{VERSE}" <span>{VERSE_REF}</span></p>
</div></section>
<footer class="site"><div class="wrap cols">
<div>
<img src="/assets/logo-sm.png" alt="" width="72" height="72">
<p><strong>{NAME}</strong><br>{STREET}<br>{CITY}, {STATE} {ZIP}</p>
<p class="small">Michigan Mechanical Contractor License #{LICENSE}<br>Licensed and insured. Established 2024.</p>
</div>
<div>
<h3>Contact</h3>
<ul class="flinks"><li><a href="tel:{TEL}">{PHONE}</a> (press 1 for service)</li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul>
<p>Office: Mon to Fri, 7:00 AM to 4:30 PM<br>Emergency service 24/7</p>
</div>
<div>
<h3>Services</h3>
<ul class="flinks"><li><a href="/commercial">Commercial HVAC</a></li><li><a href="/rtu-replacement">Rooftop unit replacement</a></li><li><a href="/commercial-maintenance">Commercial maintenance</a></li><li><a href="/design-build">Design-build and GCs</a></li><li><a href="/residential">Residential HVAC</a></li><li><a href="/rooted-assurance-program">Home maintenance plans</a></li></ul>
</div>
<div>
<h3>Reviews and social</h3>
<ul class="flinks"><li><a href="{GOOGLE_PROFILE}" rel="noopener"><span data-g="rating">{GOOGLE_RATING}</span> stars, <span data-g="count">{GOOGLE_COUNT}</span> Google reviews</a></li><li><a href="{GOOGLE_REVIEW}" rel="noopener">Leave us a Google review</a></li><li><a href="{FACEBOOK}" rel="noopener">Facebook</a></li><li><a href="{LINKEDIN}" rel="noopener">LinkedIn</a></li><li><a href="/projects">Featured projects</a></li></ul>
</div>
</div>
<div class="wrap legal"><p>&copy; 2026 {LEGAL}. Heating and cooling for businesses and homes across {AREA}.</p>
<p><a href="/privacy-policy">Privacy Policy</a> &middot; <a href="/terms-of-service">Terms of Service</a></p></div>
</footer>
<div class="mbar"><a href="tel:{TEL}">{icon("phone", 20)} Call</a><a class="mbar-main" href="/contact?type=service">{icon("wrench", 20)} Request Service</a></div>
<script src="/assets/site.js?v={ver('site.js')}" defer></script>
</body>
</html>
"""


def page(path, title, desc, body, extra=()):
    return head(title, desc, path, list(extra)) + header(path) + body + footer()


def img(name, alt, cls="", lazy=True):
    w, h = Image.open(os.path.join(ROOT, "assets", "img", name)).size
    return (f'<img src="/assets/img/{name}" alt="{e(alt)}" width="{w}" height="{h}"'
            f'{" loading=\"lazy\"" if lazy else ""}{f" class=\"{cls}\"" if cls else ""}>')


def buttons(dark=True, kind="all"):
    """The calls to action, always in Matt's order: service, assessment, quote."""
    pri = "btn-white" if dark else "btn-navy"
    sec = "btn-outline on-dark" if dark else "btn-outline"
    out = ['<div class="cta-row">',
           f'<a class="btn {pri}" href="/contact?type=service">{icon("wrench", 20)} Request Service</a>']
    if kind == "gc":     # general contractors: quote first
        return (f'<div class="cta-row"><a class="btn {pri}" href="/contact?type=quote">{icon("clipboard", 20)} Send us your project</a>'
                f'<a class="btn btn-outline{" on-dark" if dark else ""}" href="/projects">{icon("building", 20)} Featured projects</a></div>')
    if kind == "home":   # residential pages: no commercial assessment
        out.append(f'<a class="btn {sec}" href="/contact?type=quote">{icon("clipboard", 20)} Request a Quote</a>')
        out.append(f'<a class="btn btn-outline{" on-dark" if dark else ""}" href="/rooted-assurance-program">{icon("calendar", 20)} Maintenance Plans</a>')
    else:
        out.append(f'<a class="btn {sec}" href="/contact?type=assessment">{icon("calendar", 20)} Free Equipment Assessment</a>')
        out.append(f'<a class="btn btn-outline{" on-dark" if dark else ""}" href="/contact?type=quote">{icon("clipboard", 20)} Request a Quote</a>')
    out.append('</div>')
    return "".join(out)


def cta_band(text="Let us serve you!", kind="all"):
    return f"""<section class="cta-band"><div class="wrap">
<h2>{text}</h2>
{buttons(dark=True, kind=kind)}
<p class="cta-phone">Or call <a href="tel:{TEL}">{PHONE}</a> and press 1 for service, 24/7.</p>
</div></section>
"""


def rating_badge(cls=""):
    return (f'<a class="rating {cls}" href="{GOOGLE_PROFILE}" rel="noopener" aria-label="Read our Google reviews">'
            f'<span class="stars">{STARS}</span><span class="rating-text"><b><span data-g="rating">{GOOGLE_RATING}</span></b> from <b><span data-g="count">{GOOGLE_COUNT}</span></b> Google reviews</span></a>')


def trust_strip():
    items = "".join(f'<li><span class="t-ic">{icon(ic, 26)}</span><span><b>{t}</b><small>{s}</small></span></li>' for ic, t, s in TRUST)
    star = (f'<li><span class="t-ic gold">{icon("star", 26)}</span><span><b><span data-g="rating">{GOOGLE_RATING}</span> stars on Google</b>'
            f'<small><span data-g="count">{GOOGLE_COUNT}</span> reviews</small></span></li>')
    return f'<section class="trust" aria-label="Why customers trust us"><div class="wrap"><ul>{items}{star}</ul></div></section>'


def reviews_block(keys, title=None):
    cards = "".join(
        f'<figure class="review"><div class="stars small">{"".join(icon("star", 18) for _ in range(5))}</div>'
        f'<blockquote>{e(t)}</blockquote><figcaption><span class="avatar">{e(n[0])}</span><span><b>{e(n)}</b>'
        f'<small>{e(kind)} &middot; Google review</small></span></figcaption></figure>'
        for n, kind, _, t in (REVIEWS[k] for k in keys))
    return f"""<section class="reviews"><div class="wrap">
<div class="reviews-head">
<div><h2>{title or f'Rated <span data-g="rating">{GOOGLE_RATING}</span> stars on <span data-g="count">{GOOGLE_COUNT}</span> Google reviews'}</h2>
<p>Real reviews from our customers on Google.</p></div>
<div class="score"><span class="score-num"><span data-g="rating">{GOOGLE_RATING}</span></span><span class="stars">{STARS}</span><span><span data-g="count">{GOOGLE_COUNT}</span> Google reviews</span></div>
</div>
<div class="review-grid n{len(keys)}">{cards}</div>
<div class="center btn-pair"><a class="btn btn-navy" href="{GOOGLE_PROFILE}" rel="noopener"><span>Read all <span data-g="count">{GOOGLE_COUNT}</span> reviews on Google</span></a>
<a class="btn btn-outline" href="{GOOGLE_REVIEW}" rel="noopener">Leave us a review</a></div>
</div></section>
"""


def team_block():
    cards = "".join(
        f'<figure class="person"><img src="/assets/team/{k}.jpg" alt="{e(n)}, {e(t)}" width="400" height="400" loading="lazy">'
        f'<figcaption><strong>{e(n)}</strong><span>{e(t)}</span></figcaption></figure>'
        for k, n, t in TEAM)
    return f"""<section class="team"><div class="wrap">
<div class="section-head center"><h2>Meet the team</h2><p>Local people you will see on your roof and in your mechanical room.</p></div>
<div class="team-grid">{cards}</div>
</div></section>
"""


def values_block(title="Our core values", intro="Everything we do grows out of five roots.", tone=""):
    items = "".join(
        f'<li><span class="v-ic">{icon(ic, 28)}</span><span class="v-pre">Deeply Rooted in</span>'
        f'<span class="v-name">{e(t)}</span><p>{e(d)}</p></li>' for ic, t, d in VALUES)
    return f"""<section class="values {tone}"><div class="wrap">
<div class="section-head center"><h2>{title}</h2><p>{intro}</p></div>
<ul class="value-list">{items}</ul>
</div></section>
"""


def photo_cards(cards):
    out = []
    for im, alt, ic, t, d, link in cards:
        inner = (f'{img(im, alt)}<div><span class="pc-ic">{icon(ic, 22)}</span><h3>{e(t)}</h3><p>{e(d)}</p>'
                 + (f'<span class="more">Learn more {icon("arrow", 16)}</span>' if link else "") + '</div>')
        out.append(f'<li>{f"<a href=\"{link}\">{inner}</a>" if link else inner}</li>')
    return '<ul class="photo-cards">' + "".join(out) + '</ul>'


def icon_cards(cards, cols=3):
    return f'<ul class="icon-cards c{cols}">' + "".join(
        f'<li><span class="ic-wrap">{icon(ic, 26)}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for ic, t, d in cards) + '</ul>'


def project_cards(items):
    out = []
    for im, ic, t, d, tags in items:
        top = img(im, f"{html.unescape(t)} project by {NAME}") if im else f'<div class="proj-ph">{icon(ic, 40)}</div>'
        tg = "".join(f"<span>{e(x)}</span>" for x in tags)
        out.append(f'<li>{top}<div><h3>{t}</h3><p>{e(d)}</p><p class="tags">{tg}</p></div></li>')
    return '<ul class="projects">' + "".join(out) + '</ul>'


def projects_section(n=None, head_txt="Featured projects", link=True, skip_first=False):
    items = PROJECTS[:n] if n else PROJECTS
    if skip_first:
        items = items[1:]
    more = '<div class="center"><a class="btn btn-outline" href="/projects">See the project video and more</a></div>' if link else ""
    return f"""<section class="proj-sec"><div class="wrap">
<div class="section-head center"><h2>{head_txt}</h2><p>A few of the commercial jobs our crews have completed across Southeast Michigan.</p></div>
{project_cards(items)}
{more}
</div></section>
"""


def steps(items):
    return '<ol class="steps">' + "".join(f'<li><span class="n">{i}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>'
                                          for i, (t, d) in enumerate(items, 1)) + '</ol>'


TRUSTED = ["Springfield Township", "Levin Courthouse", "Target", "Schafer Construction", "Woods Construction", "McKenzie Construction", "Straits Corporation", "Arbon Equipment"]


def trusted_by():
    items = "".join(f"<li>{e(t)}</li>" for t in TRUSTED)
    return f'<section class="trusted"><div class="wrap"><p class="tb-h">Trusted by owners and general contractors including</p><ul>{items}</ul></div></section>'


def where_we_work():
    cols = "".join(f'<div><h3>{c}</h3><p>{", ".join(cs)}</p></div>' for c, cs in CITIES)
    return f"""<section class="where"><div class="wrap">
<div class="section-head center"><h2>Where we work</h2><p>Based in Brighton, serving businesses and homes across all of Southeast Michigan, including:</p></div>
<div class="where-grid">{cols}</div>
</div></section>
"""


def faq_html(faqs):
    return "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs)


# ---------------- pages ----------------
HOME = f"""<section class="hero" style="--hero:url('/assets/img/rtu-crane.jpg')"><div class="wrap">
<div class="hero-copy">
<img class="hero-logo" src="/assets/logo-sm.png" alt="{NAME} logo" width="132" height="132">
<p class="hero-slogan">{SLOGAN_HTML}</p>
<h1>Commercial HVAC you can count on, across Southeast Michigan.</h1>
<p>Rooftop unit repair and replacement, maintenance agreements, design-build and tenant build-outs, and 24/7 emergency service for building owners, property managers and general contractors. Homeowners too.</p>
{buttons(dark=True)}
{rating_badge("on-dark")}
</div>
</div></section>
{trust_strip()}

<section class="video-feature"><div class="wrap video-inner">
<div class="video-frame"><video controls preload="none" playsinline poster="/assets/video/springfield-poster.jpg" src="/assets/video/springfield-rtu-replacement.mp4" aria-label="Rooftop unit replacement job tour at Springfield Township Library"></video></div>
<div>
<h2>See us at work</h2>
<p>A 90-ton rooftop unit replacement at Springfield Township Library: old units out, new units lifted by crane, set and started up by our crew.</p>
<a class="btn btn-white" href="/rtu-replacement">{icon("building", 20)} Rooftop unit replacement</a>
</div>
</div></section>

<section class="paths"><div class="wrap">
<a class="path" href="/commercial">{img("rtu-new.jpg", "Crew setting new rooftop units")}<div><h2>For your business</h2><p>RTUs, make-up air and exhaust, boilers, VRF and ductless, ductwork and preventive maintenance agreements. Built for uptime.</p><span class="more">Commercial HVAC {icon("arrow", 18)}</span></div></a>
<a class="path" href="/residential">{img("furnace.jpg", "New furnace installed by Deeply Rooted Mechanical")}<div><h2>For your home</h2><p>Furnace, air conditioning, boiler and mini split repair and replacement, plus our Rooted Assurance maintenance plans.</p><span class="more">Residential HVAC {icon("arrow", 18)}</span></div></a>
</div></section>

<section class="services"><div class="wrap">
<div class="section-head center"><h2>What we do</h2><p>Heating and cooling, done right the first time.</p></div>
{photo_cards([
    ("rtu-set.jpg", "Crew setting a new rooftop unit on its curb", "building", "Rooftop unit repair and replacement", "Diagnosis, repair and full RTU changeouts, including crane lifts, curbs and startup.", "/rtu-replacement"),
    ("service-tech.jpg", "Technicians working inside a rooftop unit", "clipboard", "Maintenance agreements", "Scheduled visits with filters included, priority scheduling, 10% off repairs and a written report after every visit.", "/commercial-maintenance"),
    ("buildout.jpg", "Crew installing spiral duct on a tenant build-out", "wrench", "Design-build and build-outs", "Mechanical partner for general contractors on new construction and tenant build-outs, from planning to closeout.", "/design-build"),
    ("ductwork.jpg", "Installer connecting ductwork", "duct", "Ductwork and sheet metal", "Rectangular and spiral duct, exhaust and make-up air, installed clean and on schedule.", None),
    ("furnace-2.jpg", "Furnace installation", "flame", "Heating and boilers", "Furnace and boiler repair and replacement, plus CSD-1 testing for commercial boilers.", None),
    ("safety-vest.jpg", "Deeply Rooted Mechanical crew member", "clock", "24/7 emergency service", "No heat, no cooling, or a unit down on a busy day. Call (810) 360-9664 and press 1, any hour.", None),
])}
</div></section>

{projects_section(3)}
{trusted_by()}

<section class="offer"><div class="wrap offer-inner">
{img("exhaust-fan.jpg", "Technician inspecting a rooftop exhaust fan", lazy=False)}
<div>
<h2>Free Equipment Assessment</h2>
<p>For commercial buildings. We walk your rooftop units and mechanical equipment and give you a written condition report for every unit: what is good, what to watch, and what to budget for. No cost and no obligation.</p>
<a class="btn btn-white" href="/contact?type=assessment">{icon("calendar", 20)} Book your free assessment</a>
</div>
</div></section>

{reviews_block(["joe", "andrew", "steven", "kathy", "madeline", "corey"])}
{values_block()}
{team_block()}
{where_we_work()}
{cta_band()}
"""

COMMERCIAL = f"""<section class="page-hero" style="--hero:url('/assets/img/rooftop-units.jpg')"><div class="wrap">
<h1>Commercial HVAC and mechanical services built for uptime.</h1>
<p>For facility managers, property managers, general contractors and multi-site operators across {AREA}.</p>
{buttons(dark=True)}
{rating_badge("on-dark")}
</div></section>
{trust_strip()}
{trusted_by()}

<section class="services"><div class="wrap">
<div class="section-head center"><h2>Commercial service capabilities</h2><p>One mechanical partner for service, maintenance and construction.</p></div>
{photo_cards([
    ("rtu-set.jpg", "Crew setting a rooftop unit", "building", "Rooftop units", "Repair, troubleshooting and full replacement of packaged rooftop units, including crane lifts, curb adapters and startup. All major brands.", "/rtu-replacement"),
    ("service-tech.jpg", "Technicians on a maintenance visit", "clipboard", "Preventive maintenance agreements", "Twice-a-year or quarterly visits, standard filters included, priority scheduling, 10% off repairs and a written report after every visit.", "/commercial-maintenance"),
    ("buildout.jpg", "Crew on a tenant build-out", "wrench", "Design-build mechanical", "Mechanical partner for general contractors from planning through closeout, on new construction and tenant build-outs.", "/design-build"),
    ("ductwork.jpg", "Ductwork installation", "duct", "Ductwork and sheet metal", "Rectangular and spiral duct, exhaust fans and make-up air, installed clean and coordinated with the other trades.", None),
    ("rtu-new.jpg", "New rooftop heating and cooling units", "flame", "Heating and boilers", "Commercial heating repair and troubleshooting, boiler service and replacement, and CSD-1 testing.", None),
    ("chillers.jpg", "Commercial cooling equipment installation", "snow", "Cooling and refrigeration", "Air conditioning repair, airflow problems, VRF and ductless systems for offices and build-outs, and commercial refrigeration.", None),
])}
</div></section>

{projects_section()}

<section class="split"><div class="wrap split-inner">
{img("lift-ductwork.jpg", "Crew installing ductwork from a scissor lift", lazy=False)}
<div>
<h2>Working with general contractors</h2>
<p>We bid, build and close out like a partner. Every project is led by a superintendent with 42 years of experience, with clean submittals, coordinated schedules and our own sheet metal and equipment crews.</p>
<p>Have plans out for bid? Send them through our <a href="/contact?type=quote">quote request</a> (you can attach drawings) or email <a href="mailto:Matt@DeeplyRootedHVAC.com">Matt@DeeplyRootedHVAC.com</a>.</p>
<a class="btn btn-navy" href="/design-build">{icon("arrow", 18)} Design-build and general contractors</a>
</div>
</div></section>

<section class="offer"><div class="wrap offer-inner">
{img("exhaust-fan.jpg", "Technician inspecting rooftop exhaust fan")}
<div>
<h2>Free Equipment Assessment</h2>
<p>We walk your rooftop units and give you a written condition report for each one, with repair recommendations and a replacement budget. It is the easiest way to plan next year's HVAC spending and to see what a maintenance agreement would cost.</p>
<a class="btn btn-white" href="/contact?type=assessment">{icon("calendar", 20)} Book your free assessment</a>
</div>
</div></section>
{reviews_block(["joe", "andrew"], "What commercial customers say")}
{values_block("How we work", "Our core values are how we treat your building, your people and your schedule.")}
{cta_band("Keep your building running.")}
"""

RTU_FAQ = [
    ("Should I repair or replace my rooftop unit?", "It depends on the unit's age, condition, refrigerant and repair history. Our Free Equipment Assessment gives you a written condition report and a replacement budget so you can decide with real numbers."),
    ("Do you handle the crane and curb work?", "Yes. We plan the lift, arrange the crane, handle curb adapters, set the unit and start it up. Gas, electrical and roofing ties are coordinated with those trades."),
    ("What refrigerant do new units use?", "Every new unit we install uses R-454B, the current refrigerant for new equipment."),
    ("Do you work with property managers and multi-site owners?", "Yes. We can assess every unit across your buildings and give you one plan for repairs and replacements."),
]

RTU = f"""<section class="page-hero" style="--hero:url('/assets/img/library-crane.jpg')"><div class="wrap">
<h1>Rooftop unit repair and replacement</h1>
<p>From one tired unit to a full 90-ton changeout. We plan the lift, set the equipment and start it up, with as little disruption to your building as possible.</p>
{buttons(dark=True)}
</div></section>
{trust_strip()}

<section class="split"><div class="wrap split-inner">
{img("rtu-changeout.jpg", "Crew disconnecting an old rooftop unit", lazy=False)}
<div>
<h2>What is included</h2>
<ul class="checks">
<li>{icon("check", 20)} Site visit and a written proposal with a clear scope</li>
<li>{icon("check", 20)} Equipment selection and ordering, all major brands</li>
<li>{icon("check", 20)} Crane lift planning, curb adapters and rigging</li>
<li>{icon("check", 20)} Removal of the old unit</li>
<li>{icon("check", 20)} Setting, connecting and starting up the new unit</li>
<li>{icon("check", 20)} Coordination with your roofer, electrician and gas contractor</li>
<li>{icon("check", 20)} Manufacturer warranty plus our one-year workmanship guarantee</li>
</ul>
</div>
</div></section>

<section class="services"><div class="wrap">
<div class="section-head center"><h2>How a replacement works</h2></div>
{steps([
    ("Assess", "We look at the unit, the curb, the roof and the building, and talk with you about schedule and budget."),
    ("Propose", "You get a written proposal with the equipment, the scope and one firm price."),
    ("Lift day", "We plan the crane, pull the old unit and set the new one, usually around your business hours."),
    ("Start up", "We start the unit, check it over and walk you through what was done."),
])}
</div></section>

<section class="photo-row"><div class="section-head center"><h2>On the job</h2></div><div class="wrap">
{img("library-crane.jpg", "Crane lifting rooftop units at Springfield Township Library")}
{img("rtu-delivery.jpg", "New rooftop unit on a flatbed ready for the lift")}
{img("rtu-set.jpg", "Crew setting a rooftop unit on its curb")}
</div></section>

<section class="faq"><div class="wrap narrow">
<div class="section-head center"><h2>Rooftop unit questions</h2></div>
{faq_html(RTU_FAQ)}
</div></section>
{reviews_block(["joe", "andrew"], "What commercial customers say")}
{cta_band("Is a rooftop unit giving you trouble?")}
"""

PM_FAQ = [
    ("How often do you visit?", "Twice a year (spring and fall) or four times a year (quarterly). Quarterly plans suit buildings that run hard or need tighter filter changes."),
    ("What does a maintenance agreement cost?", "It is priced by the equipment you have and how often we visit. Start with a Free Equipment Assessment and you will get a written condition report and a maintenance proposal together."),
    ("Do you cover more than one building?", "Yes. One agreement can cover all of your sites, with a written report for every building after each visit."),
    ("Do you service boilers?", "Yes. CSD-1 boiler inspection is included for maintenance customers with boilers."),
]

COMM_PM = f"""<section class="page-hero" style="--hero:url('/assets/img/service-tech.jpg')"><div class="wrap">
<h1>Commercial maintenance agreements</h1>
<p>Fewer breakdowns, longer equipment life and a written report after every visit. Built for owners, property managers and multi-site operators.</p>
{buttons(dark=True)}
</div></section>
{trust_strip()}

<section class="services"><div class="wrap">
<div class="section-head center"><h2>What every agreement includes</h2></div>
{icon_cards([
    ("calendar", "Scheduled visits", "Twice a year or quarterly. We put the visits on the calendar so you never have to remember."),
    ("duct", "Standard filters included", "Filters changed at every visit, at no extra charge."),
    ("clipboard", "Written report after every visit", "What we checked, what we found, and what to watch or budget for, unit by unit."),
    ("bolt", "Priority scheduling", "Members move to the front of the line when something goes wrong."),
    ("percent", "10% off repairs", "Members save on parts and labor for every repair."),
    ("flame", "Boiler inspection", "CSD-1 boiler inspection included when your building has a boiler."),
], cols=3)}
</div></section>

<section class="split"><div class="wrap split-inner">
{img("exhaust-fan.jpg", "Technician inspecting a rooftop exhaust fan", lazy=False)}
<div>
<h2>How to get started</h2>
{steps([
    ("Free Equipment Assessment", "We walk every unit and give you a written condition report."),
    ("Your maintenance proposal", "Equipment covered, visit schedule, what is included and one yearly price."),
    ("Visits and reports", "We show up on schedule and send a report after every visit."),
])}
<a class="btn btn-navy" href="/contact?type=assessment">{icon("calendar", 20)} Book your free assessment</a>
</div>
</div></section>

<section class="faq"><div class="wrap narrow">
<div class="section-head center"><h2>Maintenance agreement questions</h2></div>
<p class="cost-line"><b>What it costs:</b> priced by the equipment you have and how often we visit. Your Free Equipment Assessment comes with a written maintenance proposal and one yearly price, so you know the cost before you sign anything.</p>
{faq_html(PM_FAQ)}
<p class="note center">Looking for a plan for your home? See our <a href="/rooted-assurance-program">Rooted Assurance home plans</a>.</p>
</div></section>
{reviews_block(["joe", "andrew"], "What commercial customers say")}
{cta_band("Keep your building running.")}
"""

DESIGN_BUILD = f"""<section class="page-hero" style="--hero:url('/assets/img/buildout.jpg')"><div class="wrap">
<h1>Design-build mechanical for general contractors and owners</h1>
<p>Design-build and plan and spec HVAC for new buildings, additions and tenant build-outs. We find the savings in design, before they turn into change orders.</p>
<div class="cta-row"><a class="btn btn-white" href="/contact?type=quote">{icon("clipboard", 20)} Send us your project</a><a class="btn btn-outline on-dark" href="/projects">{icon("building", 20)} Featured projects</a></div>
</div></section>
{trust_strip()}

<section class="services"><div class="wrap">
<div class="section-head center"><h2>Why general contractors bring us back</h2></div>
{icon_cards([
    ("clipboard", "Owner-level estimating", "Every number is priced by the owner, with 15 years in the field. You talk to the person accountable for it."),
    ("percent", "Value engineering", "We look for savings during design, before they cost you margin."),
    ("wrench", "Our own crews", "Sheet metal, equipment setting, piping, controls and startup are done by our own people."),
    ("building", "A superintendent with 42 years", "Straight answers and a crew that shows up ready when the field moves."),
    ("calendar", "Clean paperwork", "Submittals, schedules and closeout handled without chasing."),
    ("shield", "Service after the punch list", "Our service department backs the install with warranty support and maintenance."),
], cols=3)}
</div></section>

<section class="split"><div class="wrap split-inner">
{img("spiral-lift.jpg", "Crew hanging spiral duct from a scissor lift", lazy=False)}
<div>
<h2>Projects we build</h2>
<p>Offices and tenant build-outs, churches, retail, recreation facilities, schools, manufacturing and government buildings. Project sizes run from small build-outs to $500K+ equipment replacements and new buildings.</p>
<p>Send bid invitations and drawings through our <a href="/contact?type=quote">quote request</a>, where you can attach plans, or email <a href="mailto:Matt@DeeplyRootedHVAC.com">Matt@DeeplyRootedHVAC.com</a>.</p>
<ul class="checks">
<li>{icon("check", 20)} Michigan Mechanical Contractor License #{LICENSE}</li>
<li>{icon("check", 20)} Certificate of insurance and W-9 on request</li>
<li>{icon("check", 20)} Bid and performance bonds available</li>
<li>{icon("check", 20)} Prequalification packages and project references ready to send</li>
<li>{icon("check", 20)} Written safety program and toolbox talks</li>
</ul>
</div>
</div></section>
{projects_section()}
{cta_band("Have a project out for bid?", kind="gc")}
"""

PROJECTS_PAGE = f"""<section class="page-hero" style="--hero:url('/assets/img/library-crane.jpg')"><div class="wrap">
<h1>Featured projects</h1>
<p>Rooftop unit replacements, design-build new buildings, additions and build-outs across Southeast Michigan.</p>
{buttons(dark=True)}
</div></section>
<section class="video-feature"><div class="wrap video-inner">
<div class="video-frame"><video controls preload="none" playsinline poster="/assets/video/springfield-poster.jpg" src="/assets/video/springfield-rtu-replacement.mp4" aria-label="Rooftop unit replacement job tour at Springfield Township Library"></video></div>
<div><h2>Featured: Springfield Township Library</h2><p>A 90-ton rooftop unit and heating and ventilating replacement, contracted direct with the township and completed in 2026.</p></div>
</div></section>
{projects_section(None, "More project highlights", link=False, skip_first=True)}
<section class="services"><div class="wrap narrow">
<div class="section-head center"><h2>More recent work</h2><p>A sample of the commercial projects our crews have completed or have underway.</p></div>
<table class="work"><thead><tr><th>Project</th><th>Scope</th><th>Year</th></tr></thead><tbody>
{"".join(f"<tr><td><b>{e(a)}</b></td><td>{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c in MORE_WORK)}
</tbody></table>
</div></section>
{cta_band("Let's talk about your project.")}
"""

RESIDENTIAL = f"""<section class="page-hero dim" style="--hero:url('/assets/img/condenser.jpg')"><div class="wrap">
<h1>Home heating and cooling you can trust.</h1>
<p>Repairs, replacements and maintenance for homes across {AREA}. Clear options, honest advice and a clean job site.</p>
{buttons(dark=True, kind="home")}
{rating_badge("on-dark")}
</div></section>
{trust_strip()}

<section class="services"><div class="wrap">
<div class="section-head center"><h2>Residential services</h2><p>Everything your home needs to stay comfortable all year.</p></div>
{icon_cards([
    ("flame", "Heating repair", "No heat, short cycling, strange noises, ignition problems and rooms that never warm up."),
    ("snow", "Air conditioning repair", "No cooling, weak airflow, frozen coils, leaks and uneven temperatures."),
    ("home", "New furnace and AC", "We help you choose the right system and install it right. Residential installs are primarily AirQuest systems."),
    ("thermo", "Boilers and radiant heat", "Boiler repair, service and replacement."),
    ("fan", "Ductless mini splits", "Installation and repair for additions, bonus rooms, garages and zoning."),
    ("duct", "Airflow and comfort", "Hot and cold rooms, stuffy air, filters, thermostat upgrades and duct improvements."),
], cols=3)}
<div class="photo-row tight">{img("furnace.jpg", "New furnace installation")}{img("furnace-2.jpg", "Furnace and ductwork in a basement")}{img("condenser.jpg", "Air conditioning condenser outside a home")}</div>
</div></section>

{values_block("What you can expect from us", "Our core values are the promise we make at your door.")}

<section class="offer"><div class="wrap offer-inner">
{img("safety-vest.jpg", "Deeply Rooted Mechanical team member")}
<div>
<h2>Rooted Assurance Program</h2>
<p>Two tune-ups a year, priority scheduling and 10% off parts and labor. Plans start at $295 a year.</p>
<a class="btn btn-white" href="/rooted-assurance-program">{icon("calendar", 20)} See the plans</a>
</div>
</div></section>
{reviews_block(["steven", "kathy", "madeline", "anthony", "laura", "corey"], "What homeowners say")}
{cta_band("Comfortable all year, starting today.", kind="home")}
"""


def plan_cards():
    out = []
    for n, p, url, who, items in PLANS:
        lis = "".join(f"<li>{icon('check', 18)} {e(i)}</li>" for i in items)
        out.append(f'<div class="plan"><h3>{e(n)}</h3><p class="price">{p}<span> per year</span></p>'
                   f'<p class="who">{e(who)}</p><ul class="plan-list">{lis}</ul>'
                   f'<a class="btn btn-navy" href="{url}" rel="noopener">Join the {e(n)} plan</a></div>')
    return "".join(out)


PLANS_PAGE = f"""<section class="page-hero dim" style="--hero:url('/assets/img/furnace.jpg')"><div class="wrap">
<h1>Rooted Assurance Program</h1>
<p>Our home maintenance plans. We schedule your visits so you never have to remember, and you get priority service when something goes wrong.</p>
{rating_badge("on-dark")}
</div></section>

<section class="plans"><div class="wrap">
<div class="section-head center"><h2>Choose your plan</h2><p>Billed yearly through our secure QuickBooks checkout. Questions? Call <a href="tel:{TEL}">{PHONE}</a>.</p></div>
<div class="plan-grid">{plan_cards()}</div>
</div></section>

<section class="services"><div class="wrap">
<div class="section-head center"><h2>Every plan includes</h2></div>
{icon_cards([
    ("calendar", "Two visits a year", "A spring cooling check and a fall heating check. We call you to schedule."),
    ("bolt", "Priority scheduling", "Members move to the front of the line when something goes wrong."),
    ("percent", "10% off parts and labor", "On every repair, plus reduced emergency visit premiums."),
    ("shield", "Fewer breakdowns", "Small problems get caught early, which helps your equipment last longer."),
], cols=4)}
<p class="note center">Have a business? See our <a href="/commercial-maintenance">commercial maintenance agreements</a>.</p>
</div></section>
{reviews_block(["laura", "anthony", "kathy"], "What homeowners say")}
{cta_band("Questions about a plan?", kind="home")}
"""

OWNER_STORY = f"""<section class="owner"><div class="wrap owner-inner">
<figure class="owner-photo"><img src="/assets/team/matt.jpg" alt="Matt Pastor, owner of Deeply Rooted Mechanical" width="400" height="400" loading="lazy"><figcaption><strong>Matt Pastor</strong><span>Owner</span></figcaption></figure>
<div>
<h2>A note from our owner</h2>
<p>Construction is in my roots. It was my dad's world before it was mine. I lost him young, and I came into the trades as a fatherless young man trying to start life on my own.</p>
<p>For fifteen years, what I found was a broken industry in need of redemption. I worked for people who belittled their crews, didn't pay their subs, paid employees the bare minimum and built their businesses on the backs of those with the least. Some of them called themselves followers of Christ, but you couldn't see it in how they treated people.</p>
<p>Along the way, God put people in my path who showed me what a business in construction can look like when it honors Him and cares for people. I found hope. In 2024, by His grace, God called me to start Deeply Rooted Mechanical.</p>
<p>Jesus said that whoever has been forgiven little loves little (Luke 7:47). I have been redeemed from much, so I want to love much, and this company is how I get to do it: caring for our people and their families, treating every customer and partner with dignity, telling the truth when it costs us, and doing work that lasts. No effort, care or kindness is wasted. God sees all of it.</p>
<p>When I look at what the Lord has built here, I am humbled and grateful. Every crew member, every job and every open door is His provision. And to every customer and partner who has trusted us with your building, your home or your project: thank you. Your trust is a gift we never take for granted.</p>
<p class="sign">Matt Pastor, Owner</p>
</div>
</div></section>
"""

TRIBUTE = f"""<section class="tribute"><div class="wrap narrow">
<h2>Honoring Bill Purcell</h2>
<p class="center">Bill Purcell was part of the Deeply Rooted Mechanical family. We made this short video to honor his life and the way he served.</p>
<div class="yt"><iframe src="https://www.youtube-nocookie.com/embed/{TRIBUTE_YOUTUBE}" title="In Memory of Bill Purcell - Deeply Rooted Mechanical" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
</div></section>
"""

ABOUT_FAQ = [
    ("What areas do you serve?", "All of Southeast Michigan, including Livingston, Oakland, Genesee and Wayne counties. Our office is in Brighton."),
    ("What are your hours?", f"Our office is open Monday to Friday, 7:00 AM to 4:30 PM. Emergency service is available 24/7: call {PHONE} and press 1."),
    ("Are you licensed and insured?", f"Yes. We hold Michigan Mechanical Contractor License #{LICENSE} and carry full business insurance."),
    ("Do you offer guarantees or warranties?", "Yes. All work comes with a satisfaction guarantee, manufacturer warranties on installed equipment and a one-year workmanship guarantee."),
    ("Do you do plumbing or electrical work?", "No. We are heating and cooling specialists. We coordinate with your plumber and electrician when a project needs them."),
    ("What brands do you install?", "Commercially, all major brands. For homes, we primarily install AirQuest systems."),
    ("How often should my system be serviced?", "At least once a year, and twice a year for best results: a spring cooling check and a fall heating check."),
]

ABOUT = f"""<section class="page-hero" style="--hero:url('/assets/img/safety-vest.jpg')"><div class="wrap">
<h1>About Deeply Rooted Mechanical</h1>
<p>A Brighton heating and cooling contractor serving businesses and homes with excellent craftsmanship, faithful leadership and a commitment to treat every person with dignity.</p>
</div></section>

{OWNER_STORY}

<section class="split why"><div class="wrap split-inner">
{img("crew-roof.jpg", "Deeply Rooted Mechanical crew setting rooftop equipment")}
<div>
<h2>Why we do what we do</h2>
<p>We do our work to honor God, not ourselves. We want to reflect His character through excellent craftsmanship, faithful leadership and the way we treat people.</p>
<p>Every person we work with, employees, customers and partners, is made in the image of God and worthy of dignity, care and respect. In an industry often marked by shortcuts and burnout, we exist to be different: to fix systems, honor people and restore what is broken.</p>
</div>
</div></section>

{values_block(tone="tight")}
{TRIBUTE}
{team_block()}

<section class="faq"><div class="wrap narrow">
<div class="section-head center"><h2>Frequently asked questions</h2></div>
{faq_html(ABOUT_FAQ)}
</div></section>
{reviews_block(["corey", "joe", "madeline"])}
{cta_band()}
"""

CONTACT = f"""<section class="page-hero short" style="--hero:url('/assets/img/service-tech.jpg')"><div class="wrap">
<h1 id="formTitle">How can we help?</h1>
<p id="formSub">Tell us what is going on and we will get back to you quickly. For no heat, no cooling or anything urgent, call <a href="tel:{TEL}">{PHONE}</a> and press 1, any hour.</p>
</div></section>

<section class="contact"><div class="wrap contact-inner">
<form name="service-request" method="POST" action="/thanks" enctype="multipart/form-data" data-netlify="true" netlify-honeypot="company_website" class="request-form">
<input type="hidden" name="form-name" value="service-request">
<input type="hidden" name="source" value="Website">
<p class="hp"><label>Leave this empty <input name="company_website"></label></p>

<fieldset><legend>What do you need?</legend>
<div class="choices">
<label class="choice"><input type="radio" name="request_type" value="Service call" required><span>{icon("wrench", 22)} Service call<small>Something isn't working</small></span></label>
<label class="choice"><input type="radio" name="request_type" value="Free Equipment Assessment"><span>{icon("calendar", 22)} Free Equipment Assessment<small>For commercial buildings</small></span></label>
<label class="choice"><input type="radio" name="request_type" value="Quote"><span>{icon("clipboard", 22)} Quote or bid<small>New system, replacement or project</small></span></label>
<label class="choice"><input type="radio" name="request_type" value="Maintenance / tune-up"><span>{icon("check", 22)} Maintenance<small>Tune-up or maintenance plan</small></span></label>
</div>
</fieldset>

<fieldset><legend>Type of property</legend>
<label class="pill"><input type="radio" name="property_type" value="Commercial" required> Business</label>
<label class="pill"><input type="radio" name="property_type" value="Residential"> Home</label>
</fieldset>

<label><span id="descLabel">What's going on?</span><textarea id="formDesc" name="description" rows="4" required placeholder="Tell us about the equipment, the problem or the project"></textarea></label>

<div class="grid2">
<label>First name<input name="first_name" autocomplete="given-name" required></label>
<label>Last name<input name="last_name" autocomplete="family-name" required></label>
<label>Phone<input name="phone" type="tel" autocomplete="tel" required></label>
<label>Email <span class="opt">(optional)</span><input name="email" type="email" autocomplete="email"></label>
<label class="span2 for-commercial">Company <span class="opt">(optional)</span><input name="company" autocomplete="organization"></label>
<label class="span2"><span id="addrLabel">Service address</span><input name="street" autocomplete="street-address" required></label>
<label>City<input name="city" autocomplete="address-level2" required></label>
<label>ZIP code<input name="zip" autocomplete="postal-code" inputmode="numeric" required></label>
</div>

<div class="grid3">
<label>How soon? <span class="opt">(optional)</span><select name="urgency"><option value="">Choose</option><option>Emergency: no heat or no cooling</option><option>In the next few days</option><option>Flexible</option></select></label>
<label>Preferred day <span class="opt">(optional)</span><select name="preferred_day"><option value="">Any day</option><option>Monday</option><option>Tuesday</option><option>Wednesday</option><option>Thursday</option><option>Friday</option></select></label>
<label>Preferred time <span class="opt">(optional)</span><select name="preferred_time"><option value="">Any time</option><option>Morning (7 to 11)</option><option>Midday (11 to 2)</option><option>Afternoon (2 to 4:30)</option></select></label>
</div>

<label class="for-plans">Drawings or photos <span class="opt">(optional, PDF or image, up to 8 MB)</span><input type="file" name="attachment" accept=".pdf,image/*"></label>

<label>Best way to reach you
<select name="preferred_contact"><option>Phone call</option><option>Text</option><option>Email</option></select></label>

<div class="sms"><p class="sms-h">Text message updates (optional)</p>
<label class="consent"><input type="checkbox" name="sms_consent_service" value="Yes"> I consent to receive non-marketing text messages from Deeply Rooted Mechanical LLC d/b/a Deeply Rooted HVAC about appointments, service updates, estimates, and customer support. Message frequency may vary. Message &amp; data rates may apply. Reply HELP for help. Reply STOP to opt out.</label>
<label class="consent"><input type="checkbox" name="sms_consent_marketing" value="Yes"> I consent to receive marketing text messages from Deeply Rooted Mechanical LLC d/b/a Deeply Rooted HVAC about special offers, discounts, and new product updates. Message frequency may vary. Message &amp; data rates may apply. Reply HELP for help or STOP to opt out.</label>
<p class="small">Texting is optional and not required to request service.</p>
</div>
<p class="small">See our <a href="/privacy-policy">Privacy Policy</a> and <a href="/terms-of-service">Terms of Service</a>.</p>
<button class="btn btn-navy btn-lg" type="submit">{icon("arrow", 20)} <span id="submitText">Send request</span></button>
</form>

<aside class="contact-card">
<h2>Reach us</h2>
<ul class="reach">
<li><span class="r-ic">{icon("phone", 22)}</span><span><b>Call</b><a href="tel:{TEL}">{PHONE}</a><small>Press 1 for service, 24/7</small></span></li>
<li><span class="r-ic">{icon("clipboard", 22)}</span><span><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></span></li>
<li><span class="r-ic">{icon("building", 22)}</span><span><b>Office</b>{STREET}<br>{CITY}, {STATE} {ZIP}</span></li>
<li><span class="r-ic">{icon("clock", 22)}</span><span><b>Hours</b>Mon to Fri, 7:00 AM to 4:30 PM<small>Emergency service 24/7</small></span></li>
<li><span class="r-ic">{icon("wrench", 22)}</span><span><b>General contractors</b>Send bid invitations to <a href="mailto:Matt@DeeplyRootedHVAC.com">Matt@DeeplyRootedHVAC.com</a></span></li>
</ul>
{rating_badge()}
</aside>
</div></section>
"""

THANKS = f"""<section class="page-hero short"><div class="wrap">
<h1>Thank you! We got your request.</h1>
<p>Our team will reach out shortly during business hours. If this is an emergency, please call <a href="tel:{TEL}">{PHONE}</a> and press 1 so we can help right away.</p>
<div class="cta-row"><a class="btn btn-white" href="/">Back to home</a></div>
</div></section>
"""

PRIVACY = f"""<section class="page-hero short"><div class="wrap"><h1>Privacy Policy</h1><p>Effective March 3, 2026. Updated November 2026.</p></div></section>
<section class="legal-text"><div class="wrap narrow">
<p>This policy explains how {LEGAL} d/b/a Deeply Rooted HVAC ("we", "us") collects and uses information through deeplyrootedhvac.com and our text messaging.</p>
<h2>Information we collect</h2>
<p>When you contact us or submit a form, we collect the information you give us: your name, phone number, email address, service address and the details of your service, estimate or support request. Like most websites, we also collect basic usage information such as pages visited and general device and browser information.</p>
<h2>How we use it</h2>
<p>We use your information to respond to your request, schedule appointments, provide estimates and service updates, communicate with you about your inquiry, and improve our website and services.</p>
<h2>Text messaging (SMS)</h2>
<p>If you opt in, we may send you text messages about appointments, service updates, estimates and customer support, and, only if you separately opt in to marketing texts, occasional offers. Message frequency varies. Message and data rates may apply. Reply STOP at any time to opt out and HELP for help.</p>
<p>No mobile information will be shared with third parties or affiliates for marketing or promotional purposes. We may share information with subcontractors that support our services, such as customer service providers. Text messaging opt-in data and consent are not shared with any third parties for any other purpose.</p>
<h2>Cookies</h2>
<p>Our website may use cookies or similar technologies to understand traffic and improve your experience.</p>
<h2>Security</h2>
<p>We use reasonable measures to protect your information. No method of transmission over the internet or electronic storage is completely secure.</p>
<h2>Your choices</h2>
<p>You may ask us to access, correct or delete your personal information by contacting us. You can opt out of text messages at any time by replying STOP.</p>
<h2>Contact us</h2>
<p>{LEGAL} d/b/a Deeply Rooted HVAC<br>{STREET}, {CITY}, {STATE} {ZIP}<br>Phone: {PHONE}<br>Email: <a href="mailto:{EMAIL}">{EMAIL}</a><br>Website: deeplyrootedhvac.com</p>
</div></section>
"""

TERMS = f"""<section class="page-hero short"><div class="wrap"><h1>Terms of Service</h1><p>Effective March 3, 2026. Updated November 2026.</p></div></section>
<section class="legal-text"><div class="wrap narrow">
<p>These terms apply to your use of deeplyrootedhvac.com and the text messaging program of {LEGAL} d/b/a Deeply Rooted HVAC.</p>
<h2>Our services</h2>
<p>We provide residential and commercial heating and cooling services. Information on this website is for general purposes and may change at any time.</p>
<h2>SMS messaging terms</h2>
<p>By opting in through our website forms, you agree to receive non-marketing text messages about appointments, service updates, estimates and customer support, and marketing messages only if you separately opt in to them. Message frequency may vary. Msg &amp; data rates may apply. Reply STOP to opt out. Reply HELP for help. Wireless carriers are not liable for delayed or undelivered messages.</p>
<h2>Eligibility</h2>
<p>You must be at least 18 years old, or have permission from a parent or legal guardian, to use this website and opt in to text messages.</p>
<h2>Your responsibilities</h2>
<p>Please provide accurate information, use this website only for lawful purposes, and do not submit false information or interfere with the website.</p>
<h2>Intellectual property</h2>
<p>The content of this website, including text, images, logos and design, belongs to us or is used with permission and may not be copied or distributed without our written consent.</p>
<h2>Disclaimer and limitation of liability</h2>
<p>This website is provided "as is" and "as available" without warranties of any kind. To the extent permitted by law, we are not liable for indirect, incidental, consequential or special damages arising from use of this website or our messaging services.</p>
<h2>Privacy</h2>
<p>Your use of this website and our messaging is also governed by our <a href="/privacy-policy">Privacy Policy</a>.</p>
<h2>Changes</h2>
<p>We may update these terms by posting a revised version here. Continued use after a change means you accept the updated terms.</p>
<h2>Customer support</h2>
<p>{STREET}, {CITY}, {STATE} {ZIP}<br>Phone: {PHONE}<br>Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
</div></section>
"""

NOTFOUND = f"""<section class="page-hero short"><div class="wrap">
<h1>We couldn't find that page.</h1>
<p>Try the <a href="/">home page</a>, or call <a href="tel:{TEL}">{PHONE}</a> and press 1 for service.</p>
</div></section>
"""


P = "Deeply Rooted Mechanical"
PAGES = [
    ("/", "index.html", "Commercial HVAC Contractor in Brighton, MI | Deeply Rooted Mechanical",
     "Commercial HVAC across Southeast Michigan: rooftop units, maintenance agreements, design-build and 24/7 emergency service. 5.0 stars on Google.", HOME, []),
    ("/commercial", "commercial/index.html", f"Commercial HVAC Services in Southeast Michigan | {P}",
     "Commercial HVAC for owners, property managers and GCs in Southeast Michigan: RTU replacement, maintenance agreements, design-build and boilers.", COMMERCIAL,
     [service_schema("Commercial HVAC service", "Commercial heating and cooling repair, replacement, maintenance and design-build.", "/commercial")]),
    ("/rtu-replacement", "rtu-replacement/index.html", f"Rooftop Unit (RTU) Repair and Replacement, Southeast Michigan | {P}",
     "Commercial rooftop unit repair and replacement in Southeast Michigan: crane lifts, curbs, setting and startup. Licensed, insured, 5.0 on Google.", RTU,
     [service_schema("Rooftop unit replacement", "Commercial rooftop unit repair and replacement including crane lifts, curb adapters, setting and startup.", "/rtu-replacement"), faq_schema(RTU_FAQ)]),
    ("/commercial-maintenance", "commercial-maintenance/index.html", f"Commercial HVAC Maintenance Agreements | {P}",
     "Commercial HVAC maintenance twice a year or quarterly: filters included, priority service, 10% off repairs and a written report every visit.", COMM_PM,
     [service_schema("Commercial HVAC maintenance agreement", "Scheduled commercial HVAC maintenance with filters, priority service, repair discounts and written reports.", "/commercial-maintenance"), faq_schema(PM_FAQ)]),
    ("/design-build", "design-build/index.html", f"Design-Build HVAC for General Contractors | {P}",
     "Design-build and plan and spec HVAC for general contractors and owners in Southeast Michigan, with value engineering and our own crews.", DESIGN_BUILD,
     [service_schema("Design-build HVAC", "Design-build and plan and spec commercial HVAC for new buildings, additions and tenant build-outs.", "/design-build")]),
    ("/projects", "projects/index.html", f"Featured Commercial HVAC Projects | {P}",
     "Recent rooftop unit replacements, design-build new buildings, additions and build-outs across Southeast Michigan.", PROJECTS_PAGE, []),
    ("/residential", "residential/index.html", f"Furnace, AC and Boiler Service for Homes | {P}",
     "Home heating and cooling repair, replacement and maintenance across Southeast Michigan. Honest options, clean work, 24/7 emergency service.", RESIDENTIAL,
     [service_schema("Residential HVAC service", "Furnace, air conditioning, boiler and mini split repair, replacement and maintenance.", "/residential")]),
    ("/rooted-assurance-program", "rooted-assurance-program/index.html", f"Rooted Assurance Home HVAC Maintenance Plans | {P}",
     "Two tune-ups a year, priority scheduling and 10% off parts and labor. Furnace and AC $495, mini split $295, boiler $595 per year.", PLANS_PAGE, []),
    ("/about-us", "about-us/index.html", f"About Us | {P}, Brighton, MI",
     "A faith-driven heating and cooling contractor in Brighton serving Southeast Michigan. Our owner's story, core values and team.", ABOUT, [faq_schema(ABOUT_FAQ)]),
    ("/contact", "contact/index.html", f"Request Service, an Assessment or a Quote | {P}",
     "Request HVAC service, a Free Equipment Assessment or a quote. 24/7 emergency service: call (810) 360-9664 and press 1.", CONTACT, []),
    ("/thanks", "thanks/index.html", f"Thank You | {P}", "Your request was received.", THANKS, []),
    ("/privacy-policy", "privacy-policy/index.html", f"Privacy Policy | {P}", "Privacy policy for deeplyrootedhvac.com and text messaging.", PRIVACY, []),
    ("/terms-of-service", "terms-of-service/index.html", f"Terms of Service | {P}", "Terms of service for deeplyrootedhvac.com and text messaging.", TERMS, []),
    ("/404", "404.html", f"Page Not Found | {P}", "Page not found.", NOTFOUND, []),
]

REDIRECTS = """# Old addresses from the previous site keep their rankings
/home                                  /                           301
/Commercial                            /commercial                 301
/Residential                           /residential                301
/about                                 /about-us                   301
/membership                            /rooted-assurance-program   301
/maintenance                           /commercial-maintenance     301
/deeplyrootedhvac.com/privacy-policy   /privacy-policy             301
/deeplyrootedhvac.com/terms-of-service /terms-of-service           301
"""


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    for path, fname, title, desc, body, extra in PAGES:
        dest = os.path.join(OUT, fname)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(page(path, title, desc, body, extra))
    with open(os.path.join(OUT, "_redirects"), "w") as f:
        f.write(REDIRECTS)
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /thanks\n\nSitemap: {SITE}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE}{p}</loc></url>" for p, *_ in PAGES if p not in ("/thanks", "/404"))
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print("built", len(PAGES), "pages into", OUT)


if __name__ == "__main__":
    build()
