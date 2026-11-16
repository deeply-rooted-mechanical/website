#!/usr/bin/env python3
"""Builds the deeplyrootedhvac.com static site into ./public.

Edit content below, run `python3 build.py`, commit build.py + public/.
Netlify publishes public/ as-is on every push to main (no build step on Netlify).
This repo is PUBLIC: never put keys, passwords or business notes in it.
"""
import json, os, shutil, html

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
FACEBOOK = "https://www.facebook.com/profile.php?id=61579592821615"
LINKEDIN = "https://www.linkedin.com/company/deeply-rooted-mechanical"
YELP = "https://www.yelp.com/biz/deeply-rooted-brighton-2"
GOOGLE_PROFILE = "https://www.google.com/maps?cid=12884188372933293353"
GOOGLE_REVIEW = "https://g.page/r/CSk16NMP1c2yEAE/review"
GOOGLE_RATING = "5.0"
GOOGLE_COUNT = 95          # update when the count moves (checked 11/16/2026)
SLOGAN = "Rooted in Faith. Built on Trust. Thankful in All."
VERSE = "Rooted and built up in Him, established in the faith, overflowing with thankfulness."
VERSE_REF = "Colossians 2:7"
# Bill Purcell tribute video on YouTube: "In Memory of Bill Purcell - Deeply Rooted Mechanical"
TRIBUTE_YOUTUBE = "7POdWOwnGcc"

e = html.escape

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

REVIEWS = [
    ("Joe Legato", "Rooftop units", "Deeply Rooted Mechanical has been fantastic to work with. I have had them replace one rooftop unit and repair two rooftop units. In both instances they were thorough, considerate of our property, considerate of our employees, and provided expert level of professionalism at every step of the process. The next time I am in need, Matt and his team will be my first call."),
    ("Andrew Beach", "Office furnace", "We called Deeply Rooted Mechanical the morning our furnace went out at our office. They were out same day to fix our furnace! Chase was super kind and personable as well as efficient. I highly recommend this company for all of your HVAC needs!"),
    ("Anthony Progar", "Boiler repair", "After our hydro-static boiler that provides radiant heat and hot water stopped working, we called Deeply Rooted Mechanical. We're extremely satisfied with the service. Chase showed up on time and listened as I explained the issue. He took his time looking things over and found a bad part which he replaced. The cost was very reasonable."),
    ("Steven Finlayson", "Furnace, AC and thermostat", "We needed the works, new A/C condenser, new furnace, new thermostat, you name it, and we were very pleased not only with the upgrade in equipment, but with the service provided. Matt and his crew were polite, respectful of our time, and very professional."),
    ("Kathy Flowers", "Heating repair", "Chase and Deeply Rooted Mechanical helped me solve my complicated issues regarding my furnace problems and heat distribution throughout my home. He communicated well, with integrity and respect, and worked to address the issue in a way that was least expensive. Highly recommend them!"),
    ("Laura C", "Service call", "Excellent service! Very prompt and professional! We called on a Monday afternoon and had a technician at our home by Tuesday afternoon to fix our system. They even talked me through how to turn off the water to my leaking humidifier via text Monday night."),
    ("Madeline Dunn", "Furnace and ductwork", "They fixed an overheating problem without adding extra lines and looked at the bigger picture. They were professional, took their shoes off, and even made sure my furnace didn't overheat. I interviewed three HVAC companies and definitely made the right choice. They treated us like family and offered a fair price."),
    ("Corey De Luca", "Service call", "The owner Matt is hands down one of the nicest business owners I've interacted with. He listened to my concerns and explained everything thoroughly. The technician was extremely kind, knowledgeable and honest. I highly recommend them!"),
]

NAV = [("/", "Home"), ("/Commercial", "Commercial"), ("/Residential", "Residential"),
       ("/rooted-assurance-program", "Maintenance Plans"), ("/about-us", "About"), ("/contact", "Contact")]


