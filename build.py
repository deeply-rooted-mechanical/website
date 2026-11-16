#!/usr/bin/env python3
"""Builds the deeplyrootedhvac.com static site into ./public.

Edit the PAGES content below, run `python3 build.py`, commit both build.py and public/.
Netlify publishes public/ as-is (no build step on Netlify).
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
HOURS = "Office: Mon to Fri, 7:00 AM to 4:30 PM. Emergency service 24/7."
AREA = "all of Southeast Michigan"
FACEBOOK = "https://www.facebook.com/profile.php?id=61579592821615"
LINKEDIN = "https://www.linkedin.com/company/deeply-rooted-mechanical"
YELP = "https://www.yelp.com/biz/deeply-rooted-brighton-2"
GOOGLE_REVIEW = "https://g.page/r/CSk16NMP1c2yEAE/review"
VERSE = "Rooted and built up in Him, established in the faith, overflowing with thankfulness."

PLANS = [
    ("Furnace and AC", "$495", "per year", "https://connect.intuit.com/portal/app/CommerceNetwork/view/scs-v1-d741d524baba4b41be768d5c2c191868422cca07cba14e92ac8d46c62c5ddaa0fe55ff92fabf47f3b2ccc54a9a123eab"),
    ("Ductless Mini Split", "$295", "per year", "https://connect.intuit.com/portal/app/CommerceNetwork/view/scs-v1-77f76ac06b3a4b2fa6e25d38d558ec6f4161a28fa0c14a04b7bd1b167e8acaaed6dea995f78e476bbd780709297c07e6"),
    ("Boiler", "$595", "per year", "https://connect.intuit.com/portal/app/CommerceNetwork/view/scs-v1-0bbab20d75cb4d25ac2c239e2003df9715a0741281614daf9bcada283a668c5d38213cd1c0f44802a84d909006a2a524"),
]

TEAM = [
    ("matt", "Matt Pastor", "Owner", ""),
    ("ken", "Ken Crider", "Superintendent", "42 years in the trade. Every project is led by Ken."),
    ("chase", "Chase Fackler", "Service Manager", ""),
    ("don", "Don Sleep", "Service Technician", "Six years in the U.S. Air Force, then refrigeration."),
    ("james", "James Gore", "HVAC Installer", ""),
    ("nick", "Nick Mooney", "HVAC Installer", ""),
]

VALUES = [
    ("A Teachable Spirit", "We never stop learning. We take joy in applying what we have learned and growing from what is next."),
    ("Faith", "We hold everything with open hands, trusting the One who holds tomorrow."),
    ("The Hard Right", "Integrity matters, even when no one is watching. We choose the hard right over the easy wrong."),
    ("The Bigger Picture", "Work is a gift, not our first priority. We strive for excellence but keep life and purpose in proper focus."),
    ("Servant-Leadership", "We lead by serving first, with humility, responsiveness and a can-do attitude toward our customers and our team."),
]

REVIEWS = [
    ("Joe Legato", "Commercial", "Deeply Rooted Mechanical has been fantastic to work with. I have had them replace one rooftop unit and repair two rooftop units. In both instances they were thorough, considerate of our property, considerate of our employees, and provided expert level of professionalism at every step of the process. The next time I am in need, Matt and his team will be my first call."),
    ("Andrew Beach", "Office furnace", "We called Deeply Rooted Mechanical the morning our furnace went out at our office. They were out same day to fix our furnace! Chase was super kind and personable as well as efficient. I highly recommend this company for all of your HVAC needs!"),
    ("Anthony Progar", "Boiler repair", "After our hydro-static boiler that provides radiant heat and hot water stopped working, we called Deeply Rooted Mechanical. We're extremely satisfied with the service. Chase showed up on time and listened as I explained the issue. He took his time looking things over and found a bad part which he replaced. He was very friendly, professional and thorough. The cost was very reasonable."),
    ("Steven Finlayson", "Furnace, AC and thermostat", "We needed the works, new A/C condenser, new furnace, new thermostat, you name it, and we were very pleased not only with the upgrade in equipment, but with the service provided. Matt and his crew were polite, respectful of our time, and very professional. I would recommend them to anyone that needs commercial or residential HVAC work!"),
    ("Kathy Flowers", "Heating repair", "Chase and Deeply Rooted Mechanical helped me solve my complicated issues regarding my furnace problems and heat distribution throughout my home. He communicated well, with integrity and respect, and worked to address the issue in a way that was least expensive. Highly recommend them!"),
    ("Laura C", "Service call", "Excellent service! Very prompt and professional! We called on a Monday afternoon and had a technician at our home by Tuesday afternoon to fix our system. They even talked me through how to turn off the water to my leaking humidifier via text Monday night."),
    ("Madeline Dunn", "Furnace and ductwork", "They fixed an overheating problem without adding extra lines and looked at the bigger picture. They were professional, took their shoes off, and even made sure my furnace didn't overheat. I interviewed three HVAC companies and definitely made the right choice. They treated us like family and offered a fair price."),
    ("Corey De Luca", "Owner", "The owner Matt is hands down one of the nicest business owners I've interacted with. He listened to my concerns and explained everything thoroughly. The technician was extremely kind, knowledgeable and honest. I highly recommend them!"),
]

NAV = [("/", "Home"), ("/Commercial", "Commercial"), ("/Residential", "Residential"),
       ("/rooted-assurance-program", "Maintenance Plans"), ("/about-us", "About"), ("/contact", "Contact")]

e = html.escape


def schema():
    return {
        "@context": "https://schema.org",
        "@type": "HVACBusiness",
        "name": NAME,
        "legalName": LEGAL,
        "url": SITE + "/",
        "logo": SITE + "/assets/logo.png",
        "image": SITE + "/assets/img/rtu-crane.jpg",
        "telephone": PHONE,
        "email": EMAIL,
        "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY,
                    "addressRegion": STATE, "postalCode": ZIP, "addressCountry": "US"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                                       "opens": "07:00", "closes": "16:30"}],
        "areaServed": [{"@type": "AdministrativeArea", "name": n} for n in
                       ["Southeast Michigan", "Livingston County, MI", "Oakland County, MI",
                        "Genesee County, MI", "Wayne County, MI"]],
        "knowsAbout": ["Commercial HVAC", "Rooftop unit (RTU) replacement", "Commercial HVAC maintenance agreements",
                       "Design-build HVAC", "Tenant build-out HVAC", "Sheet metal ductwork", "Boiler service",
                       "Ductless mini split systems", "Furnace repair", "Air conditioning repair"],
        "slogan": "Rooted in Faith. Built on Trust.",
        "sameAs": [FACEBOOK, LINKEDIN, YELP],
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
<span>Serving {AREA}. 24/7 emergency service.</span>
<a href="tel:{TEL}">Call {PHONE}</a>
</div></div>
<header class="site"><div class="wrap">
<a class="brand" href="/"><img src="/assets/logo.png" alt="{NAME} logo" width="64" height="64"><span>Deeply Rooted<small>Mechanical</small></span></a>
<nav aria-label="Main">{links}</nav>
<a class="btn btn-primary hdr-cta" href="/contact?type=service">Request Service</a>
</div></header>
<main>
"""


