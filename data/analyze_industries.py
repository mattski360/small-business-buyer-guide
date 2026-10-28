#!/usr/bin/env python3
"""Industry deep dives: SBA 7(a) + 504 FOIA (as of 2026-06-30) and Census CBP 2023.
Run from a folder with the FOIA CSVs and cbp/cbp23us.txt, cbp/cbp23st.txt. Writes industry-deep-dives.json."""
import csv,json,statistics as st,collections as C,sys
CODES=["811111","621210","541940"]
med=lambda a:st.median(a) if a else None
def s7(R):
  n=len(R)
  if not n: return {"n":0}
  ga=sum(x["amt"] for x in R)
  own=[x for x in R if "Change of Ownership" in x["age"]]
  return {"n":n,"median":med([x["amt"] for x in R]),"total":ga,
    "co_rate":sum(x["s"]=="CHGOFF" for x in R)/n,"co_dollar":sum(x["co"] for x in R)/ga if ga else None,
    "pif_rate":sum(x["s"]=="PIF" for x in R)/n,
    "term":med([x["term"] for x in R if x["term"]]),"rate":med([x["rate"] for x in R if x.get("rate")]),
    "fixed_share":sum(x.get("fv")=="F" for x in R)/n,
    "franchise_share":sum(bool(x["fr"]) for x in R)/n,
    "own_n":len(own),"own_share":len(own)/n,"own_median":med([x["amt"] for x in own]),
    "own_co_rate":(sum(x["s"]=="CHGOFF" for x in own)/len(own)) if own else None,
    "own_term":med([x["term"] for x in own if x["term"]]),
    "ut_n":sum(x["st"]=="UT" for x in R),"ut_median":med([x["amt"] for x in R if x["st"]=="UT"]),
    "ages":dict(C.Counter(x["age"] for x in R).most_common(8))}
def load(fn,prog):
  out=C.defaultdict(list)
  for r in csv.DictReader(open(fn,newline='',encoding='latin-1')):
    c=r["NaicsCode"].strip(); s=r["LoanStatus"].strip().replace(" ","")
    if s in("CANCLD","COMMIT","NOTFUNDED"): continue
    if c not in CODES and prog=="7a": continue
    x={"s":s,"amt":float(r["GrossApproval"] or 0),"co":float(r["GrossChargeOffAmount"] or 0),"age":r["BusinessAge"].strip(),
       "term":float(r["TermInMonths"] or 0),"fr":r["FranchiseCode"].strip()!="","st":r["ProjectState"].strip(),"fy":int(r["ApprovalFY"])}
    if prog=="7a": x["rate"]=float(r["InitialInterestRate"] or 0); x["fv"]=r["FixedorVariableInterestInd"].strip()
    out[c].append(x)
    if prog=="504": out["ALL"].append(x)
  return out
res={c:{} for c in CODES}
for fn,key in [("FOIA_7a_FY2010_FY2019_asof_260630.csv","7a_fy10_19"),("FOIA_7a_FY2020_Present_asof_260630.csv","7a_fy20p")]:
  L=load(fn,"7a")
  for c in CODES: res[c][key]=s7(L[c])
L=load("FOIA_504_FY2010_Present_asof_260630.csv","504")
res["ALL504"]={"504_fy10_19":s7([x for x in L["ALL"] if x["fy"]<=2019]),"504_fy20p":s7([x for x in L["ALL"] if x["fy"]>=2020])}
for c in CODES:
  res[c]["504_fy10_19"]=s7([x for x in L[c] if x["fy"]<=2019]); res[c]["504_fy20p"]=s7([x for x in L[c] if x["fy"]>=2020])
def cbp(fn,geo):
  for r in csv.DictReader(open(fn)):
    if r["naics"] in CODES and r["lfo"]=="-" and (r.get("fipstate")==geo or r.get("uscode")==geo):
      est=int(r["est"]); sm=sum(int(r[k]) for k in ("n<5","n5_9"))
      yield r["naics"],{"est":est,"emp":int(r["emp"]),"emp_flag":r["emp_nf"],"payroll_k":int(r["ap"]),
        "pay_per_emp":int(r["ap"])*1000/int(r["emp"]) if int(r["emp"]) else None,"emp_per_est":int(r["emp"])/est,"share_under10":sm/est,
        "share_under5":int(r["n<5"])/est,"n20plus":est-sm-int(r["n10_19"])}
for c,v in cbp("cbp/cbp23us.txt","98"): res[c]["cbp_us"]=v
for c,v in cbp("cbp/cbp23st.txt","49"): res[c]["cbp_ut"]=v
json.dump(res,open(sys.argv[1] if len(sys.argv)>1 else "industry-deep-dives.json","w"),indent=1)
for c in res:
  print(c)
  for k,v in res[c].items(): print(" ",k,{a:(round(b,4) if isinstance(b,float) else b) for a,b in v.items()})
