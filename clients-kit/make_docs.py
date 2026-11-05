#!/usr/bin/env python3
"""Klaarwerk client documents: proposal letter, quote and invoice in the email-proposal style.

Usage:  python3 make_docs.py client.json OUTDIR [--html-only]
Writes  OUTDIR/<Doc> - <Business>.pdf (+ .html) for letter, quote and the deposit/balance invoices.
"""
import base64, html, json, pathlib, subprocess, sys

KIT = pathlib.Path(__file__).resolve().parent
FONTS = KIT.parent / "social/kit/fonts"
E = html.escape

PACKAGES = {
    "Starter": (6500, "Up to 5 pages, copywriting, .co.za domain for the first year, WhatsApp and call buttons, mobile-first design"),
    "Business": (12500, "Up to 10 pages, everything in Starter, quote or booking form, Google Business Profile setup, local SEO, professional email address"),
    "Online Store": (22000, "Up to 50 products loaded, card and EFT payments, courier options, order notifications to WhatsApp, training call"),
}
TERMS_URL = "klaarwerk.co.za/terms.html"


def b64(p):
    return base64.b64encode(pathlib.Path(p).read_bytes()).decode()


def rand(n):
    return "R{:,.2f}".format(n)


def rand0(n):
    return "R{:,.0f}".format(n)


CSS = """
@font-face{font-family:'Bricolage';src:url(data:font/ttf;base64,%(bri)s);font-weight:200 800}
@font-face{font-family:'Familjen';src:url(data:font/woff2;base64,%(f4)s);font-weight:400}
@font-face{font-family:'Familjen';src:url(data:font/woff2;base64,%(f6)s);font-weight:600}
@font-face{font-family:'Familjen';src:url(data:font/woff2;base64,%(f7)s);font-weight:700}
@font-face{font-family:'Mono';src:url(data:font/woff2;base64,%(mono)s);font-weight:500}
@page{size:A4;margin:12mm 14mm}
*{box-sizing:border-box}
html,body{background:#F3F5F2}
body{margin:0;font-family:'Familjen',Arial,sans-serif;color:#13232B;font-size:13px;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.card{background:#fff;border-radius:16px;overflow:hidden}
.head{background:#0E6E55;padding:24px 32px 26px;display:flex;justify-content:space-between;align-items:flex-end;gap:20px}
.head img{width:180px;display:block}
.head h1{font-family:'Bricolage',Arial,sans-serif;font-weight:800;font-size:29px;line-height:1.12;margin:18px 0 0;color:#fff;letter-spacing:-.4px}
.hl{background:#F2BE22;color:#13232B;padding:0 6px;border-radius:4px;-webkit-box-decoration-break:clone;box-decoration-break:clone}
.tag{font-size:13px;color:#E3EDE7;margin-top:8px}
.ref{flex:none;text-align:right;color:#E3EDE7;font-size:11.5px;line-height:1.65;white-space:nowrap}
.ref b{color:#fff;font-size:14px;display:block;font-family:'Mono',monospace;letter-spacing:1px}
.body{padding:22px 32px 6px}
p{margin:0 0 10px}
.lbl,h2,.steps small,.pay small{font-family:'Mono',monospace;font-weight:500;letter-spacing:1px;text-transform:uppercase;color:#0E6E55}
.lbl{font-size:10px;margin-bottom:4px}
h2{font-size:11px;margin:16px 0 7px}
.parties{display:flex;gap:16px;margin-bottom:16px}
.parties>div{flex:1;background:#F3F5F2;border-radius:10px;padding:11px 14px;font-size:12.5px}
ul{margin:0 0 8px;padding-left:18px}li{margin:0 0 4px}
.steps,.pay{display:flex;gap:10px;margin:4px 0 14px}
.steps div,.pay div{flex:1;border-top:3px solid #13232B;padding-top:8px}
.steps small,.pay small{display:block;font-size:10px}
.steps b{font-family:'Bricolage';font-weight:700;font-size:15px}
.pay b{font-family:'Bricolage';font-weight:800;font-size:18px}
table{width:100%;border-collapse:collapse;break-inside:avoid;font-size:12.5px}
th{text-align:left;font-size:10.5px;color:#56656B;font-weight:600;padding:6px 8px;border-bottom:2px solid #13232B}
td{padding:8px;border-bottom:1px solid #D6DDD8;vertical-align:top}
th.r,td.r{text-align:right;white-space:nowrap}
td small{display:block;color:#56656B;font-size:11.5px;margin-top:2px}
tr.rec td{background:#E3EDE7}
.badge{display:inline-block;font-size:9.5px;font-weight:700;color:#fff;background:#0E6E55;border-radius:99px;padding:1px 7px;margin-left:6px;vertical-align:1px}
.tot{margin-top:4px}.tot td{border:0;padding:5px 8px}
.grand td{background:#E3EDE7;font-family:'Bricolage';font-weight:800;font-size:16px;padding:10px 8px}
.grand td:first-child{border-radius:8px 0 0 8px}.grand td:last-child{border-radius:0 8px 8px 0}
.note{font-size:11.5px;color:#56656B}
.cta{background:#E3EDE7;border-radius:12px;padding:14px 18px;margin:14px 0 16px;font-size:13.5px}
.cta span{color:#0E6E55}
.bank{border:2px dashed #F2BE22;border-radius:12px;padding:12px 16px;margin:6px 0 12px}
.bank td{border:0;padding:3px 8px 3px 0}
.sig a{color:#0E6E55;text-decoration:none}
.sign{display:flex;gap:24px;margin:22px 0 8px}
.sign div{flex:1;border-top:1px solid #13232B;padding-top:5px;font-size:11px;color:#56656B}
.paid{display:inline-block;font-family:'Mono';font-size:11px;letter-spacing:1px;border:2px solid #F2BE22;color:#13232B;background:#F2BE22;border-radius:6px;padding:2px 8px}
.foot{padding:0 32px 18px}.foot div{border-top:1px solid #D6DDD8;padding-top:10px;font-size:10.5px;color:#56656B}
.pb{break-before:page;padding-top:2px}
"""