def footer():
    return f"""</main>
<section class="verse"><div class="wrap">
<p class="verse-text">"{VERSE}"</p>
<p class="verse-ref">Colossians 2:7</p>
<p class="tag">Rooted in Faith. Built on Trust. Thankful in All.</p>
</div></section>
<footer class="site"><div class="wrap cols">
<div>
<img src="/assets/logo.png" alt="" width="72" height="72">
<p><strong>{NAME}</strong><br>{STREET}<br>{CITY}, {STATE} {ZIP}</p>
</div>
<div>
<h3>Contact</h3>
<p><a href="tel:{TEL}">{PHONE}</a> (press 1 for service)<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p>{HOURS}</p>
</div>
<div>
<h3>Services</h3>
<p><a href="/Commercial">Commercial HVAC</a><br><a href="/Residential">Residential HVAC</a><br><a href="/rooted-assurance-program">Maintenance plans</a><br><a href="/contact?type=assessment">Free Equipment Assessment</a></p>
</div>
<div>
<h3>Follow and review</h3>
<p><a href="{FACEBOOK}" rel="noopener">Facebook</a><br><a href="{LINKEDIN}" rel="noopener">LinkedIn</a><br><a href="{YELP}" rel="noopener">Yelp</a><br><a href="{GOOGLE_REVIEW}" rel="noopener">Leave us a Google review</a></p>
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


def cta_band(text="Ready when you are."):
    return f"""<section class="cta-band"><div class="wrap">
