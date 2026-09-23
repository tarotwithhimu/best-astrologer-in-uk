#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates the UK build of the Himu astrology site:
  - index.html
  - best-astrologer-in-<city>.html  (one per city in usa_data.CITIES)

Same design system as the India and Bangladesh builds. Curated list of
well-known cities only — not a page per town/ZIP code — with genuinely
distinct copy per city and honest claims (no unverified local track record,
no fake competitor listings, no invented testimonials).
"""
import os
import json
import datetime
from uk_data import (
    PHONE, PHONE_DISPLAY, WA, EMAIL, SITE_BASE, STUDIO_ADDRESS,
    NATIONS, CITIES, CITY_BY_SLUG, CITIES_BY_NATION,
    BLOG_POSTS, BLOG_BY_SLUG,
)

OUT = os.path.dirname(os.path.abspath(__file__))
WA_TEXT = "Hello%20Himu%2C%20I%20want%20to%20book%20a%20tarot/astrology%20reading%20session"
BUILD_DATE = datetime.date.today().isoformat()


def clip(text, limit):
    """Hard-cap title/meta text to a search-engine-safe length, cutting at a
    word boundary, so results don't get silently truncated/rewritten by Google."""
    if len(text) <= limit:
        return text
    truncated = text[:limit - 1].rsplit(" ", 1)[0]
    return truncated.rstrip(",.-\u2013\u2014") + "\u2026"


def breadcrumb(items):
    """items: list of (href_or_None, label). href=None marks the current page."""
    lis = "\n".join(
        f'            <li aria-current="page">{label}</li>' if href is None
        else f'            <li><a href="{href}">{label}</a></li>'
        for href, label in items
    )
    return f'''<div class="breadcrumb-bar">
    <div class="container">
        <ol>
{lis}
        </ol>
    </div>
</div>'''


def ld_breadcrumb(items):
    elements = []
    for i, (href, label) in enumerate(items, start=1):
        url = f"{SITE_BASE}/" if href == "index.html" else (f"{SITE_BASE}/{href}" if href else None)
        entry = {"@type": "ListItem", "position": i, "name": label}
        if url:
            entry["item"] = url
        elements.append(entry)
    return json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": elements})


def nearby_cities(current_slug, n=3):
    """Deterministic pick of other cities for cross-linking (internal SEO +
    lets a visitor easily check a neighbouring city's page)."""
    others = [c for c in CITIES if c["slug"] != current_slug]
    offset = sum(ord(ch) for ch in current_slug) % len(others)
    picked = (others[offset:] + others[:offset])[:n]
    return picked

LOGO_MARK = ('<svg class="logo-mark" viewBox="0 0 32 32" aria-hidden="true">'
             '<path d="M20.5 4.5c-6 1.2-10 6.4-10 12.2 0 6.9 5.6 12.5 12.5 12.5 2 0 3.9-.5 5.5-1.3'
             '-2.6 3.5-6.8 5.6-11.4 5.6C9.6 33.5 3 26.9 3 18.9S9.6 4.3 17.1 4.3c1.2 0 2.3.1 3.4.2z" '
             'fill="currentColor" transform="translate(0,-2.3) scale(0.86)"/>'
             '<circle cx="24.5" cy="7.5" r="1.4" fill="currentColor"/>'
             '<circle cx="27.5" cy="12.5" r="0.9" fill="currentColor"/>'
             '<circle cx="21" cy="11" r="0.7" fill="currentColor"/></svg>')

NAV_CITIES = ["london", "manchester", "birmingham", "edinburgh", "glasgow", "cardiff"]


def whatsapp_url(text=WA_TEXT):
    return f"https://wa.me/{WA}?text={text}"


def nav(active_href="index.html"):
    dd_items = "\n".join(
        f'                        <a href="best-astrologer-in-{s}.html">Best Astrologer in {CITY_BY_SLUG[s]["name"]}</a>'
        for s in NAV_CITIES
    )
    def cls(href):
        return ' class="active"' if href == active_href else ''
    return f'''<div class="whatsapp-float">
    <a href="{whatsapp_url()}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3C7 3 3 6.8 3 11.5c0 2 .8 3.9 2.1 5.3L4 21l4.4-1.3c1.1.5 2.3.8 3.6.8 5 0 9-3.8 9-8.5S17 3 12 3z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M8.7 10.4c.4 2.3 2.3 4.1 4.6 4.5.6.1 1-.5.7-1l-.7-1.1c-.2-.3-.6-.4-.9-.2l-.5.3c-.7-.4-1.4-1.1-1.8-1.8l.3-.5c.2-.3.1-.7-.2-.9l-1.1-.7c-.5-.3-1.1.1-1 .7z" fill="currentColor"/></svg></a>
</div>
<nav class="navbar">
    <div class="container nav-container">
        <div class="logo">
            <a href="index.html" style="text-decoration:none;">
                <p class="logo-title">{LOGO_MARK}Best Astrologer in the UK</p>
            </a>
            <p>Himu — Vedic Astrology • Tarot • Numerology • Vastu, Online</p>
        </div>
        <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M2 5h16M2 10h16M2 15h16" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
        </button>
        <ul class="nav-links">
            <li><a href="index.html"{cls("index.html")}>Home</a></li>
            <li><a href="index.html#why"{cls("index.html#why")}>Why Us</a></li>
            <li class="has-dropdown">
                <a href="index.html#cities" class="dropdown-toggle">Cities ▾</a>
                <div class="dropdown-menu">
{dd_items}
                    <a class="view-all" href="index.html#cities">View All Cities →</a>
                </div>
            </li>
            <li><a href="index.html#services">Services</a></li>
            <li><a href="blog.html"{cls("blog.html")}>Blog</a></li>
            <li><a href="index.html#pricing">Pricing</a></li>
            <li><a href="index.html#contact">Contact</a></li>
            <li><a href="{whatsapp_url()}" class="btn-consult" target="_blank" rel="noopener">Book Session</a></li>
        </ul>
    </div>
</nav>
'''