def page(title, headline, highlight, tag, ref_html, body, foot_extra=""):
    css = CSS
    for k, f in dict(bri="bricolage.ttf", f4="familjen-grotesk-latin-400-normal.woff2", f6="familjen-grotesk-latin-600-normal.woff2",
                     f7="familjen-grotesk-latin-700-normal.woff2", mono="jetbrains-mono-latin-500-normal.woff2").items():
        css = css.replace("%(" + k + ")s", b64(FONTS / f))
    logo = b64(KIT / "logo-white.png")
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{E(title)}</title><style>{css}</style></head><body><div class="card">
<div class="head"><div><img src="data:image/png;base64,{logo}" alt="Klaarwerk">
<h1>{E(headline)} <span class="hl">{E(highlight)}</span></h1><div class="tag">{E(tag)}</div></div>
<div class="ref">{ref_html}</div></div>
<div class="body">{body}</div>
<div class="foot"><div>Klaarwerk Studio &middot; Delmas, Mpumalanga &middot; jared.klaarwerk@gmail.com &middot; WhatsApp 066 205 4680 &middot; tinyurl.com/Klaarwerk<br>From R6,500 once-off &middot; 50% deposit, balance at launch &middot; Terms: {TERMS_URL}{foot_extra}</div></div>
</div></body></html>"""


def parties(c, left="Prepared for"):
    return f"""<div class="parties"><div><div class="lbl">{left}</div><b>{E(c['owner'])}</b><br>{E(c['business'])}<br>{E(c['area'])}{('<br>' + E(c['email'])) if c.get('email') else ''}</div>
<div><div class="lbl">From</div><b>Klaarwerk Studio</b><br>Jared Viviers &middot; Delmas, Mpumalanga<br>jared.klaarwerk@gmail.com &middot; 066 205 4680</div></div>"""


STEPS = """<div class="steps"><div><small>Day 1</small><b>One call</b></div><div><small>Day 2&ndash;9</small><b>We build</b></div><div><small>Day 10&ndash;12</small><b>You check</b></div><div><small>Day 14</small><b>You're live</b></div></div>"""