<h2>{text}</h2>
<div class="cta-row">
<a class="btn btn-primary" href="/contact?type=service">Request Service</a>
<a class="btn btn-gold" href="/contact?type=assessment">Free Equipment Assessment</a>
<a class="btn btn-light" href="/contact?type=quote">Request a Quote</a>
</div>
<p class="cta-phone">Or call <a href="tel:{TEL}">{PHONE}</a>. Press 1 for service, 24/7.</p>
</div></section>
"""


def reviews_block(n=6):
    cards = "".join(
        f'<figure class="review"><div class="stars" aria-label="5 stars">&#9733;&#9733;&#9733;&#9733;&#9733;</div>'
        f'<blockquote>{e(t)}</blockquote><figcaption>{e(name)}<span>{e(kind)}</span></figcaption></figure>'
        for name, kind, t in REVIEWS[:n])
    return f"""<section class="reviews"><div class="wrap">
<div class="section-head"><h2>What our customers say</h2>
<p class="google">5.0 stars on Google. <a href="{GOOGLE_REVIEW}" rel="noopener">Leave us a review</a></p></div>
<div class="review-grid">{cards}</div>
</div></section>
"""


def team_block():
    cards = "".join(
        f'<figure class="person"><img src="/assets/team/{k}.jpg" alt="{e(n)}, {e(t)}" width="400" height="400">'
        f'<figcaption><strong>{e(n)}</strong><span>{e(t)}</span>{"<em>" + e(x) + "</em>" if x else ""}</figcaption></figure>'
        for k, n, t, x in TEAM)
    return f"""<section class="team"><div class="wrap">
<div class="section-head"><h2>Meet the team</h2><p>Local people you will see on your roof and in your mechanical room.</p></div>
<div class="team-grid">{cards}</div>
</div></section>
"""


def values_block():
    items = "".join(f"<li><h3>Deeply Rooted in {e(t)}</h3><p>{e(d)}</p></li>" for t, d in VALUES)
    return f"""<section class="values"><div class="wrap">
<div class="section-head"><h2>Our core values</h2></div>
<ul class="value-list">{items}</ul>
</div></section>
"""


HOME = f"""<section class="hero" style="--hero:url('/assets/img/rtu-crane.jpg')"><div class="wrap">
<div class="hero-copy">
<h1>Commercial HVAC you can count on, across Southeast Michigan.</h1>
<p>Rooftop unit repair and replacement, maintenance agreements, design-build and tenant build-outs, and 24/7 emergency service for building owners, property managers and general contractors. Homeowners too.</p>
<div class="cta-row">
<a class="btn btn-primary" href="/contact?type=service">Request Service</a>
<a class="btn btn-gold" href="/contact?type=assessment">Free Equipment Assessment</a>
<a class="btn btn-light" href="/contact?type=quote">Request a Quote</a>
</div>
<p class="hero-phone">No heat or no cooling? Call <a href="tel:{TEL}">{PHONE}</a>, press 1. We answer 24/7.</p>
</div>
</div></section>

