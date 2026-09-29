# alumarketing.co.il: from zero to a verified domain

The site is `index.html` (the agency page, rebuilt 29 Sep 2026), `privacy.html` and
`app.html`, plus `robots.txt` and `sitemap.xml`; `CNAME` tells GitHub Pages the domain.
Everything below is in the order it has to happen. Sagi's steps carry his name.

## Contact details on the page

The WhatsApp number and the e-mail sit in one place, the `CONTACT` object at the top of the
script at the bottom of `index.html`. WhatsApp is international format, digits only
(`972` + the number without the leading 0). While it is empty every button falls back to
e-mail and the WhatsApp bubble stays hidden. The form saves nothing: it opens a prepared
WhatsApp message (or an e-mail) with the name, site, budget and phone the lead typed.

The marketing page says nothing about the automation (Sagi, 29 Sep: clients do not need to
know). Google's brand verification reads `app.html` instead: the description of Alumarketing
Agency Automation, its heading equal to the app name in the Cloud project, linking
`privacy.html`. That URL, `https://alumarketing.co.il/app.html`, goes in the Branding form's
"Application home page" field (step 5). The page is not linked from `index.html`, only from
the privacy policy.

## 1. Register the domain (Sagi, 10 minutes)

`.co.il` is sold by Israeli registrars. Any of these works; pick the cheapest year:

- Box: https://www.box.co.il
- Domain The Net: https://www.domainthenet.co.il
- GoDaddy (sells .co.il too): https://www.godaddy.com

Register `alumarketing.co.il` for one year. Keep the registrar login; the DNS records
in step 3 are entered there. Nothing else is needed from the registrar (no hosting, no
e-mail, no "site builder").

## 2. Publish the site (Sagi creates the repository, Claude pushes)

GitHub Pages under Sagi's GitHub account. The GitHub CLI is not installed on this machine,
so the empty repository is created in the browser (1 minute):

1. Sagi: https://github.com/new > name `alumarketing-site`, **Public**, no README, Create.
2. Claude pushes (Git Credential Manager is already signed in from the agency repo). First the
   four privacy edits in `Alumarketing-Claude/Alumarketing/deploy/api-basic-access/form_answers.md`
   step 8, so the page matches what the code does:

```bash
cd "C:/Users/SagiA/Claude.new/alumarketing-site"
git remote add origin https://github.com/sagialuma28/alumarketing-site.git
git push -u origin main
```

3. Sagi: repository > Settings > Pages > Source "Deploy from a branch", branch `main`,
   folder `/ (root)`, Save. Custom domain `alumarketing.co.il`, Save. Tick "Enforce HTTPS"
   once the certificate is issued (up to an hour after the DNS in step 3 resolves).

## 3. DNS at the registrar (Sagi, 5 minutes, values are exact)

| Type | Host / name | Value | TTL |
|---|---|---|---|
| A | @ | 185.199.108.153 | 3600 |
| A | @ | 185.199.109.153 | 3600 |
| A | @ | 185.199.110.153 | 3600 |
| A | @ | 185.199.111.153 | 3600 |
| CNAME | www | sagialuma28.github.io | 3600 |

Propagation takes minutes to a few hours. Check: https://alumarketing.co.il shows the page.

## 4. Verify the domain in Search Console (Sagi, 5 minutes)

https://search.google.com/search-console > Add property > **Domain** > `alumarketing.co.il`.
Google shows a TXT record (`google-site-verification=...`). Add it at the registrar:

| Type | Host / name | Value |
|---|---|---|
| TXT | @ | google-site-verification=... (the value Search Console shows) |

Press Verify. This is the ownership proof Google's brand verification reads.

## 5. Branding tab in the Cloud project (Sagi, 10 minutes)

https://console.cloud.google.com/auth/branding?project=alumarketing-agency-automation

| Field | Value |
|---|---|
| App name | Alumarketing Agency Automation |
| User support email | alumasagi82@gmail.com |
| App logo | optional; skip |
| Application home page | https://alumarketing.co.il/app.html |
| Application privacy policy link | https://alumarketing.co.il/privacy.html |
| Application terms of service link | leave empty |
| Authorized domains | alumarketing.co.il |
| Developer contact | alumasagi82@gmail.com |

Audience: user type **External**, publishing status **In production** (the docs require both
for the Basic access review). Save. Then **Verify branding**, and **Publish branding** once it
passes (a pass expires after 7 days unpublished).

## 6. Apply for Basic access (Sagi, 2 minutes)

https://console.cloud.google.com/google/ads-apis/overview?project=alumarketing-agency-automation
> Upgrade access level > Apply for access. The review is automated and takes minutes (Google's
access-levels page, 25 Sep 2026). Billing check, fallback answers and what to do on a refusal:
`Alumarketing-Claude/Alumarketing/deploy/api-basic-access/form_answers.md`.
`bin/am_credcheck.py` in the agency repo probes the level every morning and the growth pack
switches its Keyword Planner section on by itself.

## Editing the site later

Change `index.html` or `privacy.html`, commit, push. GitHub Pages redeploys within a minute.
The privacy policy must stay on this domain and stay linked from the home page; Google
re-checks it.