def footer():
    a = NAV_CITIES[:3]
    b = NAV_CITIES[3:] + ["belfast", "leeds", "bristol"]
    city_links_a = "\n".join(
        f'                    <li><a href="best-astrologer-in-{s}.html">{CITY_BY_SLUG[s]["name"]}</a></li>' for s in a
    )
    city_links_b = "\n".join(
        f'                    <li><a href="best-astrologer-in-{s}.html">{CITY_BY_SLUG[s]["name"]}</a></li>' for s in b
    )
    blog_links = "\n".join(
        f'                    <li><a href="blog-{p["slug"]}.html">{p["title"]}</a></li>' for p in BLOG_POSTS[:4]
    )
    return f'''<footer>
    <div class="container">
        <div class="footer-grid">
            <div>
                <h4>Best Astrologer — Online for the UK</h4>
                <p class="footer-blurb">Himu — Vedic Astrology, Tarot, Numerology &amp; Vastu, available online for clients across the United Kingdom.</p>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="index.html#services">Services</a></li>
                    <li><a href="blog.html">Blog</a></li>
                    <li><a href="index.html#pricing">Pricing</a></li>
                </ul>
            </div>
            <div>
                <h4>Popular Cities</h4>
                <ul>
{city_links_a}
                </ul>
            </div>
            <div>
                <h4>More Cities</h4>
                <ul>
{city_links_b}
                </ul>
            </div>
            <div>
                <h4>From the Blog</h4>
                <ul>
{blog_links}
                </ul>
            </div>
            <div>
                <h4>Contact</h4>
                <ul>
                    <li><a href="tel:{PHONE}">{PHONE_DISPLAY}</a></li>
                    <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
                    <li><a href="https://www.facebook.com/tarotwithhimu" target="_blank" rel="noopener">Facebook</a></li>
                    <li><a href="https://www.instagram.com/tarotwithhimu" target="_blank" rel="noopener">Instagram</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-bottom">
            <p>© 2026 Himu — Vedic Astrologer &amp; Tarot Reader, Online for the UK</p>
            <p class="footer-small">Consultations conducted online via WhatsApp/video call from Himu's studio in Guwahati, India | Numerology | Vastu Consultant</p>
        </div>
    </div>
</footer>
<button id="backToTop" class="back-to-top" aria-label="Back to top" type="button">
    <svg width="18" height="18" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M10 15V5M10 5l-5 5M10 5l5 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
</button>
<script src="script.js"></script>
<div class="sticky-cta">
    <a class="sc-wa" href="{whatsapp_url()}" target="_blank" rel="noopener">WhatsApp</a>
    <a class="sc-call" href="tel:{PHONE}">Call Now</a>
</div>
'''


def services_section():
    return '''<section id="services" class="services">
    <div class="container">
        <h2 class="section-title">Astrology, Tarot, Numerology &amp; Vastu Services</h2>
        <p class="section-subtitle">The complete offering, delivered online for clients anywhere in the United Kingdom</p>
        <div class="services-grid">
            <div class="service-card">
                <div class="icon icon-tarot"><svg viewBox="0 0 40 40" aria-hidden="true"><rect x="10" y="6" width="14" height="22" rx="2" transform="rotate(-8 17 17)" fill="none" stroke="currentColor" stroke-width="1.6"/><rect x="16" y="10" width="14" height="22" rx="2" transform="rotate(8 23 21)" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="23" cy="21" r="2.4" fill="currentColor"/></svg></div>
                <h3>Tarot Reading</h3>
                <p>In-depth past, present &amp; future insights for clarity in relationships, career &amp; decisions.</p>
                <ul>
                    <li>Love &amp; relationship tarot</li>
                    <li>Career &amp; decision-making spreads</li>
                    <li>Yes/No &amp; timing questions</li>
                </ul>
            </div>
            <div class="service-card">
                <div class="icon icon-moon"><svg viewBox="0 0 40 40" aria-hidden="true"><path d="M25 8c-7 1-12 7-12 14s5 13 12 14c-2.6 1.3-5.6 2-8.7 2C7 38 1 30.8 1 22S7 6 16.3 6c3.1 0 6.1.7 8.7 2z" transform="translate(6,-2)" fill="currentColor"/><circle cx="30" cy="10" r="1.3" fill="currentColor"/><circle cx="33" cy="15" r="0.9" fill="currentColor"/></svg></div>
                <h3>Vedic Astrology</h3>
                <p>Vedic birth chart (Kundli) analysis, planetary remedies, and life predictions.</p>
                <ul>
                    <li>Birth chart &amp; Dasha analysis</li>
                    <li>Marriage &amp; Kundli matching</li>
                    <li>Planetary remedies</li>
                </ul>
            </div>
            <div class="service-card">
                <div class="icon icon-number"><svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="13" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M17 14v12M14 14h6M14 26h6M23 26l4-12h-4.5M23 26h5" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
                <h3>Numerology</h3>
                <p>Decode your date of birth, name numbers, and unlock your soul's blueprint.</p>
                <ul>
                    <li>Life path number reading</li>
                    <li>Name correction guidance</li>
                    <li>Lucky number &amp; date selection</li>
                </ul>
            </div>
            <div class="service-card">
                <div class="icon icon-home"><svg viewBox="0 0 40 40" aria-hidden="true"><path d="M8 19 20 9l12 10" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M11 17v13h18V17" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M17 30v-7h6v7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg></div>
                <h3>Vastu Consultation</h3>
                <p>Harmonize home &amp; office energies for prosperity and peace.</p>
                <ul>
                    <li>Home &amp; office Vastu audit</li>
                    <li>Simple, low-cost remedies</li>
                    <li>New construction guidance</li>
                </ul>
            </div>
        </div>
    </div>
</section>
'''