def schema():
    return {
        "@context": "https://schema.org", "@type": "HVACBusiness",
        "name": NAME, "legalName": LEGAL, "url": SITE + "/",
        "logo": SITE + "/assets/logo.png", "image": SITE + "/assets/img/rtu-crane.jpg",
        "telephone": PHONE, "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY,
                    "addressRegion": STATE, "postalCode": ZIP, "addressCountry": "US"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                       "opens": "07:00", "closes": "16:30"}],
        "areaServed": [{"@type": "AdministrativeArea", "name": n} for n in
                       ["Southeast Michigan", "Livingston County, MI", "Oakland County, MI",
                        "Genesee County, MI", "Wayne County, MI"]],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": GOOGLE_RATING, "reviewCount": GOOGLE_COUNT},
        "knowsAbout": ["Commercial HVAC", "Rooftop unit (RTU) replacement", "Commercial HVAC maintenance agreements",
                       "Design-build HVAC", "Tenant build-out HVAC", "Sheet metal ductwork", "Boiler service",
                       "Ductless mini split systems", "Furnace repair", "Air conditioning repair"],
        "slogan": SLOGAN, "sameAs": [FACEBOOK, LINKEDIN, YELP, GOOGLE_PROFILE],
    }


def head(title, desc, path):
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
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">{json.dumps(schema())}</script>
</head>
<body>
"""


def header(path):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == path else ""}>{t}</a>' for h, t in NAV)
    return f"""<div class="topbar"><div class="wrap">
<span class="slogan-mini">{SLOGAN}</span>
<a href="tel:{TEL}">{icon("phone", 16)} {PHONE} &middot; 24/7</a>
</div></div>
<header class="site"><div class="wrap">
<a class="brand" href="/"><img src="/assets/logo.png" alt="{NAME} logo" width="58" height="58"><span class="brand-name"><b>Deeply Rooted</b><b>Mechanical</b></span></a>
<nav aria-label="Main">{links}</nav>
<a class="btn btn-gold hdr-cta" href="/contact?type=service">Request Service</a>
</div></header>
<main>
"""


def footer():
    return f"""</main>
<section class="verse"><div class="wrap">
<p class="slogan-big">{SLOGAN}</p>
<p class="verse-text">"{VERSE}" <span>{VERSE_REF}</span></p>
</div></section>
<footer class="site"><div class="wrap cols">
<div>
<img src="/assets/logo.png" alt="" width="72" height="72">
<p><strong>{NAME}</strong><br>{STREET}<br>{CITY}, {STATE} {ZIP}</p>
</div>
<div>
<h3>Contact</h3>
<p><a href="tel:{TEL}">{PHONE}</a> (press 1 for service)<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p>Office: Mon to Fri, 7:00 AM to 4:30 PM<br>Emergency service 24/7</p>
</div>
<div>
<h3>Services</h3>
<p><a href="/Commercial">Commercial HVAC</a><br><a href="/Residential">Residential HVAC</a><br><a href="/rooted-assurance-program">Maintenance plans</a><br><a href="/contact?type=assessment">Free Equipment Assessment</a></p>
</div>
<div>
<h3>Reviews and social</h3>
<p><a href="{GOOGLE_PROFILE}" rel="noopener">{GOOGLE_RATING} stars, {GOOGLE_COUNT} Google reviews</a><br><a href="{GOOGLE_REVIEW}" rel="noopener">Leave us a Google review</a><br><a href="{FACEBOOK}" rel="noopener">Facebook</a> &middot; <a href="{LINKEDIN}" rel="noopener">LinkedIn</a></p>
</div>
</div>
<div class="wrap legal"><p>&copy; 2026 {LEGAL}. Heating and cooling for homes and businesses across {AREA}.</p>
<p><a href="/privacy-policy">Privacy Policy</a> &middot; <a href="/terms-of-service">Terms of Service</a></p></div>
</footer>
<script src="/assets/site.js" defer></script>
</body>
</html>
"""


def page(path, title, desc, body):
    return head(title, desc, path) + header(path) + body + footer()


def buttons(dark=True, plans=False):
    """The three calls to action, always in Matt's order."""
    third = ('<a class="btn btn-outline{d}" href="/contact?type=quote">{i} Request a Quote</a>'
             .format(d=" on-dark" if dark else "", i=icon("clipboard", 20)))
    second_href = "/rooted-assurance-program" if plans else "/contact?type=assessment"
    second_txt = "Maintenance Plans" if plans else "Free Equipment Assessment"
    second_cls = "btn-white" if dark else "btn-navy"
    return (f'<div class="cta-row">'
            f'<a class="btn btn-gold" href="/contact?type=service">{icon("wrench", 20)} Request Service</a>'
            f'<a class="btn {second_cls}" href="{second_href}">{icon("calendar", 20)} {second_txt}</a>'
            f'{third}</div>')


