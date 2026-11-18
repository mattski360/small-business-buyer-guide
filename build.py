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
def page(fn,title,desc,body,sources=None,verified=V):
  nav=" ".join(f'<a href="{h}">{t}</a>' for h,t in NAV); src=""
  if sources: src='<h2>Sources</h2><ul class="src">'+"".join(f'<li><a href="{u}">{t}</a></li>' for t,u in sources)+f'</ul><p class="meta">Last verified: {verified}.</p>'
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

# ---- Industry deep dives (content-plan items 1-3). Data: data/industry-deep-dives.json (made by data/analyze_industries.py) ----
D=json.load(open("data/industry-deep-dives.json")); V2="October 28, 2026"
CBP="https://www.census.gov/data/datasets/2023/econ/cbp/2023-cbp.html"
SRC_DD=[("SBA 7(a) & 504 FOIA loan-level data (files as of June 30, 2026)",FOIA),
        ("SBA 7(a)/504 FOIA data dictionary (loan status and field definitions)","https://data.sba.gov/sites/default/files/uploaded_resources/7a_504_foia_data_dictionary.xlsx"),
        ("U.S. Census Bureau, County Business Patterns 2023 (national and state files)",CBP),
        ("Census CBP methodology (noise flags, what's in scope)","https://www.census.gov/programs-surveys/cbp/technical-documentation/methodology.html"),
        ("Our analysis scripts and outputs (GitHub)","https://github.com/mattski360/small-business-buyer-guide/tree/main/data")]
A10=S["fy10_19"]["ALL"]; A20=S["fy20p"]["ALL"]; A20own=A20["own"]["n"]/A20["n"]
DDS=[("811111","auto-repair-shop-sba-loan-data.html","Auto repair shops","auto repair shop"),
     ("621210","dental-practice-sba-loan-data.html","Dental practices","dental practice"),
     ("541940","veterinary-clinic-sba-loan-data.html","Veterinary clinics","veterinary clinic"),
     ("561710","pest-control-business-sba-loan-data.html","Pest control companies","pest control company"),
     ("561720","janitorial-business-sba-loan-data.html","Janitorial services","janitorial company"),
     ("238210","electrical-contractor-sba-loan-data.html","Electrical contractors","electrical contractor"),
     ("238160","roofing-contractor-sba-loan-data.html","Roofing contractors","roofing contractor"),
     ("624410","daycare-child-care-sba-loan-data.html","Child care centers","child care center"),
     ("713940","fitness-center-gym-sba-loan-data.html","Fitness centers and gyms","fitness center or gym"),
     ("531130","self-storage-facility-sba-loan-data.html","Self-storage facilities","self-storage facility"),
     ("721110","hotel-motel-sba-loan-data.html","Hotels and motels","hotel or motel"),
     ("447110","gas-station-convenience-store-sba-loan-data.html","Gas stations with convenience stores","gas station with a convenience store")]