<section class="paths"><div class="wrap">
<a class="path" href="/Commercial"><img src="/assets/img/rooftop-units.jpg" alt="DRM crew setting new rooftop units" loading="lazy"><div><h2>For your business</h2><p>RTUs, make-up air and exhaust, boilers, VRF and ductless, ductwork and preventive maintenance agreements. Built for uptime.</p><span class="more">Commercial HVAC</span></div></a>
<a class="path" href="/Residential"><img src="/assets/img/furnace.jpg" alt="New furnace installed by Deeply Rooted Mechanical" loading="lazy"><div><h2>For your home</h2><p>Furnace, air conditioning, boiler and mini split repair and replacement, plus our Rooted Assurance maintenance plan.</p><span class="more">Residential HVAC</span></div></a>
</div></section>

<section class="services"><div class="wrap">
<div class="section-head"><h2>What we do</h2><p>Heating and cooling, done right the first time.</p></div>
<ul class="svc-grid">
<li><h3>Rooftop unit repair and replacement</h3><p>Diagnosis, repair and full RTU changeouts, including crane lifts, curbs and startup.</p></li>
<li><h3>Maintenance agreements</h3><p>Scheduled visits with filters included, priority scheduling, 10% off repairs and a written report after every visit.</p></li>
<li><h3>Design-build and build-outs</h3><p>Mechanical partner for general contractors on new construction and tenant build-outs, from planning to closeout.</p></li>
<li><h3>Ductwork and sheet metal</h3><p>Rectangular and spiral duct, exhaust and make-up air, installed clean and on schedule.</p></li>
<li><h3>Boilers and hydronics</h3><p>Boiler repair, replacement and CSD-1 testing for commercial boilers.</p></li>
<li><h3>24/7 emergency service</h3><p>No heat, no cooling, or a unit down on a busy day. Call and press 1, any hour.</p></li>
</ul>
</div></section>

<section class="offer"><div class="wrap offer-inner">
<img src="/assets/img/exhaust-fan.jpg" alt="Technician inspecting rooftop exhaust fan" loading="lazy">
<div>
<h2>Free Equipment Assessment</h2>
<p>We walk your rooftop units and mechanical equipment and give you a written condition report for every unit: what is good, what to watch, and what to budget for. No cost and no obligation.</p>
<a class="btn btn-gold" href="/contact?type=assessment">Book your free assessment</a>
</div>
</div></section>

{reviews_block(6)}
{team_block()}
{cta_band("Let us serve you!")}
"""

COMMERCIAL = f"""<section class="page-hero" style="--hero:url('/assets/img/rooftop-units.jpg')"><div class="wrap">
<h1>Commercial HVAC and mechanical services built for uptime.</h1>
<p>For facility managers, property managers, general contractors and multi-site operators across {AREA}.</p>
<div class="cta-row"><a class="btn btn-primary" href="/contact?type=service">Request Service</a><a class="btn btn-gold" href="/contact?type=assessment">Free Equipment Assessment</a><a class="btn btn-light" href="/contact?type=quote">Request a Quote</a></div>
</div></section>

<section class="services"><div class="wrap">
<div class="section-head"><h2>Commercial service capabilities</h2></div>
<ul class="svc-grid">
<li><h3>Rooftop units</h3><p>Repair, troubleshooting and full replacement of packaged rooftop units, including crane lifts, curb adapters and startup. All major brands.</p></li>
<li><h3>Preventive maintenance agreements</h3><p>Scheduled visits with standard filters included, priority scheduling, 10% off repairs for members and a written report after every visit.</p></li>
<li><h3>Design-build mechanical</h3><p>Mechanical partner for general contractors from planning through closeout, on new construction and tenant build-outs.</p></li>
<li><h3>Ductwork and sheet metal</h3><p>Rectangular and spiral duct, exhaust fans and make-up air, installed clean and coordinated with the other trades.</p></li>
<li><h3>Heating and boilers</h3><p>Commercial heating repair and troubleshooting, boiler service and replacement, and CSD-1 testing.</p></li>
<li><h3>Cooling and refrigeration</h3><p>Air conditioning repair, airflow problems, VRF and ductless mini split systems for offices and build-outs, and commercial refrigeration.</p></li>
</ul>
</div></section>

