#!/usr/bin/env python3
"""Cross-industry pages (content-plan items 13-15): SBA 7(a) + 504 FOIA files (as of 2026-06-30).
Run from the folder holding the FOIA CSVs. Writes cross-industry.json (or path in argv[1])."""
import csv,json,statistics as st,collections as C,sys
ALIAS={"457110":"447110"}
med=lambda a:st.median(a) if a else None
def stats(R):
  n=len(R)
  if not n: return {"n":0}
  ga=sum(x["amt"] for x in R); own=[x for x in R if "Change of Ownership" in x["age"]]
  d={"n":n,"median":med([x["amt"] for x in R]),"total":ga,
     "co_n":sum(x["s"]=="CHGOFF" for x in R),"co_rate":sum(x["s"]=="CHGOFF" for x in R)/n,
     "co_dollar":sum(x["co"] for x in R)/ga if ga else None,
     "pif_rate":sum(x["s"]=="PIF" for x in R)/n,"exempt_rate":sum(x["s"]=="EXEMPT" for x in R)/n,
     "term":med([x["term"] for x in R if x["term"]]),
     "own_n":len(own),"own_share":len(own)/n,"own_median":med([x["amt"] for x in own]),
     "own_co_rate":(sum(x["s"]=="CHGOFF" for x in own)/len(own)) if own else None}
  if "proj" in R[0]:
    d["proj_median"]=med([x["proj"] for x in R]); d["jobs_median"]=med([x["jobs"] for x in R if x["jobs"]>0])
    d["tp_share"]=sum(x["tp"]>0 for x in R)/n
  return d
def load(fn,prog):
  rows=[]; desc=C.defaultdict(C.Counter)
  for r in csv.DictReader(open(fn,newline='',encoding='latin-1')):
    s=r["LoanStatus"].strip().replace(" ","")
    if s in("CANCLD","COMMIT","NOTFUNDED"): continue
    c=r["NaicsCode"].strip(); c=ALIAS.get(c,c); desc[c][r["NaicsDescription"].strip()]+=1
    x={"s":s,"naics":c,"amt":float(r["GrossApproval"] or 0),"co":float(r["GrossChargeOffAmount"] or 0),"age":r["BusinessAge"].strip(),
       "term":float(r["TermInMonths"] or 0),"fr":r["FranchiseCode"].strip()!="","fy":int(r["ApprovalFY"])}
    if prog=="504":
      x["tp"]=float(r["ThirdPartyDollars"] or 0); x["proj"]=x["amt"]+x["tp"]; x["jobs"]=float(r["JobsSupported"] or 0)
    rows.append(x)
  return rows,desc
def by_naics(R,desc,top):
  g=C.defaultdict(list)
  for x in R: g[x["naics"]].append(x)
  blank=len(g.pop("",[]))
  ks=sorted(g,key=lambda k:-len(g[k]))[:top]
  return [dict(naics=k,desc=desc[k].most_common(1)[0][0],**stats(g[k])) for k in ks],blank
out={}
A,dA=load("FOIA_7a_FY2010_FY2019_asof_260630.csv","7a"); B,dB=load("FOIA_7a_FY2020_Present_asof_260630.csv","7a")
# 13: leaderboard
lb,blank=by_naics(A,dA,50); out["leaderboard"]={"rows":lb,"blank_naics":blank,"all":stats(A)}
# 14: franchise vs non-franchise
fr={}
for key,R in (("fy10_19",A),("fy20p",B)):
  fr[key]={"fr":stats([x for x in R if x["fr"]]),"non":stats([x for x in R if not x["fr"]])}
  own=[x for x in R if "Change of Ownership" in x["age"]]
  fr[key]["own_fr"]=stats([x for x in own if x["fr"]]); fr[key]["own_non"]=stats([x for x in own if not x["fr"]])
g=C.defaultdict(list)
for x in A: g[x["naics"]].append(x)
ind=[]
for k,R in g.items():
  F=[x for x in R if x["fr"]]; N=[x for x in R if not x["fr"]]
  if k and len(F)>=300 and len(N)>=300:
    ind.append({"naics":k,"desc":dA[k].most_common(1)[0][0],"fr":stats(F),"non":stats(N),"fr_share":len(F)/len(R)})
ind.sort(key=lambda d:-d["fr"]["n"]); fr["by_industry_fy10_19"]=ind
out["franchise"]=fr
# 15: 504 by industry
P,dP=load("FOIA_504_FY2010_Present_asof_260630.csv","504")
P1=[x for x in P if x["fy"]<=2019]; P2=[x for x in P if x["fy"]>=2020]
r1,b1=by_naics(P1,dP,25); r2,b2=by_naics(P2,dP,25)
# 7(a) FY10-19 charge-off for the same NAICS, for comparison
for d in r1:
  s7=stats(g[d["naics"]]) if g.get(d["naics"]) else {"n":0}
  d["7a_n"]=s7["n"]; d["7a_co_rate"]=s7.get("co_rate")
out["504"]={"fy10_19":{"rows":r1,"blank":b1,"all":stats(P1)},"fy20p":{"rows":r2,"blank":b2,"all":stats(P2)},
  "by_fy":{fy:stats([x for x in P if x["fy"]==fy]) for fy in sorted({x["fy"] for x in P})}}
json.dump(out,open(sys.argv[1] if len(sys.argv)>1 else "cross-industry.json","w"),indent=1)
print("ok",len(A),len(B),len(P))