def cta_band(text="Let us serve you!"):
    return f"""<section class="cta-band"><div class="wrap">
<h2>{text}</h2>
{buttons(dark=True)}
<p class="cta-phone">Or call <a href="tel:{TEL}">{PHONE}</a> and press 1 for service, 24/7.</p>
</div></section>
"""


def rating_badge(cls=""):
    return (f'<a class="rating {cls}" href="{GOOGLE_PROFILE}" rel="noopener" aria-label="Read our {GOOGLE_COUNT} Google reviews">'
            f'<span class="stars">{STARS}</span><span class="rating-text"><b>{GOOGLE_RATING}</b> from <b>{GOOGLE_COUNT}</b> Google reviews</span></a>')


def reviews_block(n=6):
    cards = "".join(
        f'<figure class="review"><div class="stars small">{"".join(icon("star", 18) for _ in range(5))}</div>'
        f'<blockquote>{e(t)}</blockquote><figcaption><span class="avatar">{e(name[0])}</span><span><b>{e(name)}</b>'
        f'<small>{e(kind)} &middot; Google review</small></span></figcaption></figure>'
        for name, kind, t in REVIEWS[:n])
    return f"""<section class="reviews"><div class="wrap">
<div class="reviews-head">
<div><h2>5-star service, {GOOGLE_COUNT} times over</h2>
<p>Every one of our {GOOGLE_COUNT} Google reviews is 5 stars. Here is what customers say.</p></div>
<div class="score"><span class="score-num">{GOOGLE_RATING}</span><span class="stars">{STARS}</span><span>{GOOGLE_COUNT} Google reviews</span></div>
</div>
<div class="review-grid">{cards}</div>
<div class="center"><a class="btn btn-navy" href="{GOOGLE_PROFILE}" rel="noopener">Read all {GOOGLE_COUNT} reviews on Google</a>
<a class="btn btn-outline" href="{GOOGLE_REVIEW}" rel="noopener">Leave us a review</a></div>
</div></section>
"""


def team_block():
    cards = "".join(
        f'<figure class="person"><img src="/assets/team/{k}.jpg" alt="{e(n)}, {e(t)}" width="400" height="400">'
        f'<figcaption><strong>{e(n)}</strong><span>{e(t)}</span></figcaption></figure>'
        for k, n, t in TEAM)
    return f"""<section class="team"><div class="wrap">
<div class="section-head center"><h2>Meet the team</h2><p>Local people you will see on your roof and in your mechanical room.</p></div>
<div class="team-grid">{cards}</div>
</div></section>
"""


def values_block(title="Our core values", intro="Everything we do grows out of five roots."):
    items = "".join(
        f'<li><span class="v-ic">{icon(ic, 30)}</span><span class="v-pre">Deeply Rooted in</span>'
        f'<span class="v-name">{e(t)}</span><p>{e(d)}</p></li>' for ic, t, d in VALUES)
    return f"""<section class="values"><div class="wrap">
<div class="section-head center"><h2>{title}</h2><p>{intro}</p></div>
<ul class="value-list">{items}</ul>
</div></section>
"""


def photo_cards(cards):
    return '<ul class="photo-cards">' + "".join(
        f'<li><img src="/assets/img/{img}" alt="{e(alt)}" loading="lazy"><div><span class="pc-ic">{icon(ic, 24)}</span>'
        f'<h3>{e(t)}</h3><p>{e(d)}</p></div></li>' for img, alt, ic, t, d in cards) + '</ul>'