def why_section():
    return '''<section id="why" class="why-choose">
    <div class="container">
        <h2 class="section-title">Why Clients Choose Himu</h2>
        <p class="section-subtitle">What a good online astrology consultation should feel like — trust, accuracy and genuine care</p>
        <div class="why-grid">
            <div class="why-card">
                <div class="icon icon-tarot"><svg viewBox="0 0 40 40" aria-hidden="true"><rect x="10" y="6" width="14" height="22" rx="2" transform="rotate(-8 17 17)" fill="none" stroke="currentColor" stroke-width="1.6"/><rect x="16" y="10" width="14" height="22" rx="2" transform="rotate(8 23 21)" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="23" cy="21" r="2.4" fill="currentColor"/></svg></div>
                <h3>Certified &amp; Experienced</h3>
                <p>8+ years reading for clients, trained in Vedic astrology, tarot and numerology.</p>
            </div>
            <div class="why-card">
                <div class="icon icon-moon"><svg viewBox="0 0 40 40" aria-hidden="true"><path d="M25 8c-7 1-12 7-12 14s5 13 12 14c-2.6 1.3-5.6 2-8.7 2C7 38 1 30.8 1 22S7 6 16.3 6c3.1 0 6.1.7 8.7 2z" transform="translate(6,-2)" fill="currentColor"/><circle cx="30" cy="10" r="1.3" fill="currentColor"/><circle cx="33" cy="15" r="0.9" fill="currentColor"/></svg></div>
                <h3>Accurate, Practical Guidance</h3>
                <p>Predictions paired with clear, doable remedies — not vague generalities.</p>
            </div>
            <div class="why-card">
                <div class="icon icon-number"><svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="13" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M17 14v12M14 14h6M14 26h6M23 26l4-12h-4.5M23 26h5" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
                <h3>100% Confidential</h3>
                <p>Every session is private and judgement-free, conducted over WhatsApp voice or video call.</p>
            </div>
            <div class="why-card">
                <div class="icon icon-home"><svg viewBox="0 0 40 40" aria-hidden="true"><path d="M8 19 20 9l12 10" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M11 17v13h18V17" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M17 30v-7h6v7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg></div>
                <h3>Available Anywhere in the UK</h3>
                <p>Online consultations available to clients across the United Kingdom — all you need is WhatsApp.</p>
            </div>
        </div>
    </div>
</section>
'''


def process_section():
    return '''<section class="process-section">
    <div class="container">
        <h2 class="section-title">How a Session Works</h2>
        <p class="section-subtitle">Booking a reading from the UK is simple — here's what to expect</p>
        <div class="process-grid">
            <div class="step-card">
                <span class="step-num">01</span>
                <h3>Message on WhatsApp</h3>
                <p>Reach out with your name and what you'd like guidance on — love, career, marriage, finance or general life direction.</p>
            </div>
            <div class="step-card">
                <span class="step-num">02</span>
                <h3>Share Your Details</h3>
                <p>For astrology, share your date, time &amp; place of birth. For tarot, just come with an open question or situation in mind.</p>
            </div>
            <div class="step-card">
                <span class="step-num">03</span>
                <h3>Get Your Reading</h3>
                <p>Himu prepares your chart or draws your spread and walks you through it on a WhatsApp voice/video call, at a convenient GMT/BST time slot.</p>
            </div>
            <div class="step-card">
                <span class="step-num">04</span>
                <h3>Follow-Up Guidance</h3>
                <p>Leave with clear remedies and next steps — with follow-up support if you need clarity later.</p>
            </div>
        </div>
    </div>
</section>
'''


def locations_section():
    blocks = []
    for nation in NATIONS:
        cities = CITIES_BY_NATION[nation]
        cards = "\n".join(
            f'''            <a class="location-card" href="best-astrologer-in-{c["slug"]}.html">
                <div class="lc-title">{c["name"]}</div>
                <div class="lc-sub">{c["nation"]}</div>
            </a>'''
            for c in cities
        )
        if not cards:
            continue
        blocks.append(f'''        <div class="division-block">
            <h3>{nation}</h3>
            <div class="locations-grid">
{cards}
            </div>
        </div>''')
    blocks_html = "\n".join(blocks)
    return f'''<section id="cities" class="locations-section">
    <div class="container">
        <div class="locations-intro">
            <h2 class="section-title">Best Astrologer — Cities in the UK</h2>
            <p class="section-subtitle">Find your city below for online astrology &amp; tarot guidance, available anywhere in the United Kingdom</p>
        </div>
        <div class="location-search-wrap">
            <input type="text" id="locationSearch" class="location-search" placeholder="Search your city…" aria-label="Search your city">
        </div>
{blocks_html}
    </div>
</section>
'''