def letter(c):
    pk = c["package"]
    price = PACKAGES[pk][0]
    ul = lambda xs: "<ul>" + "".join(f"<li>{E(x)}</li>" for x in xs) + "</ul>"
    rows = "".join(
        f"<tr{' class=rec' if n == pk else ''}><td><b>{n}</b>{'<span class=badge>Recommended</span>' if n == pk else ''}</td><td>{d}</td><td class=r><b>{rand0(p)}</b></td></tr>"
        for n, (p, d) in PACKAGES.items())
    body = f"""{parties(c)}
<p>Dear {E(c['salutation'])},</p>
{''.join(f'<p>{E(x)}</p>' for x in c['letter_intro'])}
<h2>What we found</h2>{ul(c['found'])}
<h2>What your website will do</h2>{ul(c['propose'])}
<h2 class="pb">How it works</h2>{STEPS}
<h2>Investment</h2>
<table><tr><th>Package</th><th>What's included</th><th class=r>Once-off</th></tr>{rows}</table>
<p class="note" style="margin-top:6px">Optional Care Plan: R450/month for hosting, security updates, backups and up to 1 hour of changes each month. Cancel any time.</p>
<p>For {E(c['business'])}, I recommend the <b>{pk}</b> package. {E(c['why'])} Your deposit would be <b>{rand0(price/2)}</b>, and the other {rand0(price/2)} is only due once you've approved the site. You own the website and domain. The full quote is attached as <b>{E(c['quote_no'])}</b>.</p>
<div class="cta"><b>Would you like a free mock-up of your new homepage first?</b><br><span>Just reply YES, or WhatsApp me on 066 205 4680.</span></div>
<p style="margin:0 0 4px">Kind regards,</p>
<p class="sig"><b>Jared Viviers</b><br>Founder, Klaarwerk Studio<br><a href="mailto:jared.klaarwerk@gmail.com">jared.klaarwerk@gmail.com</a> &middot; WhatsApp 066 205 4680 &middot; <a href="https://tinyurl.com/Klaarwerk">tinyurl.com/Klaarwerk</a></p>
<p class="note"><b style="color:#13232B">P.S.</b> Not the right time? If you know another business that needs a website, we pay R500 for every referral that becomes a client.</p>"""
    ref = f"<b>PROPOSAL</b>{E(c['date'])}<br>Valid until {E(c['valid_until'])}"
    return page(f"Proposal - {c['business']}", "A website proposal for", c["business"],
                "Websites for South African businesses. We do all of it.", ref, body, c.get("foot_note", ""))


def quote(c):
    pk = c["package"]
    price = PACKAGES[pk][0]
    items = "".join(
        f"<tr><td><b>{E(t)}</b><small>{E(d)}</small></td><td class=r>1</td><td class=r>{E(a)}</td></tr>"
        for t, d, a in [(f"{pk} website package", c["pages"], rand(price))] + [tuple(x) for x in c["included"]])
    body = f"""{parties(c)}
<h2>Quote</h2>
<table><tr><th>Description</th><th class=r>Qty</th><th class=r>Amount</th></tr>{items}</table>
<table class="tot"><tr><td style="width:58%"></td><td>Subtotal</td><td class=r>{rand(price)}</td></tr>
<tr class="grand"><td style="background:#fff"></td><td>Total, once-off</td><td class=r>{rand(price)}</td></tr></table>
<h2>Optional extra</h2>
<table><tr><td><b>Care Plan</b><small>Hosting, security updates, backups and up to 1 hour of changes every month. Cancel any time.</small></td><td class=r>R450.00 / month</td></tr></table>
<h2 class="pb">Payment</h2>
<div class="pay"><div><small>To start</small><b>{rand(price/2)}</b><br>50% deposit by EFT</div><div><small>When you approve the site</small><b>{rand(price/2)}</b><br>50% balance, before it goes live</div></div>
<p class="note">Banking details are on your invoice. We will never change our bank details by email or WhatsApp. If anyone asks you to pay a different account, phone us first on 066 205 4680.</p>
<h2>Terms</h2>
<ul><li>Your site is live within 14 days of the deposit and our first call. The clock pauses while we wait for your info, photos or feedback.</li>
<li>Two rounds of changes are included when you review your preview. Anything bigger after that is quoted upfront.</li>
<li>You own the website, its content and the domain.</li>
<li>The deposit is non-refundable once work has started.</li></ul>
<div class="cta"><b>Happy to go ahead?</b> <span>Sign below and WhatsApp a photo to 066 205 4680, or reply "I accept" by email. We'll send your deposit invoice the same day.</span></div>
<div class="lbl">Acceptance</div>
<div class="sign"><div>Name</div><div>Signature</div><div>Date</div></div>"""
    ref = f"<b>{E(c['quote_no'])}</b>Date: {E(c['date'])}<br>Valid until: {E(c['valid_until'])}"
    return page(f"Quote {c['quote_no']} - {c['business']}", "Quote for", c["business"],
                f"{pk} website package · live in 14 days", ref, body, c.get("foot_note", ""))


