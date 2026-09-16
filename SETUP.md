# alumarketing.co.il: from zero to a verified domain

Two files make the site (`index.html`, `privacy.html`); `CNAME` tells GitHub Pages the
domain. Everything below is in the order it has to happen. Sagi's steps carry his name.

## 1. Register the domain (Sagi, 10 minutes)

`.co.il` is sold by Israeli registrars. Any of these works; pick the cheapest year:

- Box: https://www.box.co.il
- Domain The Net: https://www.domainthenet.co.il
- GoDaddy (sells .co.il too): https://www.godaddy.com

Register `alumarketing.co.il` for one year. Keep the registrar login; the DNS records
in step 3 are entered there. Nothing else is needed from the registrar (no hosting, no
e-mail, no "site builder").

## 2. Publish the site (Claude, after Sagi's yes)

GitHub Pages under Sagi's GitHub account, a public repository `alumarketing-site`:

```bash
cd "C:/Users/SagiA/Claude.new/alumarketing-site"
gh repo create sagialuma28/alumarketing-site --public --source . --push
gh api -X POST repos/sagialuma28/alumarketing-site/pages -f build_type=legacy -f "source[branch]=main" -f "source[path]=/"
```

Then in the repository: Settings > Pages > Custom domain `alumarketing.co.il`, tick
"Enforce HTTPS" once the certificate is issued (up to an hour after DNS resolves).

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
| Application home page | https://alumarketing.co.il/ |
| Application privacy policy link | https://alumarketing.co.il/privacy.html |
| Application terms of service link | leave empty |
| Authorized domains | alumarketing.co.il |
| Developer contact | alumasagi82@gmail.com |

Audience: user type **External**, publishing status **In production** (the docs require both
for the Basic access review). Save.

## 6. Apply for Basic access (Sagi, 2 minutes)

https://console.cloud.google.com/google/ads-apis/overview?project=alumarketing-agency-automation
> Upgrade access level > Apply for access. Review up to 10 business days.
`bin/am_credcheck.py` in the agency repo probes the level every morning and the growth pack
switches its Keyword Planner section on by itself.

## Editing the site later

Change `index.html` or `privacy.html`, commit, push. GitHub Pages redeploys within a minute.
The privacy policy must stay on this domain and stay linked from the home page; Google
re-checks it.