def pricing_section():
    return '''<section id="pricing" class="pricing-section">
    <div class="container">
        <h2 class="section-title">Consultation Packages</h2>
        <p class="section-subtitle">Starting prices in GBP — final fee confirmed on WhatsApp based on your exact requirement</p>
        <div class="pricing-grid">
            <div class="price-card">
                <h3>Quick Clarity</h3>
                <span class="price-sub">Tarot Reading</span>
                <div class="price-amount">£15<span>starting</span></div>
                <p>Focused on one question or situation — love, career or a decision you're facing.</p>
                <ul>
                    <li>30-minute WhatsApp/video session</li>
                    <li>3–5 card focused spread</li>
                    <li>Voice-note summary to keep</li>
                </ul>
                <a href="''' + whatsapp_url("Hello%20Himu%2C%20I%20want%20to%20book%20the%20Quick%20Clarity%20session") + '''" class="btn-secondary" target="_blank" rel="noopener">Book on WhatsApp →</a>
            </div>
            <div class="price-card popular">
                <span class="popular-badge">Most Booked</span>
                <h3>Full Birth Chart</h3>
                <span class="price-sub">Vedic Astrology</span>
                <div class="price-amount">£29<span>starting</span></div>
                <p>Complete Kundli analysis with Dasha timing and remedies — the most popular session.</p>
                <ul>
                    <li>60-minute detailed reading</li>
                    <li>Birth chart &amp; Dasha analysis</li>
                    <li>Personalised planetary remedies</li>
                    <li>Follow-up questions included</li>
                </ul>
                <a href="''' + whatsapp_url("Hello%20Himu%2C%20I%20want%20to%20book%20the%20Full%20Birth%20Chart%20session") + '''" class="btn-secondary" target="_blank" rel="noopener">Book on WhatsApp →</a>
            </div>
            <div class="price-card">
                <h3>Life Guidance</h3>
                <span class="price-sub">Astrology + Numerology + Vastu</span>
                <div class="price-amount">£59<span>starting</span></div>
                <p>A combined session for major life decisions — marriage, career shift, or new home.</p>
                <ul>
                    <li>90-minute combined session</li>
                    <li>Kundli, numbers &amp; Vastu review</li>
                    <li>Written action plan</li>
                    <li>Priority WhatsApp support</li>
                </ul>
                <a href="''' + whatsapp_url("Hello%20Himu%2C%20I%20want%20to%20book%20the%20Life%20Guidance%20session") + '''" class="btn-secondary" target="_blank" rel="noopener">Book on WhatsApp →</a>
            </div>
        </div>
    </div>
</section>
'''


def blog_teaser_section():
    cards = "\n".join(f'''            <a class="blog-teaser-card" href="blog-{p["slug"]}.html">
                <div class="icon icon-{p["icon"]}">{ICON_SVGS[p["icon"]]}</div>
                <span class="tag">{p["read_minutes"]} min read</span>
                <h3>{p["title"]}</h3>
                <p>{p["excerpt"]}</p>
            </a>''' for p in BLOG_POSTS[:3])
    return f'''<section class="blog-teaser-section">
    <div class="container">
        <h2 class="section-title">From the Blog</h2>
        <p class="section-subtitle">Free guides on astrology, tarot, numerology and Vastu</p>
        <div class="blog-teaser-grid">
{cards}
        </div>
        <div style="text-align:center;margin-top:28px;">
            <a href="blog.html" class="btn-outline">Read All Articles →</a>
        </div>
    </div>
</section>
'''


def cta_section():
    return f'''<section class="cta">
    <div class="container">
        <h2>Ready to get clarity, wherever you are in the UK?</h2>
        <p>Book an online tarot or astrology session today — evening and weekend slots available across the UK.</p>
        <div class="cta-buttons">
            <a href="{whatsapp_url()}" class="btn-wa" target="_blank" rel="noopener">WhatsApp Now</a>
            <a href="tel:{PHONE}" class="btn-call">Call for Appointment</a>
        </div>
        <p class="cta-note">Evening &amp; weekend slots available | Sessions scheduled at convenient GMT/BST times</p>
    </div>
</section>
'''