V3="November 4, 2026"; V4="November 11, 2026"; V5="November 18, 2026"; VDATE={"561710":V3,"561720":V3,"238210":V3,"238160":V4,"624410":V4,"713940":V4,"531130":V5,"721110":V5,"447110":V5}
dm=lambda x:m(x) if x is not None else "—"; dp=lambda x:p(x) if x is not None else "—"
def dd_body(code,name,one,intro,notes):
  d=D[code]; a,b=d["7a_fy10_19"],d["7a_fy20p"]; e,f=d["504_fy10_19"],d["504_fy20p"]; us,ut=d["cbp_us"],d["cbp_ut"]
  others=" · ".join(f'<a href="{fn}">{nm}</a>' for c2,fn,nm,_ in DDS if c2!=code)
  return f"""<h1>Buying {('an ' if one[0] in 'aeiou' else 'a ')+one}? What SBA loan data and Census counts show</h1>
<p class=meta>NAICS {code} · SBA data as of June 30, 2026 · Census County Business Patterns 2023</p>
<p>{intro}</p>
<h2>SBA 7(a) loans to {name.lower()}</h2>
<div class=t><table><tr><th>Measure</th><th>FY2010-2019</th><th>FY2020 to June 2026</th><th>All 7(a), FY2010-2019</th></tr>
<tr><td>Loans (excl. cancelled/undisbursed)</td><td class=n>{c(a['n'])}</td><td class=n>{c(b['n'])}</td><td class=n>{c(A10['n'])}</td></tr>
<tr><td>Median loan</td><td class=n>{m(a['median'])}</td><td class=n>{m(b['median'])}</td><td class=n>{m(A10['median'])}</td></tr>
<tr><td>Median term</td><td class=n>{a['term']:.0f} mo</td><td class=n>{b['term']:.0f} mo</td><td class=n>{A10['term']:.0f} mo</td></tr>
<tr><td>Median initial rate</td><td class=n>{a['rate']:.2f}%</td><td class=n>{b['rate']:.2f}%</td><td class=n>{A10['rate']:.2f}%</td></tr>
<tr><td>Charged off (count)</td><td class=n>{p(a['co_rate'])}</td><td class=n>{p(b['co_rate'])} so far</td><td class=n>{p(A10['co_rate'])}</td></tr>
<tr><td>Charged off ($ of approved)</td><td class=n>{p(a['co_dollar'])}</td><td class=n>{p(b['co_dollar'])} so far</td><td class=n>{p(A10['co_dollar'])}</td></tr>
<tr><td>Franchise loans (share)</td><td class=n>{a['franchise_share']:.1%}</td><td class=n>{b['franchise_share']:.1%}</td><td class=n>—</td></tr></table></div>
<p class=meta>The FY2020+ charge-off figures will rise as those loans age; most are still active and their status is withheld by SBA. For a fair comparison, use the FY2010-2019 columns.</p>
<h2>Loans used to buy an existing {one}</h2>
<div class=t><table><tr><th>Measure</th><th>FY2010-2019</th><th>FY2020 to June 2026</th></tr>
<tr><td>"Change of Ownership" 7(a) loans</td><td class=n>{c(a['own_n'])}</td><td class=n>{c(b['own_n'])}</td></tr>
<tr><td>Share of this industry's 7(a) loans</td><td class=n>{a['own_share']:.1%}</td><td class=n>{b['own_share']:.1%} (all industries: {A20own:.1%})</td></tr>
<tr><td>Median acquisition loan</td><td class=n>{m(a['own_median'])}</td><td class=n>{m(b['own_median'])} (all industries: {m(A20['own']['median'])})</td></tr>
<tr><td>Median term</td><td class=n>{a['own_term']:.0f} mo</td><td class=n>{b['own_term']:.0f} mo</td></tr>
<tr><td>Charged off (count)</td><td class=n>{dp(a['own_co_rate'])}</td><td class=n>{dp(b['own_co_rate'])} so far</td></tr></table></div>
<p class=meta>The "Change of Ownership" label is used far more since FY2020 than before, so the FY2010-2019 column is a small, probably incomplete sample (see <a href="sba-acquisition-loans.html">acquisition loans</a>).</p>
<h2>SBA 504 loans (real estate and major equipment)</h2>
<div class=t><table><tr><th>Measure</th><th>FY2010-2019</th><th>FY2020 to June 2026</th><th>All 504, FY2010-2019</th></tr>
<tr><td>504 loans (excl. cancelled/not funded)</td><td class=n>{c(e['n'])}</td><td class=n>{c(f['n'])}</td><td class=n>{c(D['ALL504']['504_fy10_19']['n'])}</td></tr>
<tr><td>Median 504 (CDC) loan</td><td class=n>{m(e['median'])}</td><td class=n>{m(f['median'])}</td><td class=n>{m(D['ALL504']['504_fy10_19']['median'])}</td></tr>
<tr><td>Median term</td><td class=n>{e['term']:.0f} mo</td><td class=n>{f['term']:.0f} mo</td><td class=n>{D['ALL504']['504_fy10_19']['term']:.0f} mo</td></tr>
<tr><td>Charged off (count)</td><td class=n>{p(e['co_rate'])}</td><td class=n>{p(f['co_rate'])} so far</td><td class=n>{p(D['ALL504']['504_fy10_19']['co_rate'])}</td></tr></table></div>
<p class=meta>The 504 amount is SBA's CDC portion only. A bank first mortgage (in the data as third-party dollars) and the borrower's down payment fund the rest of the project.</p>
<h2>How big is the industry? (Census, 2023)</h2>
<div class=t><table><tr><th>Measure</th><th>United States</th><th>Utah</th></tr>
<tr><td>Establishments with employees</td><td class=n>{c(us['est'])}</td><td class=n>{c(ut['est'])}</td></tr>
<tr><td>Employees (mid-March)</td><td class=n>{c(us['emp'])}</td><td class=n>{c(ut['emp'])}</td></tr>
<tr><td>Employees per establishment (avg)</td><td class=n>{us['emp_per_est']:.1f}</td><td class=n>{ut['emp_per_est']:.1f}</td></tr>
<tr><td>Annual payroll per employee (avg)</td><td class=n>{m(us['pay_per_emp'])}</td><td class=n>{m(ut['pay_per_emp'])}</td></tr>
<tr><td>Establishments with fewer than 10 employees</td><td class=n>{us['share_under10']:.0%}</td><td class=n>{ut['share_under10']:.0%}</td></tr>
<tr><td>Establishments with 20+ employees</td><td class=n>{c(us['n20plus'])}</td><td class=n>{c(ut['n20plus'])}</td></tr></table></div>
<p class=meta>County Business Patterns counts only establishments with paid employees, so owner-only shops aren't included. Payroll per employee is total annual payroll ÷ mid-March employment (our calculation), which mixes full- and part-time staff.</p>
<h2>Utah</h2><p>SBA 7(a) loans with a Utah project location in this industry: {c(a['ut_n'])} in FY2010-2019 (median {dm(a['ut_median'])}) and {c(b['ut_n'])} from FY2020 to June 2026 (median {dm(b['ut_median'])}). SBA 504 loans in Utah: {c(e['ut_n'])} and {c(f['ut_n'])}. Small counts, so treat the Utah medians loosely.</p>
<h2>What it shows</h2><ul>{notes}</ul>
<h2>How we calculated this</h2><ul><li>SBA 7(a) and 504 FOIA loan-level files (as of June 30, 2026), filtered to NAICS {code}. Cancelled, undisbursed ("COMMIT") and 504 "NOT FUNDED" loans are excluded.</li>
<li>Charge-off rate (count) = loans with status "Charged Off" ÷ loans counted. Charge-off $ rate = gross charge-off amount ÷ gross approved amount.</li>
<li>Acquisition loans = loans whose BusinessAge field is "Change of Ownership". Franchise share = loans with any FranchiseCode.</li>
<li>Census figures are from the 2023 County Business Patterns national (cbp23us) and state (cbp23st) files, all legal forms of organization.</li>
<li>Covers every use of loan funds, not only purchases, unless labeled. Past loan outcomes don't predict any single deal.</li></ul>
<p>Other industry deep dives: {others}. See also <a href="sba-loan-chargeoff-rates-by-industry.html">charge-off rates by industry</a> and <a href="what-small-businesses-sell-for.html">what small businesses sell for</a>.</p>
{aff("sba-acquisition-lender")}"""
def dd(code):
  d=D[code]; a,b,us,ut=d["7a_fy10_19"],d["7a_fy20p"],d["cbp_us"],d["cbp_ut"]; e,f=d["504_fy10_19"],d["504_fy20p"]
  if code=="811111": return (
   f"There are about {c(us['est'])} auto repair shops with employees in the U.S. (Census, 2023), most of them small. Here's how SBA-backed loans to general automotive repair shops have been sized and how they turned out.",
   f"""<li>Auto repair loans charged off at {p(a['co_rate'])} by count in FY2010-2019, slightly below all 7(a) loans ({p(A10['co_rate'])}), and {p(a['co_dollar'])} of dollars vs {p(A10['co_dollar'])} overall.</li>
<li>Buying a shop is a big part of this industry's SBA lending now: {b['own_share']:.1%} of FY2020+ auto repair 7(a) loans were change-of-ownership loans, vs {A20own:.1%} across all industries. The median acquisition loan was {m(b['own_median'])}.</li>
<li>These are small businesses: {us['share_under10']:.0%} of U.S. shops with employees had fewer than 10, averaging {us['emp_per_est']:.1f} employees. Inference (ours): with that few staff, many shops likely depend heavily on the owner, which matters for a buyer's transition plan.</li>
<li>About {b['franchise_share']:.0%} of FY2020+ auto repair 7(a) loans went to franchise locations, so most financed shops are independents.</li>""")
  if code=="621210": return (
   f"Here's what {c(a['n']+b['n'])} 7(a) loans since FY2010, plus 504 and Census data, say about financing and buying a practice.",
   f"""<li>Dental loans held up far better than average: {p(a['co_rate'])} charged off by count in FY2010-2019 vs {p(A10['co_rate'])} for all 7(a) loans, and only {p(a['co_dollar'])} of dollars.</li>
<li>Loans are large. The FY2020+ median 7(a) loan was {m(b['median'])}, and the median change-of-ownership loan was {m(b['own_median'])}.</li>
<li>Practice purchases were {b['own_share']:.1%} of FY2020+ dental 7(a) loans. Startups were a bigger group ({c(b['ages'].get('Startup, Loan Funds will Open Business',0))} loans flagged "Startup").</li>
<li>Utah payroll per employee ({m(ut['pay_per_emp'])}) was well below the U.S. figure ({m(us['pay_per_emp'])}) in 2023. This data doesn't say why (staff mix, part-time share, and how owner-dentists are paid could all play a part), so don't read it as a wage benchmark.</li>
<li>Franchise loans are rare here ({b['franchise_share']:.1%} since FY2020).</li>""")
  if code=="561710": return (
   f"Pest control is a route-based service business with about {c(us['est'])} U.S. companies with employees (Census, 2023). Here's what SBA 7(a) and 504 loan data say about how these companies get financed and bought, and how the loans turned out.",
   f"""<li>Pest control loans charged off less often than average by count: {p(a['co_rate'])} in FY2010-2019 vs {p(A10['co_rate'])} for all 7(a) loans. By dollars the loss rate ({p(a['co_dollar'])}) was close to the all-loan figure ({p(A10['co_dollar'])}).</li>
<li>Franchising has grown here: {b['franchise_share']:.0%} of FY2020+ pest control 7(a) loans went to franchise locations, up from {a['franchise_share']:.0%} in FY2010-2019. Startups were also a large group ({c(b['ages'].get('Startup, Loan Funds will Open Business',0))} FY2020+ loans flagged "Startup").</li>
<li>Buyouts were {b['own_share']:.1%} of FY2020+ pest control 7(a) loans, about the all-industry share ({A20own:.1%}), with a median acquisition loan of {m(b['own_median'])}. None of those {c(b['own_n'])} acquisition loans had been charged off as of June 2026, but most are still young.</li>
<li>Most companies are small: {us['share_under10']:.0%} of U.S. pest control establishments with employees had fewer than 10 ({ut['share_under10']:.0%} in Utah). Inference (ours): at that size, the customer list and service routes are much of what a buyer is paying for, so check how many customers are on recurring contracts.</li>
<li>Utah is a small sample ({c(ut['est'])} establishments; {c(b['ut_n'])} 7(a) loans since FY2020), so treat the Utah medians loosely.</li>""")
  if code=="561720": return (
   f"Commercial cleaning companies are a common first acquisition because they're inexpensive to buy into. Here's what {c(a['n']+b['n'])} SBA 7(a) loans since FY2010, plus 504 and Census data, show about financing one and how those loans turned out.",
   f"""<li>Janitorial loans had a higher loss rate than average: {p(a['co_rate'])} charged off by count in FY2010-2019 vs {p(A10['co_rate'])} for all 7(a) loans, and {p(a['co_dollar'])} of dollars vs {p(A10['co_dollar'])}. That was the highest of our first six deep dives; roofing and fitness centers have since come in slightly higher.</li>
<li>Loans are small. The FY2010-2019 median 7(a) loan was {m(a['median'])} with a median {a['term']:.0f}-month term; since FY2020 the median is {m(b['median'])}.</li>
<li>Buying an existing company was {b['own_share']:.1%} of FY2020+ janitorial 7(a) loans, about the all-industry share ({A20own:.1%}), with a median acquisition loan of {m(b['own_median'])}. Franchise locations got {b['franchise_share']:.0%} of FY2020+ loans.</li>
<li>Payroll per employee was about {m(us['pay_per_emp'])} in the U.S. and {m(ut['pay_per_emp'])} in Utah (2023), among the lowest of our deep dives (only gas stations, child care and fitness centers are lower). Census doesn't separate full- and part-time staff, so part-time cleaning shifts likely pull this down (our inference); don't read it as a wage rate.</li>
<li>Most establishments are small ({us['share_under10']:.0%} under 10 employees), but {c(us['n20plus'])} U.S. establishments had 20 or more, which is why the average is {us['emp_per_est']:.1f} employees. Inference (ours): with low switching costs for customers, contract length and customer concentration deserve extra diligence.</li>""")
  if code=="238210": return (
   f"Electrical contracting is one of the larger skilled trades, with about {c(us['est'])} U.S. contractors with employees (Census, 2023). Here's what SBA 7(a) and 504 loan data say about financing and buying one.",
   f"""<li>By count, electrical contractor loans charged off at about the all-loan rate: {p(a['co_rate'])} in FY2010-2019 vs {p(A10['co_rate'])}. By dollars the loss rate was higher ({p(a['co_dollar'])} of approved dollars charged off vs {p(A10['co_dollar'])} for all 7(a) loans).</li>
<li>Acquisition loans are big. The median FY2020+ change-of-ownership loan was {m(b['own_median'])}, above the all-industry median of {m(A20['own']['median'])} and among the highest of the service and trade businesses in our deep dives (behind roofing and veterinary clinics; asset-heavy self-storage, gas stations and hotels are higher). Buyouts were {b['own_share']:.1%} of this industry's FY2020+ 7(a) loans, below the all-industry share ({A20own:.1%}).</li>
<li>Franchising is rare ({b['franchise_share']:.1%} of FY2020+ loans), so nearly every financed contractor is independent.</li>
<li>Payroll per employee averaged {m(us['pay_per_emp'])} nationally and {m(ut['pay_per_emp'])} in Utah (2023). Utah contractors were bigger on average ({ut['emp_per_est']:.1f} employees vs {us['emp_per_est']:.1f} nationally).</li>
<li>Inference (ours): in a licensed trade, the business may depend on the owner's or a key employee's electrical license, so confirm who holds the license and whether that person stays after the sale. The loan data doesn't capture this.</li>
<li>SBA 504 loans, which usually finance a building or major equipment, numbered {c(d['504_fy20p']['n'])} since FY2020 with a median CDC portion of {m(d['504_fy20p']['median'])}.</li>""")
  if code=="238160": return (
   f"Roofing is a big, fragmented trade: about {c(us['est'])} U.S. roofing contractors with employees (Census, 2023), {us['share_under10']:.0%} of them with fewer than 10 people. Here's what SBA 7(a) and 504 loan data say about financing and buying one, and how those loans turned out.",
   f"""<li>Roofing had the weakest loan record of our deep dives by dollars: {p(a['co_dollar'])} of approved FY2010-2019 dollars were charged off vs {p(A10['co_dollar'])} for all 7(a) loans. By count, {p(a['co_rate'])} were charged off vs {p(A10['co_rate'])} overall (about tied with fitness centers for highest).</li>
<li>Acquisition loans are large: the median FY2020+ change-of-ownership loan was {m(b['own_median'])}, the highest of our deep dives (veterinary clinics are close behind), vs {m(A20['own']['median'])} across all industries. Buyouts were {b['own_share']:.1%} of this industry's FY2020+ 7(a) loans.</li>
<li>Older acquisition data is thin: only {c(a['own_n'])} FY2010-2019 roofing loans carry the "Change of Ownership" label, so don't lean on that column.</li>
<li>Franchising is new here: {b['franchise_share']:.1%} of FY2020+ roofing 7(a) loans went to franchise locations, up from {a['franchise_share']:.1%} in FY2010-2019.</li>
<li>Utah roofers were a bit bigger on average ({ut['emp_per_est']:.1f} employees vs {us['emp_per_est']:.1f} nationally), with lower payroll per employee ({m(ut['pay_per_emp'])} vs {m(us['pay_per_emp'])}).</li>
<li>Inference (ours): roofing revenue can swing with weather and storm seasons, which may help explain the higher loss rates. Ask a seller for several years of monthly revenue, not just annual totals. The loan data doesn't show this directly.</li>""")
  if code=="624410": return (
   f"Child care centers are one of the most SBA-financed service businesses. Here's what {c(a['n']+b['n'])} SBA 7(a) loans since FY2010, plus {c(d['504_fy10_19']['n']+d['504_fy20p']['n'])} 504 loans and Census counts, show about financing and buying one.",
   f"""<li>Child care loans held up well: {p(a['co_rate'])} charged off by count in FY2010-2019 vs {p(A10['co_rate'])} for all 7(a) loans, and only {p(a['co_dollar'])} of dollars vs {p(A10['co_dollar'])}.</li>
<li>Buying an existing center is common: {b['own_share']:.1%} of FY2020+ child care 7(a) loans were change-of-ownership loans, above the all-industry share ({A20own:.1%}). The median acquisition loan was {m(b['own_median'])}.</li>
<li>Startups are a big group too ({c(b['ages'].get('Startup, Loan Funds will Open Business',0))} FY2020+ loans flagged "Startup"), and franchise locations got {b['franchise_share']:.0%} of FY2020+ loans.</li>
<li>Real estate shows up often (our inference from the loan types): SBA 504 loans, which usually finance a building, numbered {c(d['504_fy20p']['n'])} since FY2020 with a median CDC portion of {m(d['504_fy20p']['median'])}, and the median FY2010-2019 7(a) acquisition loan had a {a['own_term']:.0f}-month term.</li>
<li>Payroll per employee was about {m(us['pay_per_emp'])} in the U.S. and {m(ut['pay_per_emp'])} in Utah (2023). Census mixes full- and part-time staff, so don't read that as a wage rate. Inference (ours): with staffing ratios set by state licensing rules, labor cost and staff turnover deserve close diligence.</li>""")
  if code=="713940": return (
   f"Gyms and fitness centers are mostly financed as new openings, and a large share are franchises. Here's what {c(a['n']+b['n'])} SBA 7(a) loans since FY2010, plus 504 and Census data, show about financing and buying one.",
   f"""<li>Fitness loans charged off at {p(a['co_rate'])} by count in FY2010-2019, the highest of our deep dives (about tied with roofing) and well above all 7(a) loans ({p(A10['co_rate'])}). By dollars, {p(a['co_dollar'])} were charged off vs {p(A10['co_dollar'])} overall.</li>
<li>Startups dominate: {c(b['ages'].get('Startup, Loan Funds will Open Business',0))} of {c(b['n'])} FY2020+ fitness 7(a) loans were flagged "Startup", and {b['franchise_share']:.0%} went to franchise locations, among the highest franchise shares of our deep dives (only hotels and gas stations, where fuel-supply agreements count as franchises, are higher).</li>
<li>Buying an existing gym is less common: change-of-ownership loans were {b['own_share']:.1%} of FY2020+ loans (all industries: {A20own:.1%}), with a median acquisition loan of {m(b['own_median'])}, well below the all-industry median of {m(A20['own']['median'])}.</li>
<li>Payroll per employee was the lowest of our deep dives: about {m(us['pay_per_emp'])} in the U.S. and {m(ut['pay_per_emp'])} in Utah (2023). Inference (ours): part-time trainers and front-desk staff likely pull this down; it isn't a wage rate.</li>
<li>Utah gyms were bigger on average ({ut['emp_per_est']:.1f} employees vs {us['emp_per_est']:.1f} nationally). Inference (ours): with membership revenue, check member counts, churn and how much revenue is prepaid before you buy.</li>""")
  if code=="531130": return (
   f"Self-storage is a real-estate-heavy business with very few employees. Here's what {c(a['n']+b['n'])} SBA 7(a) loans and {c(e['n']+f['n'])} SBA 504 loans since FY2010, plus Census counts, show about financing and buying a facility (NAICS 531130, lessors of miniwarehouses and self-storage units).",
   f"""<li>Self-storage loans had the lowest loss record of all our deep dives: {p(a['co_rate'])} charged off by count in FY2010-2019 vs {p(A10['co_rate'])} for all 7(a) loans, and just {a['co_dollar']:.2%} of approved dollars.</li>
<li>Many loans fund new construction: {c(b['ages'].get('Startup, Loan Funds will Open Business',0))} of {c(b['n'])} FY2020+ 7(a) loans and {c(f['ages'].get('Startup, Loan Funds will Open Business',0))} of {c(f['n'])} FY2020+ 504 loans were flagged "Startup".</li>
<li>Buyouts were {b['own_share']:.1%} of FY2020+ 7(a) loans (all industries: {A20own:.1%}), with a median acquisition loan of {m(b['own_median'])} and a median {b['own_term']:.0f}-month term. Inference (ours): a 25-year term is consistent with the loan mostly financing land and buildings; the data doesn't break out what each loan paid for.</li>
<li>Franchising is uncommon ({b['franchise_share']:.1%} of FY2020+ 7(a) loans), and most of those franchise loans were portable-storage brands (UNITS, MI-BOX, Go Mini's) by SBA's FranchiseName field, not storage-facility brands.</li>
<li>Staffing is minimal: {us['emp_per_est']:.1f} employees per establishment on average in the U.S. ({ut['emp_per_est']:.1f} in Utah), and {us['share_under10']:.0%} had fewer than 10 employees. Census counts only establishments with paid employees, so unstaffed or owner-run facilities aren't in these numbers. Inference (ours): with labor this light, value rests mostly on occupancy, rental rates and the real estate itself.</li>
<li>Utah: {c(ut['est'])} establishments with employees (2023); {c(a['ut_n']+b['ut_n'])} 7(a) and {c(e['ut_n']+f['ut_n'])} 504 loans since FY2010.</li>""")
  if code=="721110": return (
   f"Hotels and motels are one of the biggest uses of SBA lending, and the loans are large. Here's what {c(a['n']+b['n'])} SBA 7(a) loans and {c(e['n']+f['n'])} SBA 504 loans since FY2010, plus Census counts, show about financing and buying one.",
   f"""<li>These are the largest loans in our deep dives: the median FY2020+ 7(a) loan was {m(b['median'])}, and the median change-of-ownership loan was {m(b['own_median'])} (all industries: {m(A20['own']['median'])}).</li>
<li>Buying an existing property is common: change-of-ownership loans were {b['own_share']:.1%} of FY2020+ hotel 7(a) loans vs {A20own:.1%} across all industries.</li>
<li>Most financed hotels carry a brand: {b['franchise_share']:.0%} of FY2020+ 7(a) loans had a franchise code, the highest share of our deep dives. The most common brands in SBA's FranchiseName field were Quality Inn, Super 8, Days Inn, Motel 6 and Best Western.</li>
<li>Losses: {p(a['co_rate'])} of FY2010-2019 7(a) hotel loans were charged off by count ({p(a['co_dollar'])} of dollars) vs {p(A10['co_rate'])} ({p(A10['co_dollar'])}) for all 7(a) loans. FY2010-2019 504 hotel loans charged off at {p(e['co_rate'])} vs {p(D['ALL504']['504_fy10_19']['co_rate'])} for all 504 loans.</li>
<li>Hotels are staffing-heavy: {us['emp_per_est']:.1f} employees per establishment in the U.S. and {ut['emp_per_est']:.1f} in Utah (2023), with payroll per employee of about {m(us['pay_per_emp'])} nationally and {m(ut['pay_per_emp'])} in Utah. Census mixes full- and part-time staff, so that isn't a wage rate.</li>
<li>Utah: {c(ut['est'])} establishments with employees; {c(b['ut_n'])} 7(a) loans since FY2020 (median {dm(b['ut_median'])}). Inference (ours): at these loan sizes, a buyer with a budget under about $1 million is mostly looking at small independent or economy-brand motels; check the brand's property-improvement requirements before pricing a deal.</li>""")
  if code=="447110": return (
   f"Gas stations with convenience stores are a common SBA acquisition. Here's what {c(a['n']+b['n'])} SBA 7(a) loans and {c(e['n']+f['n'])} SBA 504 loans since FY2010, plus Census counts, show. SBA files use both the 2017 code (447110) and the 2022 code (457110); we combined them.",
   f"""<li>Losses were below average: {p(a['co_rate'])} of FY2010-2019 7(a) loans were charged off by count vs {p(A10['co_rate'])} for all 7(a) loans, and {p(a['co_dollar'])} of dollars vs {p(A10['co_dollar'])}. FY2010-2019 504 loans charged off at {p(e['co_rate'])} vs {p(D['ALL504']['504_fy10_19']['co_rate'])} for all 504 loans.</li>
<li>Buyouts are a big share of the business: change-of-ownership loans were {b['own_share']:.1%} of FY2020+ 7(a) loans (all industries: {A20own:.1%}), with a median acquisition loan of {m(b['own_median'])} over a median {b['own_term']:.0f} months.</li>
<li>About half of FY2020+ loans ({b['franchise_share']:.0%}, up from {a['franchise_share']:.0%} in FY2010-2019) carried a franchise code, but the top "franchises" in SBA's FranchiseName field are fuel-supply and branded-reseller agreements (Chevron, Sunoco, ARCO/ampm, Phillips 66), not classic franchises.</li>
<li>The median FY2020+ initial rate was {b['rate']:.2f}%, and only {b['fixed_share']:.0%} of loans were fixed-rate.</li>
<li>Payroll per employee was about {m(us['pay_per_emp'])} in the U.S. and {m(ut['pay_per_emp'])} in Utah (2023), the second lowest of our deep dives after fitness centers. Utah stations were bigger on average ({ut['emp_per_est']:.1f} employees vs {us['emp_per_est']:.1f} nationally) and fewer were under 10 employees ({ut['share_under10']:.0%} vs {us['share_under10']:.0%}). Census payroll mixes full- and part-time staff.</li>
<li>Inference (ours): the fuel-supply contract's term, pricing and any brand-imaging obligations, plus the environmental condition of the underground tanks, can matter as much as store sales; ask for them early.</li>""")
  return (
   f"Veterinary clinics are bigger than most small businesses (about {us['emp_per_est']:.0f} employees per location on average) and borrow more. Here's what SBA 7(a) and 504 data and Census counts show for veterinary services.",
   f"""<li>Vet loans had one of the lowest loss records of our industry deep dives (only self-storage was lower): {p(a['co_rate'])} charged off by count in FY2010-2019 vs {p(A10['co_rate'])} for all 7(a) loans.</li>
<li>They're large and long. The FY2010-2019 median term was {a['term']:.0f} months vs {A10['term']:.0f} for all 7(a). Inference (ours): terms that long are consistent with real estate being part of many of these loans; the data doesn't say what each loan financed.</li>
<li>The median FY2020+ change-of-ownership loan was {m(b['own_median'])}, and buyouts were {b['own_share']:.1%} of this industry's 7(a) loans.</li>
<li>Only {us['share_under10']:.0%} of U.S. vet clinics with employees had fewer than 10 people, and {c(us['n20plus'])} had 20 or more, so this is a staffing-heavy business compared to auto repair or dental.</li>
<li>Utah counts are small ({c(ut['est'])} establishments; {c(b['ut_n'])} 7(a) loans since FY2020). Census flags the Utah employment number as having moderate noise (flag H, 2-5%).</li>""")
for code,fn,name,one in DDS:
  intro,notes=dd(code)
  page(fn,f"Buying {('an ' if one[0] in 'aeiou' else 'a ')+one}: SBA loan data and industry numbers",
   f"{name} (NAICS {code}): SBA 7(a) and 504 loan counts, sizes, acquisition loans, and charge-off rates, plus Census establishment counts for the U.S. and Utah.",
   dd_body(code,name,one,intro,notes),SRC_DD,VDATE.get(code,V2))

