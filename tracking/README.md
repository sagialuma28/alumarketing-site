# Measurement on alumarketing.co.il

One Google Tag Manager container on every page. Everything else (GA4 today, Google Ads and
Meta when campaigns start) lives inside the container, so the site code never changes again.

## What the site sends

The pages load the container whose id is in `window.GTM_ID` at the top of `index.html`,
`privacy.html` and `app.html`, and `index.html` pushes three events to the dataLayer:

| Event | When | Parameters |
|---|---|---|
| `generate_lead` | the contact form was delivered (Web3Forms or FormSubmit answered success) | `form`, `interest`, `budget` |
| `whatsapp_click` | any WhatsApp link or the floating bubble | `location` |
| `email_click` | the e-mail link | `location` |

## The container

`gtm_import_alumarketing.json` is a full container to import (Tag Manager, Admin, Import
Container, choose the file, the default workspace, Merge). It holds:

- Google tag for GA4 on all pages, reading the constant `Const - GA4 Measurement ID`.
- GA4 event tags for the three events above.
- Conversion Linker on all pages (needed for Google Ads later, harmless now).
- Google Ads lead conversion, **paused**, reading `Const - Google Ads Conversion ID (numbers
  only)` and `Const - Google Ads Lead Label`. When an Ads account exists: create a
  "Lead" conversion action (website, manual), paste its id and label into the two constants,
  unpause, publish.
- Meta Pixel base and Lead tags, **paused**, reading `Const - Meta Pixel ID`. When a pixel
  exists: paste the id, unpause both, publish.

Regenerate the file with a real GA4 id, from this folder:
`python make_gtm_container.py G-XXXXXXXXXX gtm_import_alumarketing.json`
(the constant can also be edited in the container after the import).

## Going live, in order

1. analytics.google.com: create the account (Alumarketing) and a GA4 property
   (alumarketing.co.il), web data stream, copy the Measurement ID (G-...).
2. tagmanager.google.com: create the account and a Web container (alumarketing.co.il), copy
   the container id (GTM-...).
3. Put the GTM id in `window.GTM_ID` in the three pages, commit, push.
4. Import `gtm_import_alumarketing.json`, set `Const - GA4 Measurement ID`, Submit, Publish.
5. Check in GA4 Realtime: open the site, click WhatsApp, send a test lead.
