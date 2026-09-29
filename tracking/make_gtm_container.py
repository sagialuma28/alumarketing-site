"""Builds the Tag Manager import file for alumarketing.co.il.

Usage: python make_gtm_container.py [GA4_MEASUREMENT_ID] [OUT_PATH]
The GA4 id is optional; a placeholder constant is written when it is missing and can be edited
in the container after the import. Google Ads and Meta tags are included paused, with placeholder
constants, so switching them on later is: fill the constant, unpause, publish.
"""
import json
import sys
from datetime import datetime, timezone

ga4 = sys.argv[1] if len(sys.argv) > 1 else "G-XXXXXXXXXX"
out = sys.argv[2] if len(sys.argv) > 2 else "gtm_import_alumarketing.json"

ALL_PAGES = "2147479553"


def const(vid, name, value):
    return {"accountId": "0", "containerId": "0", "variableId": str(vid), "name": name, "type": "c",
            "parameter": [{"type": "TEMPLATE", "key": "value", "value": value}]}


def dlv(vid, name, key):
    return {"accountId": "0", "containerId": "0", "variableId": str(vid), "name": name, "type": "v",
            "parameter": [{"type": "INTEGER", "key": "dataLayerVersion", "value": "2"},
                          {"type": "BOOLEAN", "key": "setDefaultValue", "value": "false"},
                          {"type": "TEMPLATE", "key": "name", "value": key}]}


def custom_event(tid, name, event):
    return {"accountId": "0", "containerId": "0", "triggerId": str(tid), "name": name, "type": "CUSTOM_EVENT",
            "customEventFilter": [{"type": "EQUALS", "parameter": [
                {"type": "TEMPLATE", "key": "arg0", "value": "{{_event}}"},
                {"type": "TEMPLATE", "key": "arg1", "value": event}]}]}


def tag(tid, name, ttype, params, triggers, paused=False, setup=None):
    t = {"accountId": "0", "containerId": "0", "tagId": str(tid), "name": name, "type": ttype,
         "parameter": params, "firingTriggerId": [str(x) for x in triggers], "tagFiringOption": "ONCE_PER_EVENT",
         "monitoringMetadata": {"type": "MAP"}, "consentSettings": {"consentStatus": "NOT_SET"}}
    if paused:
        t["paused"] = True
    if setup:
        t["setupTag"] = [{"tagName": setup, "stopOnSetupFailure": False}]
    return t


def ga4_event(tid, name, event, params, trigger):
    table = [{"type": "MAP", "map": [
        {"type": "TEMPLATE", "key": "parameter", "value": p},
        {"type": "TEMPLATE", "key": "parameterValue", "value": v}]} for p, v in params]
    return tag(tid, name, "gaawe", [
        {"type": "BOOLEAN", "key": "sendEcommerceData", "value": "false"},
        {"type": "TEMPLATE", "key": "eventName", "value": event},
        {"type": "TEMPLATE", "key": "measurementIdOverride", "value": "{{Const - GA4 Measurement ID}}"},
        {"type": "LIST", "key": "eventSettingsTable", "list": table}], [trigger])


META_BASE = (
    "<script>\n"
    "!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?"
    "n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;"
    "n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;"
    "t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,"
    "'script','https://connect.facebook.net/en_US/fbevents.js');\n"
    "fbq('init', '{{Const - Meta Pixel ID}}');\n"
    "fbq('track', 'PageView');\n"
    "</script>"
)

variables = [
    const(1, "Const - GA4 Measurement ID", ga4),
    const(2, "Const - Google Ads Conversion ID (numbers only)", "000000000"),
    const(3, "Const - Google Ads Lead Label", "XXXXXXXXXXXXXXXXXXXX"),
    const(4, "Const - Meta Pixel ID", "000000000000000"),
    dlv(5, "DLV - interest", "interest"),
    dlv(6, "DLV - budget", "budget"),
    dlv(7, "DLV - form", "form"),
    dlv(8, "DLV - location", "location"),
]

