#!/usr/bin/env python3
"""python3 build.py -> docs/. Data: data/sba-7a-summary.json (made by data/analyze_sba_7a.py from SBA FOIA CSVs)."""
import os,json
V="October 21, 2026"; SITE="Small Business Buyer Guide"
S=json.load(open("data/sba-7a-summary.json"))
NAV=[("index.html","Home"),("evaluate-a-business-checklist.html","Checklist"),("sba-loan-chargeoff-rates-by-industry.html","Industry outcomes"),
     ("sba-acquisition-loans.html","Acquisition loans"),("sba-loan-size-and-terms-by-industry.html","Loan sizes & terms"),("what-small-businesses-sell-for.html","Sale prices")]
CSS="""*{box-sizing:border-box}body{margin:0;font:17px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1d232a;background:#fbfbf9}
header{background:#1f3b2d;color:#fff}header .w{display:flex;flex-wrap:wrap;gap:.4rem 1rem;align-items:center;padding:.7rem 1rem}header a{color:#fff;text-decoration:none}
.brand{font-weight:700;margin-right:auto}nav a{font-size:.93rem;opacity:.9}.w{max-width:800px;margin:0 auto;padding:1rem}h1{line-height:1.2;font-size:1.8rem}h2{margin-top:2rem;font-size:1.3rem}
.t{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:.93rem}th,td{border:1px solid #ccd;padding:.4rem .5rem;text-align:left}th{background:#eef2ee}td.n{text-align:right}
.note{background:#fff8e1;border-left:4px solid #e0a800;padding:.6rem .9rem;margin:1rem 0}.aff{border:2px dashed #9aa;padding:.6rem .9rem;margin:1rem 0;color:#556;font-size:.92rem}
.meta,.src{color:#556;font-size:.9rem}footer{border-top:1px solid #dde;margin-top:2rem;font-size:.88rem;color:#556}a{color:#0a58ca}li{margin:.25rem 0}"""
DISC='<div class="note"><strong>Not financial, legal, or tax advice.</strong> Independent site, not affiliated with the SBA, any lender, or any marketplace. Historical loan data describes past loans, not your deal.</div>'
def aff(slot): return f'<!-- AFFILIATE-SLOT:{slot} --><div class="aff">[Affiliate placeholder: {slot}. Not active.]</div>'
def page(fn,title,desc,body,sources=None):
  nav=" ".join(f'<a href="{h}">{t}</a>' for h,t in NAV); src=""
  if sources: src='<h2>Sources</h2><ul class="src">'+"".join(f'<li><a href="{u}">{t}</a></li>' for t,u in sources)+f'</ul><p class="meta">Last verified: {V}.</p>'
  open("docs/"+fn,"w").write(f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | {SITE}</title><meta name="description" content="{desc}"><link rel="stylesheet" href="style.css"></head><body>
<header><div class="w"><a class="brand" href="index.html">{SITE}</a><nav>{nav}</nav></div></header><main class="w">{body}{DISC}{src}</main>
<footer><div class="w">{SITE}: independent, data-first guides for people buying a small business. <a href="disclaimer.html">Disclaimer</a> · <a href="affiliate-disclosure.html">Affiliate disclosure</a></div></footer></body></html>""")
FOIA="https://data.sba.gov/dataset/7a-504-foia"
BBS="https://www.bizbuysell.com/insight-report/"
SRC_SBA=[("SBA 7(a) & 504 FOIA loan-level data (files as of June 30, 2026) and data dictionary",FOIA),
         ("Our analysis script and summary output (GitHub)","https://github.com/mattski360/small-business-buyer-guide/tree/main/data")]
IND=[("238220","HVAC & plumbing contractors"),("561730","Landscaping services"),("811192","Car washes"),("812310","Coin-operated laundries & drycleaners"),("722513","Limited-service restaurants (comparison)"),("ALL","All 7(a) loans")]
m=lambda x:f"${x:,.0f}"; p=lambda x:f"{x:.1%}"; c=lambda x:f"{x:,}"
os.makedirs("docs",exist_ok=True); open("docs/style.css","w").write(CSS); open("docs/.nojekyll","w").write("")
METHOD="""<h2>How we calculated this</h2><ul><li>Source: SBA 7(a) FOIA loan-level files, data as of June 30, 2026.</li>
<li>Loans counted: every 7(a) loan with that NAICS code, <strong>excluding cancelled and undisbursed</strong> loans.</li>
<li>Charge-off rate (count) = loans with status "Charged Off" ÷ loans counted. Charge-off $ rate = total gross charge-off amount ÷ total gross approved amount.</li>
<li>SBA withholds the status of loans that are still active (FOIA Exemption 4), so younger cohorts look better than they will end up. That's why FY2010-2019 is our main cohort.</li></ul>"""

r10=S["fy10_19"]; r20=S["fy20p"]
rows="".join(f"<tr><td>{n}</td><td>{k if k!='ALL' else '—'}</td><td class=n>{c(r10[k]['n'])}</td><td class=n>{p(r10[k]['co_rate'])}</td><td class=n>{p(r10[k]['co_dollar'])}</td></tr>" for k,n in IND)
page("sba-loan-chargeoff-rates-by-industry.html","SBA loan charge-off rates by industry: HVAC, landscaping, car washes, laundromats",
 "How often SBA 7(a) loans made in FY2010-2019 were charged off, by industry, from SBA's own loan-level data.",
 f"""<h1>Which industries hold up? SBA 7(a) charge-off rates by industry</h1>
<p>Out of hundreds of thousands of SBA 7(a) loans made from fiscal 2010 to 2019, what share were eventually charged off (written off as a loss)? It's one rough, public signal of how businesses in an industry hold up under debt.</p>
<h2>FY2010-2019 loans</h2><div class=t><table><tr><th>Industry</th><th>NAICS</th><th>Loans</th><th>Charged off (count)</th><th>Charged off ($ of approved)</th></tr>{rows}</table></div>
<h2>What it shows</h2><ul>
<li>In this cohort, laundromats/drycleaners ({p(r10['812310']['co_rate'])}) and car washes ({p(r10['811192']['co_rate'])}) were charged off less often than all 7(a) loans ({p(r10['ALL']['co_rate'])}), and well below limited-service restaurants ({p(r10['722513']['co_rate'])}).</li>
<li>HVAC/plumbing and landscaping came in at {p(r10['238220']['co_rate'])} and {p(r10['561730']['co_rate'])} by count. Their dollar loss rates were higher than car washes or laundries, partly because those loans are smaller and shorter (see <a href="sba-loan-size-and-terms-by-industry.html">loan sizes &amp; terms</a>).</li>
<li>These numbers cover every use of loan funds (startups, expansions, acquisitions, real estate), not just business purchases. For purchases, see <a href="sba-acquisition-loans.html">acquisition loans</a>.</li></ul>
{METHOD}{aff("sba-lender-marketplace")}""",SRC_SBA)

def own_rows(R): return "".join(f"<tr><td>{n}</td><td class=n>{c(R[k]['own']['n'])}</td><td class=n>{m(R[k]['own']['median'])}</td><td class=n>{p(R[k]['own']['co_rate'])}</td></tr>" for k,n in IND)
page("sba-acquisition-loans.html","SBA loans to buy a business: counts, sizes, and outcomes by industry",
 "SBA 7(a) loans flagged 'Change of Ownership' by industry: how many, median size, and charge-off share, from SBA FOIA data.",
 f"""<h1>SBA loans used to buy a business, by industry</h1>
<p>SBA's loan data marks some loans with a business age of <strong>"Change of Ownership"</strong>, meaning the borrower bought an existing business. Here's how those loans break down.</p>
<h2>FY2020 to present (approved Oct 2019 to June 2026)</h2>
<div class=t><table><tr><th>Industry</th><th>Change-of-ownership loans</th><th>Median loan</th><th>Charged off so far</th></tr>{own_rows(r20)}</table></div>
<p class=meta>Most of these loans are still active, so their charge-off share will rise over time. Don't read the "so far" column as a final loss rate.</p>
<h2>FY2010-2019</h2>
<div class=t><table><tr><th>Industry</th><th>Change-of-ownership loans</th><th>Median loan</th><th>Charged off</th></tr>{own_rows(r10)}</table></div>
<p class=meta>Caution: far fewer FY2010-2019 loans carry the "Change of Ownership" label ({c(r10['ALL']['own']['n'])} vs {c(r20['ALL']['own']['n'])} since FY2020), and the business-age categories differ between the two files. It looks like the label wasn't used consistently in earlier years, so treat this older table as a small sample.</p>
<h2>Takeaways</h2><ul>
<li>Acquisition loans are much larger than the typical 7(a) loan. Since FY2020 the median change-of-ownership loan is {m(r20['ALL']['own']['median'])}, vs {m(r20['ALL']['median'])} for all 7(a) loans.</li>
<li>Car-wash acquisitions are the biggest of these industries (median {m(r20['811192']['own']['median'])}), likely because of land and equipment. That's our inference, not something the data states.</li></ul>
{METHOD}{aff("sba-acquisition-lender")}{aff("business-acquisition-financing-alt")}""",SRC_SBA)

trow=lambda R:"".join(f"<tr><td>{n}</td><td class=n>{m(R[k]['median'])}</td><td class=n>{R[k]['term']:.0f} mo</td><td class=n>{R[k]['rate']:.2f}%</td><td class=n>{R[k]['fixed_share']:.0%}</td></tr>" for k,n in IND)
page("sba-loan-size-and-terms-by-industry.html","SBA 7(a) loan sizes, terms, and rates by industry",
 "Median SBA 7(a) loan amount, term, initial interest rate, and fixed-rate share by industry, FY2010-2019 vs FY2020-present.",
 f"""<h1>SBA 7(a) loan sizes, terms and rates by industry</h1><p>How these industries actually got financed, from SBA's loan-level data. All figures are medians across loans (cancelled and undisbursed loans excluded).</p>
<h2>FY2020 to present</h2><div class=t><table><tr><th>Industry</th><th>Median loan</th><th>Median term</th><th>Median initial rate</th><th>Fixed-rate share</th></tr>{trow(r20)}</table></div>
<h2>FY2010-2019</h2><div class=t><table><tr><th>Industry</th><th>Median loan</th><th>Median term</th><th>Median initial rate</th><th>Fixed-rate share</th></tr>{trow(r10)}</table></div>
<ul><li>Car-wash loans have by far the longest median term ({r20['811192']['term']:.0f} months since FY2020), consistent with real estate being part of many deals (our inference).</li>
<li>Rates are the <em>initial</em> rate at approval. Most 7(a) loans here are variable rate, so the rate a borrower actually paid could differ.</li>
<li>Rates are higher in the FY2020+ cohort, which reflects the rate environment when those loans were made.</li></ul>
{aff("loan-calculator-or-lender")}""",SRC_SBA)

page("what-small-businesses-sell-for.html","What small businesses sell for: cash-flow multiples and median prices (Q3 2026)",
 "Median sale prices and average cash-flow multiples for U.S. small businesses from BizBuySell's Q3 2026 Insight Report.",
 """<h1>What small businesses sell for (Q3 2026)</h1>
<p>From BizBuySell's quarterly Insight Report, which is built from closed sales that brokers report voluntarily. It's the most widely cited public benchmark for Main Street deals, but it's a sample, not every sale.</p>
<h2>Q3 2026 headline numbers</h2><div class=t><table><tr><th>Metric</th><th>Value</th></tr>
<tr><td>Businesses reported sold</td><td>2,132</td></tr><tr><td>Median sale price</td><td>$350,000</td></tr>
<tr><td>Median cash flow</td><td>$156,000</td></tr><tr><td>Median revenue</td><td>$669,801</td></tr></table></div>
<h2>Average multiples by deal size</h2><div class=t><table><tr><th>Segment</th><th>Avg cash-flow multiple</th><th>Avg revenue multiple</th><th>Median price</th><th>Median cash flow</th></tr>
<tr><td>Sold above $1M</td><td>3.73x</td><td>0.97x</td><td>$1.8M</td><td>$559,000</td></tr>
<tr><td>Sold below $1M</td><td>2.30x</td><td>0.62x</td><td>$250,000</td><td>$123,000</td></tr></table></div>
<h2>By sector (where BizBuySell reported it)</h2><ul>
<li><strong>Service:</strong> 992 sales, median price $350,000, median cash flow $157,378.</li>
<li><strong>Manufacturing:</strong> median price $807,000, average cash-flow multiple 3.02x (highest of the major sectors).</li>
<li><strong>Restaurants:</strong> 358 sales, median price $235,000, average cash-flow multiple 2.39x.</li>
<li><strong>Retail:</strong> 417 sales, median price $272,500, median cash flow $119,285.</li></ul>
<p>One broker quoted in the report put it this way: "SDE multiples held steady near 2.0x–3.0x for main street businesses." That's an attributed opinion, not a computed statistic.</p>
<h2>How to use this</h2><ul><li>A multiple only means something once you know which earnings figure it's applied to. Confirm how the seller calculated cash flow and add-backs.</li>
<li>Smaller deals traded at noticeably lower multiples than larger ones in this quarter.</li></ul>
""" + aff("valuation-tool-or-marketplace"),
 [("BizBuySell Insight Report (Q3 2026)",BBS)])

page("evaluate-a-business-checklist.html","How to evaluate a small business for sale: a buyer's checklist",
 "A practical checklist for evaluating a small business for sale: earnings, customers, owner dependence, financing fit.",
 """<h1>How to evaluate a small business for sale</h1><p>A working checklist, roughly in the order you'll need it. Bring in a CPA and an attorney for the deal itself.</p>
<h2>1. First screen (before an NDA)</h2><ul><li>Asking price vs stated cash flow: compare to <a href="what-small-businesses-sell-for.html">published multiples</a>.</li>
<li>Industry track record: see <a href="sba-loan-chargeoff-rates-by-industry.html">SBA loan outcomes by industry</a>.</li><li>Why is the owner selling, and why now?</li><li>Is the location, license, or lease transferable?</li></ul>
<h2>2. Earnings quality</h2><ul><li>3 years of tax returns, P&amp;Ls and balance sheets, and whether they agree.</li><li>Every add-back to cash flow, documented and defensible.</li>
<li>Bank deposits reconciled to reported revenue.</li><li>Trend: growing, flat, or declining, and why.</li></ul>
<h2>3. Customers and revenue</h2><ul><li>Customer concentration: share of revenue from the top 1, 5 and 10 customers.</li><li>Recurring vs one-time revenue; contracts and whether they transfer.</li><li>Seasonality.</li></ul>
<h2>4. Owner dependence and people</h2><ul><li>What does the owner personally do each week? Who else can do it?</li><li>Key employees: tenure, pay vs market, likelihood they stay.</li><li>Will the seller agree to a transition period?</li></ul>
<h2>5. Assets and operations</h2><ul><li>Equipment age, condition, and replacement cost.</li><li>Lease terms remaining, renewal options, rent vs market.</li><li>Working capital and inventory needed at close.</li></ul>
<h2>6. Financing fit</h2><ul><li>Does cash flow cover debt payments with room to spare after paying yourself?</li><li>How much cash you'll put in, and whether the seller will carry a note.</li>
<li>What similar deals borrowed: see <a href="sba-acquisition-loans.html">SBA acquisition loans by industry</a>.</li></ul>
<h2>7. Before you close</h2><ul><li>Letter of intent terms, then a due diligence period.</li><li>Professional review of the financials (CPA) and purchase agreement (attorney).</li><li>Insurance, licenses and permits for the new owner.</li></ul>
""" + aff("diligence-or-qoe-service") + aff("deal-marketplace"))

page("index.html","Data-driven guides for buying a small business","Independent, data-first guides for small-business buyers: industry outcomes, sale multiples, and how deals get financed.",
 f"""<h1>Buying a small business? Start with the data.</h1>
<p>Plain, sourced numbers for buyers: which industries hold up, what businesses sell for, and how deals actually get financed. Every number links to its public source.</p>
<ul><li><a href="evaluate-a-business-checklist.html">How to evaluate a small business for sale (checklist)</a></li>
<li><a href="sba-loan-chargeoff-rates-by-industry.html">SBA loan charge-off rates by industry</a>: laundromats {p(r10['812310']['co_rate'])}, car washes {p(r10['811192']['co_rate'])}, all loans {p(r10['ALL']['co_rate'])} (FY2010-2019)</li>
<li><a href="sba-acquisition-loans.html">SBA loans used to buy a business</a>: {c(r20['ALL']['own']['n'])} since FY2020, median {m(r20['ALL']['own']['median'])}</li>
<li><a href="sba-loan-size-and-terms-by-industry.html">Loan sizes, terms and rates by industry</a></li>
<li><a href="what-small-businesses-sell-for.html">What small businesses sell for (Q3 2026)</a></li></ul>""",
 [("SBA 7(a) FOIA data",FOIA),("BizBuySell Insight Report",BBS)])

page("disclaimer.html","Disclaimer","Disclaimer","""<h1>Disclaimer</h1><p>Small Business Buyer Guide is an independent informational site. It is not affiliated with or endorsed by the U.S. Small Business Administration, any lender, broker, or marketplace.</p>
<p>Nothing here is financial, investment, legal, or tax advice. Historical loan statistics describe past loans and don't predict any individual business or deal. Do your own due diligence and consult qualified professionals.</p>
<p>We compute figures from public data and publish our method and code. If you find an error, the original source wins.</p>""")
page("affiliate-disclosure.html","Affiliate disclosure","Affiliate disclosure","""<h1>Affiliate disclosure</h1><p>Some pages may link to lenders, marketplaces, or services. If you use some of those links, we may earn a commission or referral fee at no extra cost to you. Such links will be labeled.</p>
<p>Compensation doesn't change our data. Every figure comes from a cited public source.</p><p class="meta">As of October 21, 2026, this site has no active affiliate relationships.</p>""")
print("built")