def invoice(c, kind):
    pk = c["package"]
    half = PACKAGES[pk][0] / 2
    inv = c["invoices"][kind]
    label = "Deposit (50%)" if kind == "deposit" else "Balance (50%)"
    when = "Work starts as soon as this payment clears." if kind == "deposit" else "Your website goes live as soon as this payment clears."
    bank = c.get("bank") or {}
    brow = lambda k, lbl: f"<tr><td style='color:#56656B;width:38%'>{lbl}</td><td><b>{E(bank.get(k) or '[add before sending]')}</b></td></tr>"
    body = f"""{parties(c, 'Billed to')}
<h2>Invoice</h2>
<table><tr><th>Description</th><th class=r>Amount</th></tr>
<tr><td><b>{pk} website package: {label}</b><small>Quote {E(c['quote_no'])}. Package total {rand(half*2)}.</small></td><td class=r>{rand(half)}</td></tr></table>
<table class="tot"><tr class="grand"><td style="background:#fff;width:58%"></td><td>Amount due</td><td class=r>{rand(half)}</td></tr></table>
<h2>Pay by EFT</h2>
<div class="bank"><table>{brow('account_name','Account name')}{brow('bank','Bank')}{brow('account_no','Account number')}{brow('branch','Branch code')}{brow('type','Account type')}
<tr><td style='color:#56656B'>Reference</td><td><b>{E(inv['no'])}</b></td></tr></table></div>
<p>Please pay by <b>{E(inv['due'])}</b> and use <b>{E(inv['no'])}</b> as your reference. {when}</p>
<p class="note">We will never change our bank details by email or WhatsApp. If anyone asks you to pay a different account, phone us first on 066 205 4680.</p>
<div class="cta"><b>Thank you for choosing Klaarwerk Studio!</b><br><span>Questions about this invoice? WhatsApp 066 205 4680.</span></div>"""
    ref = f"<b>{E(inv['no'])}</b>Date: {E(inv['date'])}<br>Due: {E(inv['due'])}"
    return page(f"Invoice {inv['no']} - {c['business']}", "Invoice for", c["business"], label + " · " + pk + " website",
                ref, body, c.get("foot_note", ""))


def to_pdf(html_path, pdf_path):
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
          f"await p.goto('file://{html_path}');await p.evaluate(()=>document.fonts.ready);"
          f"await p.pdf({{path:{json.dumps(str(pdf_path))},format:'A4',printBackground:true}});await b.close();}})()")
    subprocess.run(["node", "-e", js], check=True)


def main():
    c = json.loads(pathlib.Path(sys.argv[1]).read_text())
    out = pathlib.Path(sys.argv[2]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    biz = c["business"].replace("&", "and").replace("/", "-")
    docs = [(f"01 Proposal letter - {biz}", letter(c)), (f"02 Quote {c['quote_no']} - {biz}", quote(c))]
    for k in ("deposit", "balance"):
        if k in c.get("invoices", {}):
            docs.append((f"03 Invoice {c['invoices'][k]['no']} ({k}) - {biz}", invoice(c, k)))
    for name, h in docs:
        hp = out / (name + ".html")
        hp.write_text(h)
        if "--html-only" not in sys.argv:
            to_pdf(hp, out / (name + ".pdf"))
        print(out / name)


if __name__ == "__main__":
    main()