triggers = [
    custom_event(30, "CE - generate_lead", "generate_lead"),
    custom_event(31, "CE - whatsapp_click", "whatsapp_click"),
    custom_event(32, "CE - email_click", "email_click"),
]

tags = [
    tag(1, "Google tag (GA4)", "googtag",
        [{"type": "TEMPLATE", "key": "tagId", "value": "{{Const - GA4 Measurement ID}}"}], [ALL_PAGES]),
    ga4_event(2, "GA4 - generate_lead", "generate_lead",
              [("form", "{{DLV - form}}"), ("interest", "{{DLV - interest}}"), ("budget", "{{DLV - budget}}")], 30),
    ga4_event(3, "GA4 - whatsapp_click", "whatsapp_click", [("location", "{{DLV - location}}")], 31),
    ga4_event(4, "GA4 - email_click", "email_click", [("location", "{{DLV - location}}")], 32),
    tag(5, "Conversion Linker", "gclidw", [
        {"type": "BOOLEAN", "key": "enableCrossDomain", "value": "false"},
        {"type": "BOOLEAN", "key": "enableUrlPassthrough", "value": "false"},
        {"type": "BOOLEAN", "key": "enableCookieOverrides", "value": "false"}], [ALL_PAGES]),
    tag(6, "Google Ads - lead conversion (paused until the account exists)", "awct", [
        {"type": "BOOLEAN", "key": "enableNewCustomerReporting", "value": "false"},
        {"type": "BOOLEAN", "key": "enableConversionLinker", "value": "true"},
        {"type": "BOOLEAN", "key": "enableProductReporting", "value": "false"},
        {"type": "BOOLEAN", "key": "enableEnhancedConversion", "value": "false"},
        {"type": "TEMPLATE", "key": "conversionCookiePrefix", "value": "_gcl"},
        {"type": "BOOLEAN", "key": "enableShippingData", "value": "false"},
        {"type": "TEMPLATE", "key": "conversionId", "value": "{{Const - Google Ads Conversion ID (numbers only)}}"},
        {"type": "TEMPLATE", "key": "conversionLabel", "value": "{{Const - Google Ads Lead Label}}"},
        {"type": "BOOLEAN", "key": "rdp", "value": "false"}], [30], paused=True),
    tag(7, "Meta Pixel - base (paused until the pixel exists)", "html", [
        {"type": "TEMPLATE", "key": "html", "value": META_BASE},
        {"type": "BOOLEAN", "key": "supportDocumentWrite", "value": "false"}], [ALL_PAGES], paused=True),
    tag(8, "Meta Pixel - Lead (paused until the pixel exists)", "html", [
        {"type": "TEMPLATE", "key": "html", "value": "<script>fbq('track', 'Lead');</script>"},
        {"type": "BOOLEAN", "key": "supportDocumentWrite", "value": "false"}], [30], paused=True,
        setup="Meta Pixel - base (paused until the pixel exists)"),
]

builtins = [{"accountId": "0", "containerId": "0", "type": t, "name": n} for t, n in [
    ("PAGE_URL", "Page URL"), ("PAGE_HOSTNAME", "Page Hostname"), ("PAGE_PATH", "Page Path"),
    ("REFERRER", "Referrer"), ("EVENT", "Event"), ("CLICK_URL", "Click URL"), ("CLICK_TEXT", "Click Text")]]

doc = {
    "exportFormatVersion": 2,
    "exportTime": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    "containerVersion": {
        "path": "accounts/0/containers/0/versions/0",
        "accountId": "0", "containerId": "0", "containerVersionId": "0",
        "container": {"path": "accounts/0/containers/0", "accountId": "0", "containerId": "0",
                      "name": "alumarketing.co.il", "publicId": "GTM-XXXXXXX", "usageContext": ["WEB"]},
        "tag": tags, "trigger": triggers, "variable": variables, "builtInVariable": builtins,
    },
}

with open(out, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
print(out, "written:", len(tags), "tags,", len(triggers), "triggers,", len(variables), "variables; GA4 id:", ga4)