def page_shell(title, description, body, canonical, schema_scripts, active_href="index.html"):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <meta name="theme-color" content="#0e0a1c">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="author" content="Himu">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%94%AE%3C/text%3E%3C/svg%3E">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{SITE_BASE}/og-image.jpg">
    <meta property="og:url" content="{canonical}">
    <meta name="twitter:card" content="summary_large_image">
{schema_scripts}
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,500;1,9..144,600&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
<a href="#main" class="skip-link">Skip to main content</a>
{nav(active_href)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
'''


def local_business_schema(name, description, area_served_json, url):
    return (
        '{"@context": "https://schema.org", "@type": "ProfessionalService", '
        f'"name": "{name}", "description": "{description}", '
        f'"image": "{SITE_BASE}/og-image.jpg", '
        f'"address": {{"@type": "PostalAddress", "streetAddress": "{STUDIO_ADDRESS["streetAddress"]}", '
        f'"addressLocality": "{STUDIO_ADDRESS["addressLocality"]}", "addressRegion": "{STUDIO_ADDRESS["addressRegion"]}", '
        f'"postalCode": "{STUDIO_ADDRESS["postalCode"]}", "addressCountry": "{STUDIO_ADDRESS["addressCountry"]}"}}, '
        f'"areaServed": {area_served_json}, '
        f'"telephone": "{PHONE}", "email": "{EMAIL}", "url": "{url}", "priceRange": "£", '
        '"aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.9", "reviewCount": "186"}, '
        '"sameAs": ["https://www.facebook.com/tarotwithhimu", "https://www.instagram.com/tarotwithhimu"]}'
    )


def build_homepage():
    title = clip("Best Astrologer for the UK | Vedic Astrology, Tarot &amp; Vastu Online – Himu", 60)
    desc = clip("Himu is a certified Vedic astrologer &amp; tarot reader offering online consultations "
                "for clients across the UK via WhatsApp/video call. Astrology, Numerology &amp; Vastu.", 160)
    canonical = f"{SITE_BASE}/index.html"
    schema1 = local_business_schema(
        "Himu Astrology — Best Astrologer for Clients in the UK",
        "Certified Vedic Astrologer, Tarot Reader, Numerologist and Vastu Consultant, Himu, offering online consultations for clients across the United Kingdom.",
        '{"@type": "Country", "name": "United Kingdom"}',
        canonical,
    )
    schema2 = ('{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ['
               '{"@type": "Question", "name": "Does Himu offer astrology consultations in the UK?", '
               '"acceptedAnswer": {"@type": "Answer", "text": "Yes. Himu is a certified Vedic astrologer and tarot reader offering online consultations to clients across the United Kingdom over WhatsApp voice or video call, for love, career, marriage, finance and family matters."}}, '
               '{"@type": "Question", "name": "How do I book a session from the UK?", '
               '"acceptedAnswer": {"@type": "Answer", "text": "Message Himu on WhatsApp with your name, date of birth (and time/place of birth for a Vedic astrology reading), and the city you\'re writing from. Available slots and fees will be shared, and the session is conducted over WhatsApp voice or video call at a convenient GMT/BST time."}}, '
               '{"@type": "Question", "name": "Which US cities are served?", '
               '"acceptedAnswer": {"@type": "Answer", "text": "Clients from any city in the United Kingdom can book online \u2014 from London and Manchester to smaller towns \u2014 since every session is conducted remotely over WhatsApp or video call."}}, '
               '{"@type": "Question", "name": "What is the difference between tarot reading and Vedic astrology?", '
               '"acceptedAnswer": {"@type": "Answer", "text": "Vedic astrology uses your exact date, time and place of birth to map planetary positions and predict long-term life patterns, while tarot reading uses card spreads for intuitive guidance on a specific question or situation. Many clients combine both."}}, '
               '{"@type": "Question", "name": "How much does a session cost, and in what currency?", '
               '"acceptedAnswer": {"@type": "Answer", "text": "Starting prices are listed in Pounds Sterling (GBP). Fees vary by session type and duration \u2014 message Himu on WhatsApp with what you need and the exact price will be confirmed before you book."}}]}')
    schema_scripts = (f'    <script type="application/ld+json">{schema1}</script>\n'
                       f'    <script type="application/ld+json">{schema2}</script>')

    body = f'''<header class="hero">
    <div class="container hero-container">
        <div class="hero-content">
            <div class="hero-badge">Online Consultations for Clients Across the UK</div>
            <h1>Best Astrologer for the <span class="highlight">UK</span><br>Vedic Astrology, Tarot &amp; Vastu — Online</h1>
            <p>Himu — certified Vedic astrologer &amp; tarot reader, offering online consultations for clients across the United Kingdom. Accurate predictions for love, career, marriage, finance and life purpose, delivered over WhatsApp at a GMT/BST-friendly slot.</p>
            <div class="hero-buttons">
                <a href="{whatsapp_url()}" class="btn-primary" target="_blank" rel="noopener">Book a Reading</a>
                <a href="#cities" class="btn-outline">Find Your City</a>
            </div>
            <div class="keywords">
                <span>Best Astrologer in the UK</span>
                <span>Online Astrologer UK</span>
                <span>Tarot Reader UK</span>
                <span>Vastu Consultant UK</span>
            </div>
        </div>
        <div class="hero-image">
            <div class="hero-visual" aria-hidden="true">
                <svg viewBox="0 0 320 320">
                    <circle class="hv-ring" cx="160" cy="160" r="128"/>
                    <path class="hv-moon" d="M196 76c-46 8-78 46-78 92 0 50 38 90 87 94-18 12-40 18-63 18-58 0-105-52-105-116S144 48 202 48c22 0 43 6 61 15-24 3-46 7-67 13z"/>
                    <g class="hv-stars">
                        <circle cx="238" cy="70" r="3.4"/>
                        <circle cx="256" cy="98" r="2.1"/>
                        <circle cx="90" cy="238" r="2.6"/>
                        <circle cx="66" cy="90" r="2"/>
                    </g>
                    <g class="hv-card">
                        <rect x="120" y="118" width="92" height="132" rx="10"/>
                        <path d="M166 150v68M140 184h52" />
                        <circle cx="166" cy="150" r="5"/>
                    </g>
                </svg>
            </div>
            <p class="hero-tagline">"Accurate. Empathetic. Life-changing insights."</p>
        </div>
    </div>
</header>

<div class="badges-strip">
    <div class="container">
        <span class="rating-chip">★★★★★ 4.9/5 — 186+ Readings</span>
        <span>Vedic &amp; Tarot Certified</span>
        <span>Online Sessions via WhatsApp</span>
        <span>Available Across the UK</span>
        <span>Time-Zone-Friendly Slots</span>
    </div>
</div>

<section class="stats-bar">
    <div class="container stats-grid">
            <div class="stat-item">
                <span class="stat-num">8+</span>
                <span class="stat-label">Years of Practice</span>
            </div>
            <div class="stat-item">
                <span class="stat-num">3,500+</span>
                <span class="stat-label">Readings Delivered</span>
            </div>
            <div class="stat-item">
                <span class="stat-num">100%</span>
                <span class="stat-label">Online &amp; Confidential</span>
            </div>
            <div class="stat-item">
                <span class="stat-num">4.9★</span>
                <span class="stat-label">Average Client Rating</span>
            </div>
    </div>
</section>

{services_section()}
{why_section()}
{process_section()}
{locations_section()}
{blog_teaser_section()}
{pricing_section()}

<section class="faq-section">
    <div class="container">
        <h2 class="section-title">Frequently Asked Questions</h2>
        <div class="faq-list">
            <details class="faq-item">
                <summary>Does Himu offer astrology consultations in the UK?</summary>
                <p>Yes. Himu is a certified Vedic astrologer and tarot reader offering online consultations to clients across the United Kingdom over WhatsApp voice or video call, for love, career, marriage, finance and family matters.</p>
            </details>
            <details class="faq-item">
                <summary>How do I book a session from the UK?</summary>
                <p>Message Himu on WhatsApp with your name, date of birth (and time/place of birth for a Vedic astrology reading), and the city you're writing from. Available slots and fees will be shared, and the session is conducted over WhatsApp voice or video call at a convenient GMT/BST time.</p>
            </details>
            <details class="faq-item">
                <summary>Which US cities are served?</summary>
                <p>Clients from any city in the United Kingdom can book online — from London and Manchester to smaller towns — since every session is conducted remotely over WhatsApp or video call.</p>
            </details>
            <details class="faq-item">
                <summary>What is the difference between tarot reading and Vedic astrology?</summary>
                <p>Vedic astrology uses your exact date, time and place of birth to map planetary positions and predict long-term life patterns, while tarot reading uses card spreads for intuitive guidance on a specific question or situation. Many clients combine both.</p>
            </details>
            <details class="faq-item">
                <summary>How much does a session cost, and in what currency?</summary>
                <p>Starting prices are listed in Pounds Sterling (GBP). Fees vary by session type and duration — message Himu on WhatsApp with what you need and the exact price will be confirmed before you book.</p>
            </details>
        </div>
    </div>
</section>

{cta_section()}'''
    return page_shell(title, desc, body, canonical, schema_scripts, "index.html")


def build_city_page(c):
    name = c["name"]
    slug = c["slug"]
    nation = c["nation"]
    title = clip(f"Best Astrologer for Clients in {name}, {nation} | Vedic Astrology &amp; Tarot – Himu", 60)
    desc = clip(f"Online Vedic astrology &amp; tarot consultations for clients in {name}, {nation} — "
                f"book Himu on WhatsApp for astrology, numerology &amp; Vastu guidance.", 160)
    canonical = f"{SITE_BASE}/best-astrologer-in-{slug}.html"
    schema1 = local_business_schema(
        f"Himu — Astrology &amp; Tarot Consultations for Clients in {name}",
        f"Vedic astrology, tarot reading, numerology and Vastu consultation, delivered online to clients in {name}, {nation}, United Kingdom.",
        f'{{"@type": "City", "name": "{name}"}}',
        canonical,
    )
    schema2 = ('{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": ['
               f'{{"@type": "Question", "name": "Can clients in {name} book an astrology or tarot session with Himu?", '
               f'"acceptedAnswer": {{"@type": "Answer", "text": "Yes. Clients in {name} can book a Vedic astrology or tarot reading with Himu entirely online, over WhatsApp voice or video call \u2014 no travel required."}}}}, '
               f'{{"@type": "Question", "name": "What astrology services are available for clients in {name}?", '
               '"acceptedAnswer": {"@type": "Answer", "text": "Vedic astrology (Kundli/birth chart reading), tarot card reading, numerology, Vastu consultation, marriage matching (Kundli Milan) and remedies for career, finance, love and health concerns \u2014 all available online."}}, '
               f'{{"@type": "Question", "name": "How much does a session cost for clients in {name}?", '
               '"acceptedAnswer": {"@type": "Answer", "text": "Starting prices are listed in Pounds Sterling (GBP) on the pricing section of the site. Message Himu on WhatsApp with your requirement and the exact fee and available slots will be shared."}}]}')
    crumb_items = [("index.html", "Home"), ("index.html#cities", "Cities"), (None, name)]
    schema3 = ld_breadcrumb(crumb_items)
    schema_scripts = (f'    <script type="application/ld+json">{schema1}</script>\n'
                       f'    <script type="application/ld+json">{schema2}</script>\n'
                       f'    <script type="application/ld+json">{schema3}</script>')

    nearby = nearby_cities(slug)
    nearby_links_html = "\n".join(
        f'            <a href="best-astrologer-in-{n["slug"]}.html">{n["name"]}, {n["nation"]}</a>' for n in nearby
    )

    body = f'''{breadcrumb(crumb_items)}
<header class="hero city-hero">
    <div class="container hero-container">
        <div class="hero-content">
            <div class="hero-badge">Online for Clients in {name}, {nation}</div>
            <h1>Best Astrologer for <span class="highlight">{name}</span><br>Vedic Astrology, Tarot &amp; Vastu — Online</h1>
            <p>Himu — certified Vedic astrologer &amp; tarot reader, offering online consultations for clients in {name}, {c["hook"]}. Accurate predictions for love, career, marriage, finance and life purpose, delivered over WhatsApp.</p>
            <div class="hero-buttons">
                <a href="{whatsapp_url()}" class="btn-primary" target="_blank" rel="noopener">Book a Reading</a>
                <a href="index.html#cities" class="btn-outline">See All Cities</a>
            </div>
        </div>
        <div class="hero-image">
            <div class="hero-visual" aria-hidden="true">
                <svg viewBox="0 0 320 320">
                    <circle class="hv-ring" cx="160" cy="160" r="128"/>
                    <path class="hv-moon" d="M196 76c-46 8-78 46-78 92 0 50 38 90 87 94-18 12-40 18-63 18-58 0-105-52-105-116S144 48 202 48c22 0 43 6 61 15-24 3-46 7-67 13z"/>
                    <g class="hv-stars">
                        <circle cx="238" cy="70" r="3.4"/>
                        <circle cx="256" cy="98" r="2.1"/>
                        <circle cx="90" cy="238" r="2.6"/>
                        <circle cx="66" cy="90" r="2"/>
                    </g>
                    <g class="hv-card">
                        <rect x="120" y="118" width="92" height="132" rx="10"/>
                        <path d="M166 150v68M140 184h52" />
                        <circle cx="166" cy="150" r="5"/>
                    </g>
                </svg>
            </div>
            <p class="hero-tagline">"Accurate. Empathetic. Life-changing insights."</p>
        </div>
    </div>
</header>

<section class="services" style="padding-top:2.5rem;">
    <div class="container">
        <p class="section-subtitle" style="max-width:760px;margin:0 auto 0;text-align:left;">{c["blurb"]}</p>
    </div>
</section>

{services_section()}
{why_section()}
{process_section()}
{pricing_section()}

<section class="faq-section">
    <div class="container">
        <h2 class="section-title">FAQ — Astrology &amp; Tarot for Clients in {name}</h2>
        <div class="faq-list">
            <details class="faq-item">
                <summary>Can clients in {name} book an astrology or tarot session with Himu?</summary>
                <p>Yes. Clients in {name} can book a Vedic astrology or tarot reading with Himu entirely online, over WhatsApp voice or video call — no travel required.</p>
            </details>
            <details class="faq-item">
                <summary>What astrology services are available for clients in {name}?</summary>
                <p>Vedic astrology (Kundli/birth chart reading), tarot card reading, numerology, Vastu consultation, marriage matching (Kundli Milan) and remedies for career, finance, love and health concerns — all available online.</p>
            </details>
            <details class="faq-item">
                <summary>How much does a session cost for clients in {name}?</summary>
                <p>Starting prices are listed in Pounds Sterling (GBP) above. Message Himu on WhatsApp with your requirement and the exact fee and available slots will be shared.</p>
            </details>
        </div>
    </div>
</section>

<section class="nearby-section">
    <div class="container">
        <h2>Nearby Cities</h2>
        <div class="nearby-links">
{nearby_links_html}
        </div>
    </div>
</section>

{cta_section()}'''
    return page_shell(title, desc, body, canonical, schema_scripts, f"best-astrologer-in-{slug}.html")


ICON_SVGS = {
    "tarot": '<svg viewBox="0 0 40 40" aria-hidden="true"><rect x="10" y="6" width="14" height="22" rx="2" transform="rotate(-8 17 17)" fill="none" stroke="currentColor" stroke-width="1.6"/><rect x="16" y="10" width="14" height="22" rx="2" transform="rotate(8 23 21)" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="23" cy="21" r="2.4" fill="currentColor"/></svg>',
    "moon": '<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M25 8c-7 1-12 7-12 14s5 13 12 14c-2.6 1.3-5.6 2-8.7 2C7 38 1 30.8 1 22S7 6 16.3 6c3.1 0 6.1.7 8.7 2z" transform="translate(6,-2)" fill="currentColor"/><circle cx="30" cy="10" r="1.3" fill="currentColor"/><circle cx="33" cy="15" r="0.9" fill="currentColor"/></svg>',
    "number": '<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="13" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M17 14v12M14 14h6M14 26h6M23 26l4-12h-4.5M23 26h5" stroke="currentColor" stroke-width="1.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "home": '<svg viewBox="0 0 40 40" aria-hidden="true"><path d="M8 19 20 9l12 10" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M11 17v13h18V17" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M17 30v-7h6v7" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>',
}


def _emph(text):
    """Turn *word* into <em>word</em> for the light markdown used in blog copy."""
    import re as _re
    return _re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)


def render_post_body(items):
    parts = []
    for item in items:
        if isinstance(item, tuple):
            heading, para = item
            heading = heading.lstrip("# ").strip()
            parts.append(f"<h2>{_emph(heading)}</h2>\n<p>{_emph(para)}</p>")
        else:
            parts.append(f"<p>{_emph(item)}</p>")
    return "\n".join(parts)


def related_posts(current_slug, n=2):
    others = [p for p in BLOG_POSTS if p["slug"] != current_slug]
    offset = sum(ord(ch) for ch in current_slug) % len(others)
    return (others[offset:] + others[:offset])[:n]


def build_blog_index():
    title = clip("Astrology &amp; Tarot Blog | Vedic Astrology Guides for the UK – Himu", 60)
    desc = clip("Free guides on Vedic astrology, tarot, numerology and Vastu from Himu — "
                "practical reading for clients across the UK.", 160)
    canonical = f"{SITE_BASE}/blog.html"
    crumb_items = [("index.html", "Home"), (None, "Blog")]
    schema = ld_breadcrumb(crumb_items)
    schema_scripts = f'    <script type="application/ld+json">{schema}</script>'

    cards = "\n".join(f'''            <article class="blog-card">
                <div class="icon icon-{p["icon"]}">{ICON_SVGS[p["icon"]]}</div>
                <span class="tag">{p["tag"]} · {p["read_minutes"]} min read</span>
                <h2><a href="blog-{p["slug"]}.html">{p["title"]}</a></h2>
                <p>{p["excerpt"]}</p>
                <a href="blog-{p["slug"]}.html" class="read-more">Read More →</a>
            </article>''' for p in BLOG_POSTS)

    body = f'''{breadcrumb(crumb_items)}
<header class="hero loc-hero">
    <div class="container">
        <div class="hero-badge">Insights &amp; Guidance</div>
        <h1>Astrology &amp; Tarot <span class="highlight">Blog</span></h1>
        <p>Practical, plain-English guides to Vedic astrology, tarot, numerology and Vastu — for readers across the UK.</p>
    </div>
</header>

<section>
    <div class="container">
        <div class="blog-grid">
{cards}
        </div>
    </div>
</section>

{cta_section()}'''
    return page_shell(title, desc, body, canonical, schema_scripts, "blog.html")


def build_blog_post(post):
    slug = post["slug"]
    title = clip(f"{post['title']} | Himu Astrology Blog", 60)
    desc = clip(post["excerpt"], 160)
    canonical = f"{SITE_BASE}/blog-{slug}.html"
    crumb_items = [("index.html", "Home"), ("blog.html", "Blog"), (None, post["title"])]
    schema1 = ld_breadcrumb(crumb_items)
    schema2 = json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": post["title"], "description": post["excerpt"],
        "author": {"@type": "Person", "name": "Himu"},
        "publisher": {"@type": "Organization", "name": "Himu Astrology"},
        "mainEntityOfPage": canonical,
    })
    schema_scripts = (f'    <script type="application/ld+json">{schema1}</script>\n'
                       f'    <script type="application/ld+json">{schema2}</script>')

    related = related_posts(slug)
    related_html = "\n".join(
        f'            <a href="blog-{r["slug"]}.html">{r["title"]}</a>' for r in related
    )

    body = f'''{breadcrumb(crumb_items)}
<article style="padding: 56px 0 90px;">
    <div class="container post-body">
        <h1>{post["title"]}</h1>
        <p class="post-meta">By Himu · {post["tag"]} · {post["read_minutes"]} min read</p>

{render_post_body(post["body"])}

        <div class="cta" style="margin: 40px 0; padding: 40px 28px;">
            <h2 style="font-size:1.5rem;">Ready to explore this for yourself?</h2>
            <p>Book a session with Himu — online, over WhatsApp, for clients anywhere in the UK.</p>
            <div class="cta-buttons">
                <a href="{whatsapp_url()}" class="btn-wa" target="_blank" rel="noopener">Book Your Reading Now →</a>
            </div>
        </div>

        <div class="local-fact-card" style="margin-top:40px;">
            <h3>About Himu</h3>
            <p style="font-size:0.94rem;">Himu is a certified astrologer offering tarot, Vedic astrology, numerology and Vastu consultation online, for clients across the UK.</p>
        </div>
    </div>
</article>

<section class="nearby-section">
    <div class="container">
        <h2>More From the Blog</h2>
        <div class="nearby-links">
{related_html}
        </div>
    </div>
</section>

{cta_section()}'''
    return page_shell(title, desc, body, canonical, schema_scripts, "blog.html")


def build_sitemap():
    entries = [(f"{SITE_BASE}/index.html", "1.0")]
    entries += [(f"{SITE_BASE}/best-astrologer-in-{c['slug']}.html", "0.8") for c in CITIES]
    entries += [(f"{SITE_BASE}/blog.html", "0.6")]
    entries += [(f"{SITE_BASE}/blog-{p['slug']}.html", "0.6") for p in BLOG_POSTS]
    items = "\n".join(
        f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{BUILD_DATE}</lastmod>\n"
        f"    <changefreq>monthly</changefreq>\n    <priority>{p}</priority>\n  </url>"
        for u, p in entries
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}\n</urlset>\n'


def build_robots():
    return f"User-agent: *\nAllow: /\n\nSitemap: {SITE_BASE}/sitemap.xml\n"


def main():
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_homepage())
    for c in CITIES:
        with open(os.path.join(OUT, f"best-astrologer-in-{c['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(build_city_page(c))
    with open(os.path.join(OUT, "blog.html"), "w", encoding="utf-8") as f:
        f.write(build_blog_index())
    for p in BLOG_POSTS:
        with open(os.path.join(OUT, f"blog-{p['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(build_blog_post(p))
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(build_sitemap())
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(build_robots())
    print(f"Built index.html + {len(CITIES)} city pages + blog.html + {len(BLOG_POSTS)} posts + sitemap.xml + robots.txt in {OUT}")


if __name__ == "__main__":
    main()
