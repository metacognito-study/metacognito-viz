#!/usr/bin/env python3
"""Deterministic AP-Econ SVG factory (lean priority set). House style: 480x320, white bg,
#333 axes, demand #1d4ed8, supply #b91c1c, shifts dashed + #0f766e arrows. Variants:
labeled (inline example image) / plain (pad underlay, no answer-revealing marks)."""
import os, xml.etree.ElementTree as ET

W,H=480,320; X0,Y0,X1,Y1=60,280,440,40   # axes frame: origin bottom-left
def head(): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="#ffffff"/>'
def axes(xl="Q",yl="P"):
    s=f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1}" stroke="#333" stroke-width="2"/><line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="#333" stroke-width="2"/>'
    s+=f'<text x="{(X0+X1)//2}" y="306" font-family="sans-serif" font-size="13" fill="#555" text-anchor="middle">{xl}</text>'
    s+=f'<text x="24" y="{(Y0+Y1)//2}" font-family="sans-serif" font-size="13" fill="#555" text-anchor="middle" transform="rotate(-90 24 {(Y0+Y1)//2})">{yl}</text>'
    return s
def txt(x,y,t,size=14,fill="#333",anchor="middle",bold=False):
    t=str(t).replace("&","&amp;").replace("<","&lt;")
    w=' font-weight="700"' if bold else ''
    return f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" fill="{fill}" text-anchor="{anchor}"{w}>{t}</text>'