<section class="split"><div class="wrap split-inner">
<img src="/assets/img/lift-ductwork.jpg" alt="Crew installing ductwork from a scissor lift" loading="lazy">
<div>
<h2>Working with general contractors</h2>
<p>We bid, build and close out like a partner. Every project is led by a superintendent with 42 years of experience, with clean submittals, coordinated schedules and a crew that shows up ready to work.</p>
<p>Have plans out for bid? <a href="/contact?type=quote">Send us the project</a> or email <a href="mailto:Matt@DeeplyRootedHVAC.com">Matt@DeeplyRootedHVAC.com</a>.</p>
</div>
</div></section>

<section class="offer"><div class="wrap offer-inner">
<img src="/assets/img/rtu-crane.jpg" alt="New rooftop unit being lifted by crane" loading="lazy">
<div>
<h2>Free Equipment Assessment</h2>
<p>We walk your rooftop units and give you a written condition report for each one, with repair recommendations and a replacement budget. It is the easiest way to plan next year's HVAC spending and to see what a maintenance agreement would cost.</p>
<a class="btn btn-gold" href="/contact?type=assessment">Book your free assessment</a>
</div>
</div></section>
{reviews_block(3)}
{cta_band("Keep your building running.")}
"""

RESIDENTIAL = f"""<section class="page-hero" style="--hero:url('/assets/img/condenser.jpg')"><div class="wrap">
<h1>Home heating and cooling service you can trust like a friend.</h1>
<p>Repairs, replacements and maintenance for homes across {AREA}. Clear options, honest advice and a clean job site.</p>
<div class="cta-row"><a class="btn btn-primary" href="/contact?type=service">Request Service</a><a class="btn btn-gold" href="/rooted-assurance-program">Maintenance Plans</a><a class="btn btn-light" href="/contact?type=quote">Request a Quote</a></div>
</div></section>

<section class="services"><div class="wrap">
<div class="section-head"><h2>Residential services</h2></div>
<ul class="svc-grid">
<li><h3>Heating repair</h3><p>No heat, short cycling, strange noises, ignition problems and rooms that never warm up.</p></li>
<li><h3>Air conditioning repair</h3><p>No cooling, weak airflow, frozen coils, leaks and uneven temperatures.</p></li>
<li><h3>New furnace and AC</h3><p>We help you choose the right system and install it right. Residential installs are primarily AirQuest systems.</p></li>
<li><h3>Boilers</h3><p>Boiler and radiant heat repair, service and replacement.</p></li>
<li><h3>Ductless mini splits</h3><p>Installation and repair for additions, bonus rooms, garages and zoning.</p></li>
<li><h3>Airflow and comfort</h3><p>Hot and cold rooms, stuffy air, filters, thermostat upgrades and duct improvements.</p></li>
</ul>
</div></section>

<section class="steps"><div class="wrap">
<div class="section-head"><h2>What to expect</h2></div>
<ol class="step-list">
<li><h3>We listen</h3><p>Tell us what is happening. We ask the right questions before we touch anything.</p></li>
<li><h3>We explain</h3><p>Plain language and honest options, including what we would do in our own home.</p></li>
<li><h3>We fix it and clean up</h3><p>Work done right, explained when we are finished, and your home left clean.</p></li>
</ol>
</div></section>

