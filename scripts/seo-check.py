"""Post-build SEO lint for the Hugo output folder.

Usage: python3 scripts/seo-check.py public
Fails (exit 1) on errors: broken internal links, invalid JSON-LD, TODO placeholders
in schema, malformed breadcrumbs, duplicate schema blocks, thin /sections/ pages in
the sitemap, missing staticwebapp.config.json. Length/format issues are warnings.
"""
import sys, os, re, json, html
from html.parser import HTMLParser
root = sys.argv[1]
BASE = "https://www.curedcompliance.com"
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links=[]; s.ld=[]; s._ld=False; s.title=""; s._t=False; s.meta={}; s.h1=0; s.imgs_nodim=0; s.lang=None
    def handle_starttag(s,t,a):
        a=dict(a)
        if t=="html": s.lang=a.get("lang")
        if t=="a" and a.get("href"): s.links.append(a["href"])
        if t=="script" and a.get("type")=="application/ld+json": s._ld=True; s.ld.append("")
        if t=="title": s._t=True
        if t=="meta" and a.get("name"): s.meta[a["name"]]=a.get("content","")
        if t=="h1": s.h1+=1
        if t=="img" and not (a.get("width") and a.get("height")): s.imgs_nodim+=1
    def handle_endtag(s,t):
        if t=="script": s._ld=False
        if t=="title": s._t=False
    def handle_data(s,d):
        if s._ld: s.ld[-1]+=d
        if s._t: s.title+=d
pages={}
for dp,_,fs in os.walk(root):
    for f in fs:
        if f.endswith(".html"):
            rel="/"+os.path.relpath(os.path.join(dp,f),root).replace("index.html","")
            p=P(); p.feed(open(os.path.join(dp,f),encoding="utf8").read()); pages[rel]=p
def exists(path):
    path=path.split("#")[0].split("?")[0]
    if path in ("","/"): return True
    fp=os.path.join(root,path.lstrip("/"))
    return os.path.isfile(fp) or os.path.isfile(os.path.join(fp,"index.html"))
problems=[]
for url,p in sorted(pages.items()):
    if url.startswith("/404"): continue
    for h in p.links:
        h=html.unescape(h)
        if h.startswith(BASE): h=h[len(BASE):] or "/"
        if h.startswith("/") and not h.startswith("//"):
            if not exists(h): problems.append(f"BROKEN {url} -> {h}")
            elif not h.split("#")[0].endswith("/") and "." not in h.split("/")[-1] and h.split("#")[0]: problems.append(f"NOSLASH {url} -> {h}")
    types=[]
    for raw in p.ld:
        try: j=json.loads(raw)
        except Exception as e: problems.append(f"BADJSON {url}: {e}"); continue
        types.append(j.get("@type"))
        txt=json.dumps(j)
        if "TODO" in txt: problems.append(f"TODO-IN-SCHEMA {url} {j.get('@type')}")
        if j.get("@type")=="BreadcrumbList":
            for it in j["itemListElement"]:
                if not str(it.get("item","")).startswith("https://") or '"' in it.get("name",""): problems.append(f"BAD-BREADCRUMB {url} {it}")
    dup=[t for t in set(types) if types.count(t)>1 and t!="Person"]
    if dup: problems.append(f"DUP-SCHEMA {url} {dup}")
    if "LocalBusiness" in types: problems.append(f"LOCALBUSINESS {url}")
    tl=len(html.unescape(p.title)); dl=len(html.unescape(p.meta.get("description","")))
    if tl>65: problems.append(f"LONG-TITLE({tl}) {url}")
    if dl>165: problems.append(f"LONG-DESC({dl}) {url}")
    if p.h1!=1: problems.append(f"H1={p.h1} {url}")
    if p.lang!="en-AU": problems.append(f"LANG={p.lang} {url}")
    if p.meta.get("generator"): problems.append(f"GENERATOR {url}")
sm=open(os.path.join(root,"sitemap.xml")).read()
for loc in re.findall(r"<loc>([^<]+)</loc>",sm):
    if "/sections/" in loc: problems.append(f"SITEMAP-SECTIONS {loc}")
if not os.path.isfile(os.path.join(root,"staticwebapp.config.json")):
    problems.append("NO-SWA-CONFIG staticwebapp.config.json missing from build output")
ERRORS=("BROKEN","BADJSON","TODO-IN-SCHEMA","BAD-BREADCRUMB","DUP-SCHEMA","SITEMAP-SECTIONS","NO-SWA-CONFIG","LOCALBUSINESS")
errs=[p for p in problems if p.startswith(ERRORS)]
warns=[p for p in problems if p not in errs]
print(f"SEO check: {len(pages)} pages, {len(errs)} errors, {len(warns)} warnings")
for p in errs: print("ERROR  "+p)
for p in warns: print("WARN   "+p)
sys.exit(1 if errs else 0)