def ln(x1,y1,x2,y2,stroke,w=2.5,dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{w}"{d}/>'
def guide(x,y): return ln(X0,y,x,y,"#999",1,"4 4")+ln(x,y,x,Y0,"#999",1,"4 4")
def dot(x,y): return f'<circle cx="{x}" cy="{y}" r="4" fill="#333"/>'
def arrow(x1,y1,x2,y2,color="#0f766e"):
    return f'<defs><marker id="ah{abs(x1+y2)}" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{color}"/></marker></defs>'+f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2" marker-end="url(#ah{abs(x1+y2)})"/>'
D=(80,80,400,260); S=(80,260,400,80)   # demand: high-left->low-right (x1,y1,x2,y2 screen coords)
def demand(off=0,dash=None,color="#1d4ed8"): return ln(D[0]+off,D[1],D[2]+off,D[3],color,2.5,dash)
def supply(off=0,dash=None,color="#b91c1c"): return ln(S[0]+off,S[1],S[2]+off,S[3],color,2.5,dash)
def eq(off_d=0,off_s=0):
    x=(240+(off_d+off_s)/2); y=170+(off_s-off_d)/2   # LEGACY approximation; superseded by the QP model below
    return x,y
# ── Economic-coordinate model (07-19 fix, Ibrahim feedback): Q,P in [0,100]; SUPPLY PASSES THROUGH
# THE ORIGIN (60,280); every equilibrium dot is the EXACT algebraic line intersection, no guess. ──
QX0,QX1,PY0,PY1 = 60,430,280,54            # screen anchors: (Q=0,P=0) == axis origin corner
def sx(Q): return round(QX0+(QX1-QX0)*Q/100.0,1)
def sy(P): return round(PY0+(PY1-PY0)*P/100.0,1)
def lnQP(Q1,P1,Q2,P2,color,w=2.5,dash=None): return ln(sx(Q1),sy(P1),sx(Q2),sy(P2),color,w,dash)
def dotQP(Q,P): return dot(sx(Q),sy(P))
def guideQP(Q,P): return ln(QX0,sy(P),sx(Q),sy(P),"#999",1,"4 4")+ln(sx(Q),sy(P),sx(Q),PY0,"#999",1,"4 4")
def txtQP(Q,P,t,size=13,fill="#333",anchor="middle",bold=False): return txt(sx(Q),sy(P),t,size,fill,anchor,bold)
BOX=(0,97,0,98)                            # visible clip window (Qmin,Qmax,Pmin,Pmax)
def _demandQP(a,dash=None,color="#1d4ed8"):   # P = a - Q  (a=100+shift). Downward.
    qlo=max(BOX[0],a-BOX[3]); qhi=min(BOX[1],a-BOX[2]); return lnQP(qlo,a-qlo,qhi,a-qhi,color,2.5,dash)
def _supplyQP(b,dash=None,color="#b91c1c"):   # P = Q - b  (b=shift; b=0 => through origin). Upward.
    qlo=max(BOX[0],BOX[2]+b); qhi=min(BOX[1],BOX[3]+b); return lnQP(qlo,qlo-b,qhi,qhi-b,color,2.5,dash)
def eqQP(dsh=0,ssh=0):                      # D:P=100+dsh-Q  S:P=Q-ssh  -> exact intersection
    Q=(100+dsh+ssh)/2.0; return Q, Q-ssh
def demand_top(a): qlo=max(BOX[0],a-BOX[3]); return qlo, a-qlo   # top (high-P) end of a demand curve
def supply_top(b): qhi=min(BOX[1],BOX[3]+b); return qhi, qhi-b   # top end of a supply curve
def clabel(kind,ab,name,color):            # place a curve label just past its top endpoint
    if kind=='D': Q,P=demand_top(ab); return txt(sx(Q)+14,sy(P)+3,name,13,color,"start")
    Q,P=supply_top(ab); return txt(sx(Q)-14,sy(P)+3,name,13,color,"end")
def grid():
    s=''
    for gx in range(X0+38,X1,38): s+=ln(gx,Y1,gx,Y0,"#e2e8f0",1)
    for gy in range(Y1+30,Y0,30): s+=ln(X0,gy,X1,gy,"#e2e8f0",1)
    return s
def tail(): return '</svg>'
OUT={}
def emit(name,body): OUT[name]=head()+body+tail()

# F1 supply-demand core (supply through origin; exact equilibrium dot)
def sd_base(): return axes()+_demandQP(100)+_supplyQP(0)
Qe,Pe=eqQP()
emit("u_econ_sd_equilibrium__plain.svg", sd_base())
emit("u_econ_sd_equilibrium__labeled.svg", sd_base()+dotQP(Qe,Pe)+guideQP(Qe,Pe)
     +clabel('D',100,"D","#1d4ed8")+clabel('S',0,"S","#b91c1c")
     +txt(52,sy(Pe)+4,"Pe",12,"#333","end")+txt(sx(Qe)+15,294,"Qe",12,"#333","start"))
# numeric gridded S&D: read exact values off the grid ($=P/5, Q 1:1); eq (50,50) -> $10, 50 units
def num_grid():
    s=''
    for Q in (25,50,75): s+=ln(sx(Q),PY1,sx(Q),PY0,"#e2e8f0",1)
    for P in (25,50,75): s+=ln(QX0,sy(P),QX1,sy(P),"#e2e8f0",1)
    return s
gp=axes()+num_grid()+_demandQP(100)+_supplyQP(0)
emit("u_econ_sd_numeric_grid__plain.svg", gp)
labg=gp+dotQP(50,50)+guideQP(50,50)
for P,t in ((25,"$5"),(50,"$10"),(75,"$15")): labg+=txt(52,sy(P)+4,t,11,"#333","end")
for Q,t in ((25,"25"),(50,"50"),(75,"75")): labg+=txt(sx(Q),296,t,11)
emit("u_econ_sd_numeric_grid__labeled.svg", labg+clabel('D',100,"D","#1d4ed8")+clabel('S',0,"S","#b91c1c"))
# shifts: EXACT new-eq dot at the true intersection; dashed shifted curve + direction arrow
for slug,dsh,ssh in [("demand_shift_right",15,0),("demand_shift_left",-15,0),("supply_shift_right",0,15),("supply_shift_left",0,-15)]:
    base=sd_base()
    if dsh: shifted=_demandQP(100+dsh,"7 5"); c="#1d4ed8"; names=("D1","D2"); labs=clabel('D',100,"D1",c)+clabel('D',100+dsh,"D2",c)
    else:   shifted=_supplyQP(ssh,"7 5");     c="#b91c1c"; names=("S1","S2"); labs=clabel('S',0,"S1",c)+clabel('S',ssh,"S2",c)
    Q1,P1=eqQP(); Q2,P2=eqQP(dsh,ssh)
    Pa=75 if dsh else 25                       # arrow band: upper for D, lower for S
    qb=(100-Pa) if dsh else Pa                 # base-curve Q at Pa
    qs=(100+dsh-Pa) if dsh else (Pa+ssh)       # shifted-curve Q at Pa
    d=1 if (dsh>0 or ssh>0) else -1
    ar=arrow(sx(qb)+d*4,sy(Pa),sx(qs)-d*4,sy(Pa))
    emit(f"u_econ_{slug}__plain.svg", base)     # plain = original curves only; student draws the shift + new eq
    emit(f"u_econ_{slug}__labeled.svg", base+shifted+ar+dotQP(Q1,P1)+dotQP(Q2,P2)+guideQP(Q2,P2)+labs)
# F4 payoff matrix
def payoff(blank=False):
    ox,oy,cw,ch=150,90,120,70
    s=txt(240,40,"Firm B",14,bold=True)+txt(70,60,"",1)
    s+=txt(ox+cw//2,oy-8,"Low price",12)+txt(ox+cw+cw//2,oy-8,"High price",12)
    s+=f'<text x="52" y="{oy+ch//2}" font-family="sans-serif" font-size="14" font-weight="700" fill="#333" text-anchor="middle" transform="rotate(-90 52 {oy+ch//2+35})">Firm A</text>'
    s+=txt(ox-45,oy+ch//2+4,"Low",12)+txt(ox-45,oy+ch+ch//2+4,"High",12)
    for r in range(2):
        for c in range(2):
            s+=f'<rect x="{ox+c*cw}" y="{oy+r*ch}" width="{cw}" height="{ch}" fill="none" stroke="#333" stroke-width="1.5"/>'
    vals=[("$40, $40","$70, $20"),("$20, $70","$55, $55")]
    if not blank:
        for r in range(2):
            for c in range(2): s+=txt(ox+c*cw+cw//2,oy+r*ch+ch//2+5,vals[r][c],13)
    else:
        for r in range(2):
            for c in range(2): s+=f'<rect x="{ox+c*cw+30}" y="{oy+r*ch+22}" width="60" height="26" fill="none" stroke="#94a3b8" stroke-dasharray="5 4"/>'
    return s
emit("u_econ_payoff_matrix_2x2__labeled.svg", payoff(False))
emit("u_econ_payoff_matrix_2x2__plain.svg", payoff(True))
# F6 PPC bowed + linear
ppc=f'<path d="M {X0} {Y1+30} Q {X0+240} {Y1+60} {X1-20} {Y0}" fill="none" stroke="#0f766e" stroke-width="2.5"/>'
emit("u_econ_ppc_bowed__plain.svg", axes("Good X","Good Y")+ppc)
emit("u_econ_ppc_bowed__labeled.svg", axes("Good X","Good Y")+ppc+dot(250,108)+txt(262,100,"A",13)+dot(360,190)+txt(372,182,"B",13)+dot(180,200)+txt(180,218,"C (inefficient)",12)+dot(390,90)+txt(392,78,"D (unattainable)",12))
emit("u_econ_ppc_linear__plain.svg", axes("Good X","Good Y")+ln(X0,Y1+30,X1-20,Y0,"#0f766e",2.5))
# F8 circular flow 2-sector
def cflow(labeled):
    s=f'<rect x="60" y="130" width="110" height="56" rx="10" fill="#eef2ff" stroke="#333" stroke-width="1.5"/>'+txt(115,162,"Households",13,bold=True)
    s+=f'<rect x="310" y="130" width="110" height="56" rx="10" fill="#fef2f2" stroke="#333" stroke-width="1.5"/>'+txt(365,162,"Firms",13,bold=True)
    s+=f'<ellipse cx="240" cy="70" rx="95" ry="26" fill="#f0fdf4" stroke="#333" stroke-width="1.5"/>'+txt(240,75,"Product market",12,bold=True)
    s+=f'<ellipse cx="240" cy="250" rx="95" ry="26" fill="#fffbeb" stroke="#333" stroke-width="1.5"/>'+txt(240,255,"Factor market",12,bold=True)
    s+=arrow(150,120,190,88)+arrow(290,88,330,120)+arrow(330,196,290,232)+arrow(190,232,150,196)
    if labeled:
        s+=txt(118,95,"$ consumer spending",11,"#0f766e")+txt(372,95,"$ revenue",11,"#0f766e")
        s+=txt(382,225,"$ factor payments",11,"#0f766e")+txt(108,225,"$ wages, rent, profit",11,"#0f766e")
    return s
emit("u_econ_circular_flow_2sector__labeled.svg", cflow(True))
emit("u_econ_circular_flow_2sector__plain.svg", cflow(False))
# F8 AD-AS-LRAS + gaps
def adas(gap=None,labeled=True):
    s=axes("Real GDP","PL")+ln(80,80,400,260,"#1d4ed8",2.5)+ln(80,260,400,80,"#b91c1c",2.5)
    lras_x = 240 if gap is None else (300 if gap=="recessionary" else 180)
    s+=ln(lras_x,Y0,lras_x,Y1,"#7c3aed",2.5)
    if labeled:
        s+=txt(90,75,"AD",13,"#1d4ed8")+txt(90,275,"SRAS",13,"#b91c1c")+txt(lras_x,34,"LRAS",12,"#7c3aed")
        x,y=eq(); s+=dot(x,y)+guide(x,y)
        if gap: s+=txt(240,310,"",1)
    return s
emit("u_econ_ad_as_lras__labeled.svg", adas(None,True))
emit("u_econ_ad_as_lras__plain.svg", adas(None,False))
emit("u_econ_recessionary_gap__labeled.svg", adas("recessionary",True))
emit("u_econ_inflationary_gap__labeled.svg", adas("inflationary",True))
# F8 money market + loanable funds + phillips
mm=axes("Q of Money","Nominal r")+ln(240,Y0,240,Y1,"#b91c1c",2.5)+ln(80,80,400,260,"#1d4ed8",2.5)
emit("u_econ_money_market__plain.svg", axes("Q of Money","Nominal r")+ln(240,Y0,240,Y1,"#b91c1c",2.5)+ln(80,80,400,260,"#1d4ed8",2.5))
emit("u_econ_money_market__labeled.svg", mm+txt(240,34,"MS",12,"#b91c1c")+txt(90,75,"MD",13,"#1d4ed8")+dot(240,170)+ln(X0,170,240,170,"#999",1,"4 4")+txt(52,174,"r*",12,"#333","end"))
lf=axes("Q of Loanable Funds","Real r")+_demandQP(100)+_supplyQP(0)
Qlf,Plf=eqQP()
emit("u_econ_loanable_funds__labeled.svg", lf+dotQP(Qlf,Plf)+guideQP(Qlf,Plf)+clabel('D',100,"D (borrowers)","#1d4ed8")+clabel('S',0,"S (savers)","#b91c1c")+txt(52,sy(Plf)+4,"r*",12,"#333","end"))
ph=axes("Unemployment","Inflation")+f'<path d="M 100 70 Q 170 220 400 250" fill="none" stroke="#1d4ed8" stroke-width="2.5"/>'+ln(220,Y0,220,Y1,"#7c3aed",2.5)
emit("u_econ_phillips_sr_lr__labeled.svg", ph+txt(120,80,"SRPC",12,"#1d4ed8")+txt(220,34,"LRPC",12,"#7c3aed")+txt(220,296,"NRU",11))
emit("u_econ_phillips_sr_lr__plain.svg", axes("Unemployment","Inflation")+f'<path d="M 100 70 Q 170 220 400 250" fill="none" stroke="#1d4ed8" stroke-width="2.5"/>'+ln(220,Y0,220,Y1,"#7c3aed",2.5))
# F7 demand schedule table
def table(title,heads,rows,blanks=()):
    oy,ch=70,34
    n=len(heads); cw=min(130,(440-40)//n); ox=(W-n*cw)//2   # 07-19 fix: center + size to column count so wide (3-col) tables never overflow the 480 viewBox
    s=txt(240,48,title,14,bold=True)
    for c,htxt in enumerate(heads):
        s+=f'<rect x="{ox+c*cw}" y="{oy}" width="{cw}" height="{ch}" fill="#f1f5f9" stroke="#333" stroke-width="1.2"/>'+txt(ox+c*cw+cw//2,oy+22,htxt,13,bold=True)
    for r,row in enumerate(rows):
        for c,cell in enumerate(row):
            yy=oy+(r+1)*ch
            s+=f'<rect x="{ox+c*cw}" y="{yy}" width="{cw}" height="{ch}" fill="none" stroke="#333" stroke-width="1.2"/>'
            if (r,c) in blanks: s+=f'<rect x="{ox+c*cw+35}" y="{yy+7}" width="60" height="20" fill="none" stroke="#94a3b8" stroke-dasharray="5 4"/>'
            else: s+=txt(ox+c*cw+cw//2,yy+22,cell,13)
    return s
rows=[("$10","20"),("$8","40"),("$6","60"),("$4","80"),("$2","100")]
emit("u_econ_demand_schedule_table__labeled.svg", table("Demand Schedule",("Price","Qd"),rows))
emit("u_econ_demand_schedule_table__plain.svg", table("Demand Schedule",("Price","Qd"),rows,blanks=((2,1),(4,1))))
ca=[("Country A","4","2"),("Country B","1","1")]
emit("u_econ_comparative_advantage_table__labeled.svg", table("Output per worker-hour",("","Wheat","Cloth"),ca))
# monopoly (QP model, exact construction): D:P=100-Q ; MR:P=100-2Q (twice the slope, same intercept,
# hits x-axis at HALF demand's Q) ; MC:P=10+0.5Q upward. Qm at MR=MC (Q=36); PRICE READ UP TO DEMAND
# (Pm=64), not to the MR=MC point (P=28) — the single most-tested monopoly idea.
Qm,Pm,Prc = 36,64,28
mono = axes("Q","$")+_demandQP(100)+lnQP(0,100,50,0,"#60a5fa",2)+lnQP(0,10,95,57.5,"#b91c1c",2.5)
mono += ln(sx(Qm),PY0,sx(Qm),sy(Pm),"#999",1,"4 4")          # Qm vertical: x-axis -> MR=MC -> up to demand
mono += ln(QX0,sy(Pm),sx(Qm),sy(Pm),"#999",1,"4 4")          # Pm horizontal to the $ axis
mono += dot(sx(Qm),sy(Prc))+dotQP(Qm,Pm)                     # MR=MC point (lower) + price point ON demand (upper)
emit("u_econ_monopoly__labeled.svg", mono
     +txt(sx(9),sy(94),"D",13,"#1d4ed8","start")+txtQP(45,13,"MR",13,"#60a5fa")+txtQP(84,60,"MC",13,"#b91c1c")
     +txt(sx(Qm),296,"Qm",12)+txt(52,sy(Pm)+4,"Pm",12,"#333","end")
     +txt(sx(Qm)+8,sy(Prc)+4,"MR=MC",10,"#666","start"))
# write + validate
os.makedirs(".",exist_ok=True); n=0
for name,svg in OUT.items():
    ET.fromstring(svg)   # raises on malformed XML
    with open(name,"w") as f: f.write(svg)
    n+=1
print(f"WROTE {n} SVGs, all XML-valid")