<section class="offer"><div class="wrap offer-inner">
<img src="/assets/img/furnace.jpg" alt="Furnace installation" loading="lazy">
<div>
<h2>Rooted Assurance Program</h2>
<p>Two tune-ups a year, priority scheduling and 10% off parts and labor. Plans start at $295 a year.</p>
<a class="btn btn-gold" href="/rooted-assurance-program">See the plans</a>
</div>
</div></section>
{reviews_block(6)}
{cta_band("Comfortable all year, starting today.")}
"""

plan_cards = "".join(
    f'<div class="plan"><h3>{e(n)}</h3><p class="price">{p}<span> {u}</span></p>'
    f'<a class="btn btn-primary" href="{url}" rel="noopener">Join now</a></div>'
    for n, p, u, url in PLANS)

PLANS_PAGE = f"""<section class="page-hero short"><div class="wrap">
<h1>Rooted Assurance Program</h1>
<p>Our home maintenance plan. We schedule the visits so you never have to remember.</p>
</div></section>

<section class="services"><div class="wrap">
<div class="section-head"><h2>What every plan includes</h2></div>
<ul class="svc-grid">
<li><h3>Two visits a year</h3><p>A spring cooling tune-up and a fall heating tune-up. We call you to schedule.</p></li>
<li><h3>Priority scheduling</h3><p>Members move to the front of the line when something goes wrong.</p></li>
<li><h3>10% off parts and labor</h3><p>On every repair, plus reduced emergency visit premiums.</p></li>
<li><h3>Fewer breakdowns</h3><p>Small problems get caught early, which helps your equipment last longer.</p></li>
</ul>
</div></section>

<section class="plans"><div class="wrap">
<div class="section-head"><h2>Choose your plan</h2><p>Billed yearly through our secure QuickBooks checkout.</p></div>
<div class="plan-grid">{plan_cards}</div>
<p class="note">Have a business? Ask about a commercial <a href="/contact?type=assessment">maintenance agreement</a>. It starts with a Free Equipment Assessment.</p>
</div></section>
{reviews_block(3)}
{cta_band("Questions about a plan?")}
"""

ABOUT = f"""<section class="page-hero short"><div class="wrap">
<h1>About Deeply Rooted Mechanical</h1>
<p>We serve homes and businesses with excellent craftsmanship, faithful leadership and a commitment to treat every person with dignity.</p>
</div></section>

<section class="split"><div class="wrap split-inner">
<img src="/assets/img/safety-vest.jpg" alt="Deeply Rooted Mechanical crew member on a job site" loading="lazy">
<div>
<h2>Why we do what we do</h2>
<p>We do our work to honor God, not ourselves. We want to reflect His character through excellent craftsmanship, faithful leadership and the way we treat people.</p>
<p>Every person we work with, employees, customers and partners, is made in the image of God and worthy of dignity, care and respect. In an industry often marked by shortcuts and burnout, we exist to be different: to fix systems, honor people and restore what is broken.</p>
</div>
</div></section>

<section class="tribute"><div class="wrap">
<h2>Honoring Bill Purcell, a life of service</h2>
<p>Bill helped shape the way we serve our customers and lead our team. We carry his example with us on every job.</p>
</div></section>

{values_block()}
{team_block()}

