import csv,statistics as st,json,collections as C
codes=["ALL","238220","811192","812310","561730","722513"]
out={}
for fn,key in [("FOIA_7a_FY2010_FY2019_asof_260630.csv","fy10_19"),("FOIA_7a_FY2020_Present_asof_260630.csv","fy20p")]:
  g={k:{"desc":"","rows":[]} for k in codes}
  for r in csv.DictReader(open(fn,newline='',encoding='latin-1')):
    c=r["NaicsCode"].strip()
    s=r["LoanStatus"].strip()
    if s in("CANCLD","COMMIT"): continue
    rec=(s,float(r["GrossApproval"] or 0),float(r["GrossChargeOffAmount"] or 0),r["BusinessAge"].strip(),r["TermInMonths"],r["InitialInterestRate"],r["FixedorVariableInterestInd"].strip())
    g["ALL"]["rows"].append(rec)
    if c in g: g[c]["rows"].append(rec); g[c]["desc"]=r["NaicsDescription"].strip()
  res={}
  for k,d in g.items():
    R=d["rows"];n=len(R)
    def stats(R):
      n=len(R);co=sum(1 for x in R if x[0]=="CHGOFF");ga=sum(x[1] for x in R)
      return {"n":n,"co_rate":co/n if n else None,"co_dollar":sum(x[2] for x in R)/ga if ga else None,"median":st.median([x[1] for x in R]) if R else None}
    own=[x for x in R if "Change of Ownership" in x[3]]
    res[k]={"desc":d["desc"],**stats(R),"own":stats(own),"ages":dict(C.Counter(x[3] for x in R).most_common()),
      "term":st.median([float(x[4]) for x in R if x[4]]),"rate":st.median([float(x[5]) for x in R if x[5]]),
      "fixed_share":sum(1 for x in R if x[6]=="F")/n}
  out[key]=res
json.dump(out,open("summary.json","w"),indent=1)
for key in out:
  print(key)
  for k,v in out[key].items(): print(" ",k,v["desc"],v["n"],round(v["median"]),f'{v["co_rate"]:.1%} {v["co_dollar"]:.1%}',"own:",v["own"]["n"],v["own"]["co_rate"] and f'{v["own"]["co_rate"]:.1%}',v["own"]["median"],v["term"],v["rate"],f'{v["fixed_share"]:.0%}',list(v["ages"].items())[:6])