def icon_cards(cards):
    return '<ul class="icon-cards">' + "".join(
        f'<li><span class="ic-wrap">{icon(ic, 30)}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for ic, t, d in cards) + '</ul>'


def slogan_band():
    return f"""<section class="slogan-band"><div class="wrap">
<p class="slogan-big">{SLOGAN}</p>
<p class="verse-text">"{VERSE}" <span>{VERSE_REF}</span></p>
</div></section>
"""


HOME = f"""<section class="hero" style="--hero:url('/assets/img/rtu-crane.jpg')"><div class="wrap">
<div class="hero-copy">
<p class="hero-slogan">{SLOGAN}</p>
<h1>Commercial HVAC you can count on, across Southeast Michigan.</h1>
<p>Rooftop unit repair and replacement, maintenance agreements, design-build and tenant build-outs, and 24/7 emergency service for building owners, property managers and general contractors. Homeowners too.</p>
{buttons(dark=True)}
{rating_badge("on-dark")}
</div>
</div></section>

<section class="video-feature"><div class="wrap video-inner">
<div class="video-frame"><video controls preload="metadata" playsinline poster="/assets/video/springfield-poster.jpg" src="/assets/video/springfield-rtu-replacement.mp4" aria-label="Springfield Township rooftop unit replacement job tour"></video></div>
<div>
<h2>See us at work</h2>
<p>A rooftop unit replacement for Springfield Township: new units lifted by crane, set on the roof and started up by our crew.</p>
<a class="btn btn-gold" href="/contact?type=quote">{icon("clipboard", 20)} Get a quote for your building</a>
</div>
</div></section>

{slogan_band()}

<section class="paths"><div class="wrap">
<a class="path" href="/Commercial"><img src="/assets/img/rtu-new.jpg" alt="DRM crew setting new rooftop units" loading="lazy"><div><h2>For your business</h2><p>RTUs, make-up air and exhaust, boilers, VRF and ductless, ductwork and preventive maintenance agreements. Built for uptime.</p><span class="more">Commercial HVAC {icon("arrow", 18)}</span></div></a>
<a class="path" href="/Residential"><img src="/assets/img/furnace.jpg" alt="New furnace installed by Deeply Rooted Mechanical" loading="lazy"><div><h2>For your home</h2><p>Furnace, air conditioning, boiler and mini split repair and replacement, plus our Rooted Assurance maintenance plan.</p><span class="more">Residential HVAC {icon("arrow", 18)}</span></div></a>
</div></section>

<section class="services"><div class="wrap">
<div class="section-head center"><h2>What we do</h2><p>Heating and cooling, done right the first time.</p></div>
{photo_cards([
    ("rtu-set.jpg", "Crew setting a new rooftop unit on its curb", "building", "Rooftop unit repair and replacement", "Diagnosis, repair and full RTU changeouts, including crane lifts, curbs and startup."),
    ("service-tech.jpg", "Technicians working inside a rooftop unit", "clipboard", "Maintenance agreements", "Scheduled visits with filters included, priority scheduling, 10% off repairs and a written report after every visit."),
    ("buildout.jpg", "Crew installing spiral duct on a tenant build-out", "wrench", "Design-build and build-outs", "Mechanical partner for general contractors on new construction and tenant build-outs, from planning to closeout."),
    ("ductwork.jpg", "Installer connecting ductwork", "duct", "Ductwork and sheet metal", "Rectangular and spiral duct, exhaust and make-up air, installed clean and on schedule."),
    ("furnace-2.jpg", "Furnace installation", "flame", "Heating and boilers", "Furnace and boiler repair and replacement, plus CSD-1 testing for commercial boilers."),
    ("safety-vest.jpg", "Deeply Rooted Mechanical crew member", "clock", "24/7 emergency service", "No heat, no cooling, or a unit down on a busy day. Call (810) 360-9664 and press 1, any hour."),
])}
</div></section>

<section class="offer"><div class="wrap offer-inner">
<img src="/assets/img/exhaust-fan.jpg" alt="Technician inspecting rooftop exhaust fan" width="1200" height="900">
<div>
<h2>Free Equipment Assessment</h2>
<p>We walk your rooftop units and mechanical equipment and give you a written condition report for every unit: what is good, what to watch, and what to budget for. No cost and no obligation.</p>
<a class="btn btn-gold" href="/contact?type=assessment">{icon("calendar", 20)} Book your free assessment</a>
</div>
</div></section>

{reviews_block(6)}
{values_block()}
{team_block()}
{cta_band()}
"""

COMMERCIAL = f"""<section class="page-hero" style="--hero:url('/assets/img/rooftop-units.jpg')"><div class="wrap">
<p class="hero-slogan">{SLOGAN}</p>
<h1>Commercial HVAC and mechanical services built for uptime.</h1>
<p>For facility managers, property managers, general contractors and multi-site operators across {AREA}.</p>
{buttons(dark=True)}
{rating_badge("on-dark")}
</div></section>

<section class="services"><div class="wrap">
<div class="section-head center"><h2>Commercial service capabilities</h2><p>One mechanical partner for service, maintenance and construction.</p></div>
{photo_cards([
    ("rtu-set.jpg", "Crew setting a rooftop unit", "building", "Rooftop units", "Repair, troubleshooting and full replacement of packaged rooftop units, including crane lifts, curb adapters and startup. All major brands."),
    ("service-tech.jpg", "Technicians on a maintenance visit", "clipboard", "Preventive maintenance agreements", "Scheduled visits with standard filters included, priority scheduling, 10% off repairs and a written report after every visit."),
    ("buildout.jpg", "Crew on a tenant build-out", "wrench", "Design-build mechanical", "Mechanical partner for general contractors from planning through closeout, on new construction and tenant build-outs."),
    ("ductwork.jpg", "Ductwork installation", "duct", "Ductwork and sheet metal", "Rectangular and spiral duct, exhaust fans and make-up air, installed clean and coordinated with the other trades."),
    ("rtu-new.jpg", "New rooftop heating and cooling units", "flame", "Heating and boilers", "Commercial heating repair and troubleshooting, boiler service and replacement, and CSD-1 testing."),
    ("chillers.jpg", "Commercial cooling equipment installation", "snow", "Cooling and refrigeration", "Air conditioning repair, airflow problems, VRF and ductless systems for offices and build-outs, and commercial refrigeration."),
])}
</div></section>

<section class="split"><div class="wrap split-inner">
<img src="/assets/img/lift-ductwork.jpg" alt="Crew installing ductwork from a scissor lift" width="1200" height="900">
<div>
<h2>Working with general contractors</h2>
<p>We bid, build and close out like a partner. Every project is led by a superintendent with 42 years of experience, with clean submittals, coordinated schedules and a crew that shows up ready to work.</p>
<p>Have plans out for bid? Send the project to <a href="mailto:Matt@DeeplyRootedHVAC.com">Matt@DeeplyRootedHVAC.com</a> or <a href="/contact?type=quote">request a quote</a>.</p>
</div>
</div></section>

<section class="offer"><div class="wrap offer-inner">
<img src="/assets/img/exhaust-fan.jpg" alt="Technician inspecting rooftop exhaust fan" width="1200" height="900">
<div>
<h2>Free Equipment Assessment</h2>
<p>We walk your rooftop units and give you a written condition report for each one, with repair recommendations and a replacement budget. It is the easiest way to plan next year's HVAC spending and to see what a maintenance agreement would cost.</p>
<a class="btn btn-gold" href="/contact?type=assessment">{icon("calendar", 20)} Book your free assessment</a>
</div>
</div></section>
{reviews_block(3)}
{values_block("How we work", "Our core values are how we treat your building, your people and your schedule.")}
{cta_band("Keep your building running.")}
"""

RESIDENTIAL = f"""<section class="page-hero" style="--hero:url('/assets/img/condenser.jpg')"><div class="wrap">
<p class="hero-slogan">{SLOGAN}</p>
<h1>Home heating and cooling you can trust like a friend.</h1>
<p>Repairs, replacements and maintenance for homes across {AREA}. Clear options, honest advice and a clean job site.</p>
{buttons(dark=True, plans=True)}
{rating_badge("on-dark")}
</div></section>

<section class="services"><div class="wrap">
<div class="section-head center"><h2>Residential services</h2><p>Everything your home needs to stay comfortable all year.</p></div>
<div class="res-split">
<div class="res-photos"><img src="/assets/img/furnace.jpg" alt="New furnace installation" loading="lazy"><img src="/assets/img/furnace-2.jpg" alt="Furnace and ductwork in a basement" loading="lazy"></div>
{icon_cards([
    ("flame", "Heating repair", "No heat, short cycling, strange noises, ignition problems and rooms that never warm up."),
    ("snow", "Air conditioning repair", "No cooling, weak airflow, frozen coils, leaks and uneven temperatures."),
    ("home", "New furnace and AC", "We help you choose the right system and install it right. Residential installs are primarily AirQuest systems."),
    ("thermo", "Boilers and radiant heat", "Boiler repair, service and replacement."),
    ("fan", "Ductless mini splits", "Installation and repair for additions, bonus rooms, garages and zoning."),
    ("duct", "Airflow and comfort", "Hot and cold rooms, stuffy air, filters, thermostat upgrades and duct improvements."),
])}
</div>
</div></section>

{values_block("What you can expect from us", "Our core values are the promise we make at your door.")}

<section class="offer"><div class="wrap offer-inner">
<img src="/assets/img/safety-vest.jpg" alt="Deeply Rooted Mechanical team member" width="1200" height="900">
<div>
<h2>Rooted Assurance Program</h2>
<p>Two tune-ups a year, priority scheduling and 10% off parts and labor. Plans start at $295 a year.</p>
<a class="btn btn-gold" href="/rooted-assurance-program">{icon("calendar", 20)} See the plans</a>
</div>
</div></section>
{reviews_block(6)}
{cta_band("Comfortable all year, starting today.")}
"""


def plan_cards():
    out = []
    for n, p, url, who, items in PLANS:
        lis = "".join(f"<li>{icon('check', 18)} {e(i)}</li>" for i in items)
        out.append(f'<div class="plan"><h3>{e(n)}</h3><p class="price">{p}<span> per year</span></p>'
                   f'<p class="who">{e(who)}</p><ul class="plan-list">{lis}</ul>'
                   f'<a class="btn btn-gold" href="{url}" rel="noopener">Join the {e(n)} plan</a></div>')
    return "".join(out)


PLANS_PAGE = f"""<section class="page-hero" style="--hero:url('/assets/img/furnace.jpg')"><div class="wrap">
<p class="hero-slogan">{SLOGAN}</p>
<h1>Rooted Assurance Program</h1>
<p>Our home maintenance plan. We schedule your visits so you never have to remember, and you get priority service when something goes wrong.</p>
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
])}
<p class="note center">Have a business? Ask about a commercial <a href="/contact?type=assessment">maintenance agreement</a>. It starts with a Free Equipment Assessment.</p>
</div></section>
{reviews_block(3)}
{cta_band("Questions about a plan?")}
"""

TRIBUTE = f"""<section class="tribute"><div class="wrap narrow">
<h2>Honoring Bill Purcell, a life of service</h2>
<div class="yt"><iframe src="https://www.youtube-nocookie.com/embed/{TRIBUTE_YOUTUBE}" title="In Memory of Bill Purcell - Deeply Rooted Mechanical" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>
</div></section>
"""

ABOUT = f"""<section class="page-hero" style="--hero:url('/assets/img/safety-vest.jpg')"><div class="wrap">
<p class="hero-slogan">{SLOGAN}</p>
<h1>About Deeply Rooted Mechanical</h1>
<p>We serve homes and businesses with excellent craftsmanship, faithful leadership and a commitment to treat every person with dignity.</p>
</div></section>

<section class="split"><div class="wrap split-inner">
<img src="/assets/img/crew-roof.jpg" alt="Deeply Rooted Mechanical crew setting rooftop equipment" width="1200" height="900">
<div>
<h2>Why we do what we do</h2>
<p>We do our work to honor God, not ourselves. We want to reflect His character through excellent craftsmanship, faithful leadership and the way we treat people.</p>
<p>Every person we work with, employees, customers and partners, is made in the image of God and worthy of dignity, care and respect. In an industry often marked by shortcuts and burnout, we exist to be different: to fix systems, honor people and restore what is broken.</p>
<p class="verse-inline">"{VERSE}" <b>{VERSE_REF}</b></p>
</div>
</div></section>

{values_block()}
{TRIBUTE}
{team_block()}

<section class="faq"><div class="wrap narrow">
<div class="section-head center"><h2>Frequently asked questions</h2></div>
<details><summary>What areas do you serve?</summary><p>All of Southeast Michigan, including Livingston, Oakland, Genesee and Wayne counties. Our office is in Brighton.</p></details>
<details><summary>What are your hours?</summary><p>Our office is open Monday to Friday, 7:00 AM to 4:30 PM. Emergency service is available 24/7: call {PHONE} and press 1.</p></details>
<details><summary>Do you offer guarantees or warranties?</summary><p>Yes. All work comes with a satisfaction guarantee, manufacturer warranties on installed equipment and a one-year workmanship guarantee.</p></details>
<details><summary>Do you do plumbing or electrical work?</summary><p>No. We are heating and cooling specialists. We coordinate with your plumber and electrician when a project needs them.</p></details>
<details><summary>What brands do you install?</summary><p>Commercially, all major brands. For homes, we primarily install AirQuest systems.</p></details>
<details><summary>How often should my system be serviced?</summary><p>At least once a year, and twice a year for best results: a spring cooling check and a fall heating check.</p></details>
</div></section>
{reviews_block(6)}
{cta_band()}
"""

CONTACT = f"""<section class="page-hero short"><div class="wrap">
<h1>Request service</h1>
<p>Tell us what is going on and we will get back to you quickly. For no heat, no cooling or anything urgent, call <a href="tel:{TEL}">{PHONE}</a> and press 1, any hour.</p>
</div></section>

<section class="contact"><div class="wrap contact-inner">
<form name="service-request" method="POST" action="/thanks" data-netlify="true" netlify-honeypot="company_website" class="request-form">
<input type="hidden" name="form-name" value="service-request">
<p class="hp"><label>Leave this empty <input name="company_website"></label></p>

<fieldset><legend>What do you need?</legend>
<div class="choices">
<label class="choice"><input type="radio" name="request_type" value="Service call" required><span>{icon("wrench", 22)} Service call<small>Something isn't working</small></span></label>
<label class="choice"><input type="radio" name="request_type" value="Free Equipment Assessment"><span>{icon("calendar", 22)} Free Equipment Assessment<small>Commercial buildings</small></span></label>
<label class="choice"><input type="radio" name="request_type" value="Quote"><span>{icon("clipboard", 22)} Quote<small>New system, replacement or project</small></span></label>
<label class="choice"><input type="radio" name="request_type" value="Maintenance / tune-up"><span>{icon("check", 22)} Maintenance<small>Tune-up or maintenance plan</small></span></label>
</div>
</fieldset>

<div class="grid2">
<fieldset><legend>Property type</legend>
<label class="pill"><input type="radio" name="property_type" value="Commercial" required> Commercial</label>
<label class="pill"><input type="radio" name="property_type" value="Residential"> Residential</label>
</fieldset>
<fieldset><legend>Is this an emergency?</legend>
<label class="pill"><input type="radio" name="emergency" value="Yes" required> Yes</label>
<label class="pill"><input type="radio" name="emergency" value="No"> No</label>
</fieldset>
</div>
<p class="small emergency-note">For an emergency, please also call {PHONE} and press 1.</p>

<label>Please describe the issue or project<textarea name="description" rows="5" required></textarea></label>

<div class="grid2">
<label>First name<input name="first_name" autocomplete="given-name" required></label>
<label>Last name<input name="last_name" autocomplete="family-name" required></label>
<label>Company (if commercial)<input name="company" autocomplete="organization"></label>
<label>Phone<input name="phone" type="tel" autocomplete="tel" required></label>
<label>Email<input name="email" type="email" autocomplete="email" required></label>
<label>Preferred contact method
<select name="preferred_contact"><option>Phone call</option><option>Text</option><option>Email</option></select></label>
<label class="span2">Street address<input name="street" autocomplete="street-address" required></label>
<label>City<input name="city" autocomplete="address-level2" required></label>
<label>ZIP code<input name="zip" autocomplete="postal-code" inputmode="numeric" required></label>
</div>

<label class="consent"><input type="checkbox" name="sms_consent_service" value="Yes"> I consent to receive non-marketing text messages from Deeply Rooted Mechanical LLC d/b/a Deeply Rooted HVAC about appointments, service updates, estimates, and customer support. Message frequency may vary. Message &amp; data rates may apply. Reply HELP for help. Reply STOP to opt out.</label>
<label class="consent"><input type="checkbox" name="sms_consent_marketing" value="Yes"> I consent to receive marketing text messages from Deeply Rooted Mechanical LLC d/b/a Deeply Rooted HVAC about special offers, discounts, and new product updates. Message frequency may vary. Message &amp; data rates may apply. Reply HELP for help or STOP to opt out.</label>
<p class="small">Texting is optional and not required to request service. See our <a href="/privacy-policy">Privacy Policy</a> and <a href="/terms-of-service">Terms of Service</a>.</p>
<button class="btn btn-gold btn-lg" type="submit">{icon("arrow", 20)} Submit request</button>
</form>

<aside class="contact-card">
<h2>Reach us</h2>
<p><strong>Call:</strong> <a href="tel:{TEL}">{PHONE}</a><br>Press 1 for service, 24/7</p>
<p><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p><strong>Office:</strong> {STREET}<br>{CITY}, {STATE} {ZIP}</p>
<p><strong>Hours:</strong> Mon to Fri, 7:00 AM to 4:30 PM<br>Emergency service 24/7</p>
<p><strong>Service area:</strong> All of Southeast Michigan</p>
<p><strong>General contractors:</strong> send bid invitations to <a href="mailto:Matt@DeeplyRootedHVAC.com">Matt@DeeplyRootedHVAC.com</a></p>
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

PAGES = [
    ("/", "index.html", "Commercial HVAC Contractor in Brighton, MI | Deeply Rooted Mechanical",
     "Commercial and residential heating and cooling across Southeast Michigan: rooftop unit repair and replacement, maintenance agreements, design-build, ductwork and 24/7 emergency service. 5.0 stars on Google. Call (810) 360-9664.", HOME),
    ("/Commercial", "Commercial/index.html", "Commercial HVAC Services, Rooftop Units and Maintenance | Deeply Rooted Mechanical",
     "Commercial HVAC for building owners, property managers and general contractors in Southeast Michigan: RTU repair and replacement, maintenance agreements, design-build, ductwork, boilers. Free Equipment Assessment.", COMMERCIAL),
    ("/Residential", "Residential/index.html", "Furnace, AC and Boiler Service for Homes | Deeply Rooted Mechanical",
     "Home heating and cooling repair, replacement and maintenance across Southeast Michigan. Honest options, clean work, 24/7 emergency service. Call (810) 360-9664.", RESIDENTIAL),
    ("/rooted-assurance-program", "rooted-assurance-program/index.html", "Rooted Assurance Program | Home HVAC Maintenance Plans",
     "Two tune-ups a year, priority scheduling and 10% off parts and labor. Furnace and AC $495, mini split $295, boiler $595 per year.", PLANS_PAGE),
    ("/about-us", "about-us/index.html", "About Us | Deeply Rooted Mechanical, Brighton, MI",
     "A faith-driven heating and cooling contractor serving homes and businesses across Southeast Michigan. Our core values and our team.", ABOUT),
    ("/contact", "contact/index.html", "Request Service | Deeply Rooted Mechanical",
     "Request HVAC service, a Free Equipment Assessment or a quote. 24/7 emergency service: call (810) 360-9664 and press 1.", CONTACT),
    ("/thanks", "thanks/index.html", "Thank You | Deeply Rooted Mechanical", "Your request was received.", THANKS),
    ("/privacy-policy", "privacy-policy/index.html", "Privacy Policy | Deeply Rooted Mechanical", "Privacy policy for deeplyrootedhvac.com and text messaging.", PRIVACY),
    ("/terms-of-service", "terms-of-service/index.html", "Terms of Service | Deeply Rooted Mechanical", "Terms of service for deeplyrootedhvac.com and text messaging.", TERMS),
    ("/404", "404.html", "Page Not Found | Deeply Rooted Mechanical", "Page not found.", NOTFOUND),
]

REDIRECTS = """# Old addresses from the previous site keep their rankings
/home                                  /                           301
/commercial                            /Commercial                 301
/residential                           /Residential                301
/about                                 /about-us                   301
/membership                            /rooted-assurance-program   301
/deeplyrootedhvac.com/privacy-policy   /privacy-policy             301
/deeplyrootedhvac.com/terms-of-service /terms-of-service           301
"""


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    for path, fname, title, desc, body in PAGES:
        dest = os.path.join(OUT, fname)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(page(path, title, desc, body))
    with open(os.path.join(OUT, "_redirects"), "w") as f:
        f.write(REDIRECTS)
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /thanks\n\nSitemap: {SITE}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE}{p}</loc></url>" for p, fn, *_ in PAGES if p not in ("/thanks", "/404"))
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print("built", len(PAGES), "pages into", OUT)


if __name__ == "__main__":
    build()
