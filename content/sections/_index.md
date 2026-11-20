---
headless: true
# These pages are homepage fragments pulled in with .Site.GetPage.
# Never render them as standalone URLs (thin duplicate pages) and keep them out of the sitemap.
cascade:
  build:
    render: never
    list: local
    publishResources: false
---