page("index.html","Data-driven guides for buying a small business","Independent, data-first guides for small-business buyers: industry outcomes, sale multiples, and how deals get financed.",
 f"""<h1>Buying a small business? Start with the data.</h1>
<p>Plain, sourced numbers for buyers: which industries hold up, what businesses sell for, and how deals actually get financed. Every number links to its public source.</p>
<ul><li><a href="evaluate-a-business-checklist.html">How to evaluate a small business for sale (checklist)</a></li>
<li><a href="sba-loan-chargeoff-rates-by-industry.html">SBA loan charge-off rates by industry</a>: laundromats {p(r10['812310']['co_rate'])}, car washes {p(r10['811192']['co_rate'])}, all loans {p(r10['ALL']['co_rate'])} (FY2010-2019)</li>
<li><a href="sba-acquisition-loans.html">SBA loans used to buy a business</a>: {c(r20['ALL']['own']['n'])} since FY2020, median {m(r20['ALL']['own']['median'])}</li>
<li><a href="sba-loan-size-and-terms-by-industry.html">Loan sizes, terms and rates by industry</a></li>
<li><a href="what-small-businesses-sell-for.html">What small businesses sell for (Q3 2026)</a></li></ul>
<h2>Industry deep dives</h2><ul>"""+"".join(f'<li><a href="{fn}">{nm}</a>: median FY2020+ acquisition loan {m(D[cd]["7a_fy20p"]["own_median"])}, FY2010-2019 charge-off rate {p(D[cd]["7a_fy10_19"]["co_rate"])}</li>' for cd,fn,nm,_ in DDS)+"""</ul>""",
 [("SBA 7(a) FOIA data",FOIA),("BizBuySell Insight Report",BBS),("Census County Business Patterns 2023",CBP)])

page("disclaimer.html","Disclaimer","Disclaimer","""<h1>Disclaimer</h1><p>Small Business Buyer Guide is an independent informational site. It is not affiliated with or endorsed by the U.S. Small Business Administration, any lender, broker, or marketplace.</p>
<p>Nothing here is financial, investment, legal, or tax advice. Historical loan statistics describe past loans and don't predict any individual business or deal. Do your own due diligence and consult qualified professionals.</p>
<p>We compute figures from public data and publish our method and code. If you find an error, the original source wins.</p>""")
page("affiliate-disclosure.html","Affiliate disclosure","Affiliate disclosure","""<h1>Affiliate disclosure</h1><p>Some pages may link to lenders, marketplaces, or services. If you use some of those links, we may earn a commission or referral fee at no extra cost to you. Such links will be labeled.</p>
<p>Compensation doesn't change our data. Every figure comes from a cited public source.</p><p class="meta">As of October 21, 2026, this site has no active affiliate relationships.</p>""")
print("built")
