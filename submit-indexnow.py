"""Submit all pages to IndexNow (Bing, Yandex, Seznam, Naver)."""
import json, urllib.request, sys

KEY = "2f7f2f3c236a48fdba58cd8018b0a3cf"
HOST = "tadoliphantconstruction.com"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"

CORE = [
    "/", "/about.html", "/contact.html", "/reviews.html",
    "/gallery.html", "/faq.html", "/service-areas.html",
]

SERVICES = [
    "/services/deck-construction.html", "/services/deck-repair.html",
    "/services/siding-repair.html", "/services/dry-rot-repair.html",
    "/services/roofing.html", "/services/windows-doors.html",
    "/services/home-remodeling.html", "/services/kitchen-remodeling.html",
    "/services/bathroom-remodeling.html", "/services/framing-structural-repair.html",
    "/services/painting.html", "/services/fencing.html",
]

CITIES = [
    "/siletz.html", "/newport.html", "/lincoln-city.html",
    "/toledo.html", "/depoe-bay.html", "/waldport.html", "/south-beach.html",
]

BLOG_INDEX = ["/blog/"]

urls = [f"https://{HOST}{p}" for p in CORE + SERVICES + CITIES + BLOG_INDEX]

# Also add blog posts from sitemap
try:
    import xml.etree.ElementTree as ET
    tree = ET.parse("sitemap.xml")
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    for url_el in tree.findall(".//sm:url/sm:loc", ns):
        u = url_el.text.strip()
        if u not in urls:
            urls.append(u)
except Exception as e:
    print(f"Warning: could not parse sitemap.xml: {e}")

print(f"Submitting {len(urls)} URLs via IndexNow...")

ENGINES = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
    "https://yandex.com/indexnow",
]

payload = json.dumps({
    "host": HOST,
    "key": KEY,
    "keyLocation": KEY_LOCATION,
    "urlList": urls,
}).encode("utf-8")

for engine in ENGINES:
    try:
        req = urllib.request.Request(
            engine,
            data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=30)
        print(f"  {engine} -> {resp.status} {resp.reason}")
    except Exception as e:
        print(f"  {engine} -> ERROR: {e}")

# Ping sitemaps
SITEMAP = f"https://{HOST}/sitemap.xml"
PINGS = [
    f"https://www.google.com/ping?sitemap={SITEMAP}",
    f"https://www.bing.com/ping?sitemap={SITEMAP}",
]

print(f"\nPinging sitemaps...")
for ping_url in PINGS:
    try:
        req = urllib.request.Request(ping_url, method="GET")
        resp = urllib.request.urlopen(req, timeout=15)
        print(f"  {ping_url.split('?')[0]} -> {resp.status}")
    except Exception as e:
        print(f"  {ping_url.split('?')[0]} -> ERROR: {e}")

print(f"\nDone! {len(urls)} URLs submitted.")