<section class="faq"><div class="wrap">
<div class="section-head"><h2>Frequently asked questions</h2></div>
<details><summary>What areas do you serve?</summary><p>All of Southeast Michigan, including Livingston, Oakland, Genesee and Wayne counties. Our office is in Brighton.</p></details>
<details><summary>What are your hours?</summary><p>Our office is open Monday to Friday, 7:00 AM to 4:30 PM. Emergency service is available 24/7: call {PHONE} and press 1.</p></details>
<details><summary>Do you offer guarantees or warranties?</summary><p>Yes. All work comes with a satisfaction guarantee, manufacturer warranties on installed equipment and a one-year workmanship guarantee.</p></details>
<details><summary>Do you do plumbing or electrical work?</summary><p>No. We are heating and cooling specialists. We coordinate with your plumber and electrician when a project needs them.</p></details>
<details><summary>What brands do you install?</summary><p>Commercially, all major brands. For homes, we primarily install AirQuest systems.</p></details>
<details><summary>How often should my system be serviced?</summary><p>At least once a year, and twice a year for best results: a spring cooling check and a fall heating check.</p></details>
</div></section>
{reviews_block(8)}
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
<label class="choice"><input type="radio" name="request_type" value="Service call" required> Service call (something isn't working)</label>
<label class="choice"><input type="radio" name="request_type" value="Free Equipment Assessment"> Free Equipment Assessment (commercial)</label>
<label class="choice"><input type="radio" name="request_type" value="Quote"> Quote (new system, replacement or project)</label>
<label class="choice"><input type="radio" name="request_type" value="Maintenance / tune-up"> Maintenance or tune-up</label>
</fieldset>

<fieldset><legend>Property type</legend>
<label class="choice"><input type="radio" name="property_type" value="Commercial" required> Commercial</label>
<label class="choice"><input type="radio" name="property_type" value="Residential"> Residential</label>
</fieldset>

<fieldset><legend>Is this an emergency?</legend>
<label class="choice"><input type="radio" name="emergency" value="Yes" required> Yes (please also call {PHONE}, press 1)</label>
<label class="choice"><input type="radio" name="emergency" value="No"> No</label>
</fieldset>

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
<button class="btn btn-primary" type="submit">Submit request</button>
</form>

<aside class="contact-card">
<h2>Reach us</h2>
<p><strong>Call:</strong> <a href="tel:{TEL}">{PHONE}</a><br>Press 1 for service, 24/7</p>
<p><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p><strong>Office:</strong> {STREET}<br>{CITY}, {STATE} {ZIP}</p>
<p><strong>Hours:</strong> Mon to Fri, 7:00 AM to 4:30 PM<br>Emergency service 24/7</p>
<p><strong>Service area:</strong> {AREA[0].upper() + AREA[1:]}</p>
<p><strong>General contractors:</strong> send bid invitations to <a href="mailto:Matt@DeeplyRootedHVAC.com">Matt@DeeplyRootedHVAC.com</a></p>
</aside>
</div></section>
"""

THANKS = f"""<section class="page-hero short"><div class="wrap">
<h1>Thank you! We got your request.</h1>
<p>Our team will reach out shortly during business hours. If this is an emergency, please call <a href="tel:{TEL}">{PHONE}</a> and press 1 so we can help right away.</p>
<div class="cta-row"><a class="btn btn-light" href="/">Back to home</a></div>
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
     "Commercial and residential heating and cooling across Southeast Michigan: rooftop unit repair and replacement, maintenance agreements, design-build, ductwork and 24/7 emergency service. Call (810) 360-9664.", HOME),
    ("/Commercial", "Commercial/index.html", "Commercial HVAC Services, Rooftop Units and Maintenance | Deeply Rooted Mechanical",
     "Commercial HVAC for building owners, property managers and general contractors in Southeast Michigan: RTU repair and replacement, maintenance agreements, design-build, ductwork, boilers. Free Equipment Assessment.", COMMERCIAL),
    ("/Residential", "Residential/index.html", "Furnace, AC and Boiler Service for Homes | Deeply Rooted Mechanical",
     "Home heating and cooling repair, replacement and maintenance across Southeast Michigan. Honest options, clean work, 24/7 emergency service. Call (810) 360-9664.", RESIDENTIAL),
    ("/rooted-assurance-program", "rooted-assurance-program/index.html", "Rooted Assurance Program | Home HVAC Maintenance Plans",
     "Two tune-ups a year, priority scheduling and 10% off parts and labor. Furnace and AC $495, mini split $295, boiler $595 per year.", PLANS_PAGE),
    ("/about-us", "about-us/index.html", "About Us | Deeply Rooted Mechanical, Brighton, MI",
     "A faith-driven heating and cooling contractor serving homes and businesses across Southeast Michigan. Meet the team and our core values.", ABOUT),
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
