#!/usr/bin/env python3
"""Deterministic AP-Econ SVG factory (lean priority set). House style: 480x320, white bg,
#333 axes, demand #1d4ed8, supply #b91c1c, shifts dashed + #0f766e arrows. Variants:
labeled (inline example image) / plain (pad underlay, no answer-revealing marks)."""
import os, xml.etree.ElementTree as ET

W,H=480,320; X0,Y0,X1,Y1=60,280,440,40   # axes frame: origin bottom-left
def head(): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="#ffffff"/>'
def axes(xl="Q",yl="P"):
    s=f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1}" stroke="#333" stroke-width="2"/><line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="#333" stroke-width="2"/>'
    s+=f'<text x="{X1}" y="298" font-family="sans-serif" font-size="12" fill="#555" text-anchor="end">{xl}</text>'
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
# A,B must sit EXACTLY ON the frontier (Bezier M60,70 Q300,100 420,280): points computed at t=0.35, 0.68.
def _bz(t,p0,p1,p2): return (round((1-t)**2*p0[0]+2*t*(1-t)*p1[0]+t*t*p2[0],1),round((1-t)**2*p0[1]+2*t*(1-t)*p1[1]+t*t*p2[1],1))
_A=_bz(0.35,(60,70),(300,100),(420,280)); _B=_bz(0.68,(60,70),(300,100),(420,280))
emit("u_econ_ppc_bowed__labeled.svg", axes("Good X","Good Y")+ppc
     +dot(*_A)+txt(_A[0]+12,_A[1]-6,"A",13)+dot(*_B)+txt(_B[0]+12,_B[1]-6,"B",13)
     +dot(180,200)+txt(180,218,"C (inefficient)",12)+dot(390,90)+txt(392,78,"D (unattainable)",12))
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
    fs=lambda t:(13 if len(str(t))*7<=cw-12 else max(9,int((cw-12)/(len(str(t))*0.6))))   # auto-shrink long cells to fit
    s=txt(240,48,title,14,bold=True)
    for c,htxt in enumerate(heads):
        s+=f'<rect x="{ox+c*cw}" y="{oy}" width="{cw}" height="{ch}" fill="#f1f5f9" stroke="#333" stroke-width="1.2"/>'+txt(ox+c*cw+cw//2,oy+22,htxt,fs(htxt),bold=True)
    for r,row in enumerate(rows):
        for c,cell in enumerate(row):
            yy=oy+(r+1)*ch
            s+=f'<rect x="{ox+c*cw}" y="{yy}" width="{cw}" height="{ch}" fill="none" stroke="#333" stroke-width="1.2"/>'
            if (r,c) in blanks: s+=f'<rect x="{ox+c*cw+35}" y="{yy+7}" width="60" height="20" fill="none" stroke="#94a3b8" stroke-dasharray="5 4"/>'
            else: s+=txt(ox+c*cw+cw//2,yy+22,cell,fs(cell))
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

# CS & PS, Price Ceiling, Price Floor, Per-unit Tax
cs_poly = f'<polygon points="{sx(0)},{sy(50)} {sx(0)},{sy(100)} {sx(50)},{sy(50)}" fill="#1d4ed8" opacity="0.18"/>'
ps_poly = f'<polygon points="{sx(0)},{sy(0)} {sx(50)},{sy(50)} {sx(0)},{sy(50)}" fill="#b91c1c" opacity="0.18"/>'
emit("u_econ_consumer_producer_surplus__plain.svg", axes() + _demandQP(100) + _supplyQP(0))
emit("u_econ_consumer_producer_surplus__labeled.svg", axes() + cs_poly + ps_poly + _demandQP(100) + _supplyQP(0) + dotQP(50,50) + guideQP(50,50) + txtQP(18,72,"CS",13,"#1d4ed8") + txtQP(18,30,"PS",13,"#b91c1c") + txtQP(8,92,"D",13,"#1d4ed8") + txtQP(90,92,"S",13,"#b91c1c"))

ceiling_line = lnQP(0,30,100,30,"#0f766e",2,"6 4")
ceiling_guides = ln(sx(30),sy(30),sx(30),Y0,"#999",1,"4 4") + ln(sx(70),sy(30),sx(70),Y0,"#999",1,"4 4")
emit("u_econ_price_ceiling__plain.svg", axes() + _demandQP(100) + _supplyQP(0) + ceiling_line)
emit("u_econ_price_ceiling__labeled.svg", axes() + _demandQP(100) + _supplyQP(0) + ceiling_line + ceiling_guides + dotQP(30,30) + dotQP(70,30) + txtQP(85,34,"Price ceiling",12,"#0f766e") + txt(sx(30),296,"Qs",12) + txt(sx(70),296,"Qd",12) + txtQP(50,20,"Shortage",12) + txtQP(8,92,"D",13,"#1d4ed8") + txtQP(90,92,"S",13,"#b91c1c"))

floor_line = lnQP(0,70,100,70,"#0f766e",2,"6 4")
floor_guides = ln(sx(30),sy(70),sx(30),Y0,"#999",1,"4 4") + ln(sx(70),sy(70),sx(70),Y0,"#999",1,"4 4")
emit("u_econ_price_floor__plain.svg", axes() + _demandQP(100) + _supplyQP(0) + floor_line)
emit("u_econ_price_floor__labeled.svg", axes() + _demandQP(100) + _supplyQP(0) + floor_line + floor_guides + dotQP(30,70) + dotQP(70,70) + txtQP(85,74,"Price floor",12,"#0f766e") + txt(sx(30),296,"Qd",12) + txt(sx(70),296,"Qs",12) + txtQP(50,84,"Surplus",12) + txtQP(8,92,"D",13,"#1d4ed8") + txtQP(90,92,"S",13,"#b91c1c"))

dwl_poly = f'<polygon points="{sx(40)},{sy(60)} {sx(40)},{sy(40)} {sx(50)},{sy(50)}" fill="#6b7280" opacity="0.25"/>'
tax_guides = ln(sx(40),Y0,sx(40),sy(60),"#999",1,"4 4") + ln(X0,sy(60),sx(40),sy(60),"#999",1,"4 4") + ln(X0,sy(40),sx(40),sy(40),"#999",1,"4 4")
emit("u_econ_per_unit_tax__plain.svg", axes() + _demandQP(100) + _supplyQP(0))   # 07-20 QA: pad scaffold = pre-tax D+S ONLY; the S+tax shift is the answer the student must draw, so it stays out of the pad (kept on __labeled reference)
dwl_leader = ln(sx(76),sy(15),sx(47),sy(49),"#999",1)   # leader from the open-space DWL label to the small triangle
emit("u_econ_per_unit_tax__labeled.svg", axes() + dwl_poly + _demandQP(100) + _supplyQP(0) + _supplyQP(-20,"7 5") + tax_guides + dwl_leader + dotQP(40,60) + dotQP(40,40) + txtQP(52,80,"S+tax",12,"#b91c1c") + txtQP(90,90,"S",13,"#b91c1c") + txtQP(9,90,"D",13,"#1d4ed8") + txt(52,sy(60)+4,"Pb",12,"#333","end") + txt(52,sy(40)+4,"Ps",12,"#333","end") + txtQP(80,12,"DWL",11,"#555") + txt(sx(40),296,"Qt",12))

# WAVE T: data-table family (compute-from-table; the corpus's biggest under-served category)
emit("u_econ_marginal_utility_table__labeled.svg", table("Marginal Utility",["Units","Total Utility","Marginal Utility"],[["1","10","10"],["2","18","8"],["3","24","6"],["4","28","4"],["5","30","2"]]))
emit("u_econ_marginal_utility_table__plain.svg", table("Marginal Utility",["Units","Total Utility","Marginal Utility"],[["1","10","10"],["2","18","8"],["3","24","6"],["4","28","4"],["5","30","2"]],blanks=[(1,2),(2,2),(3,2)]))
emit("u_econ_production_output_table__labeled.svg", table("Production & Marginal Product",["Labour","Total Product","Marginal Product"],[["1","10","10"],["2","24","14"],["3","33","9"],["4","39","6"],["5","42","3"]]))
emit("u_econ_production_output_table__plain.svg", table("Production & Marginal Product",["Labour","Total Product","Marginal Product"],[["1","10","10"],["2","24","14"],["3","33","9"],["4","39","6"],["5","42","3"]],blanks=[(1,2),(2,2),(3,2)]))
emit("u_econ_cpi_basket_table__labeled.svg", table("CPI Basket",["Item","Qty","Base $","Now $"],[["Bread","10","2","3"],["Milk","8","3","4"],["Eggs","6","2","2"]]))
emit("u_econ_gdp_nominal_real_table__labeled.svg", table("Nominal vs Real GDP",["Year","Nominal GDP","Price Index","Real GDP"],[["1 (base)","500","100","500"],["2","560","112","500"],["3","648","120","540"]]))
emit("u_econ_gdp_nominal_real_table__plain.svg", table("Nominal vs Real GDP",["Year","Nominal GDP","Price Index","Real GDP"],[["1 (base)","500","100","500"],["2","560","112","500"],["3","648","120","540"]],blanks=[(1,3),(2,3)]))
emit("u_econ_consumption_saving_table__labeled.svg", table("Consumption & Saving",["Income","Consumption","Saving"],[["0","20","-20"],["100","100","0"],["200","180","20"],["300","260","40"]]))
emit("u_econ_consumption_saving_table__plain.svg", table("Consumption & Saving",["Income","Consumption","Saving"],[["0","20","-20"],["100","100","0"],["200","180","20"],["300","260","40"]],blanks=[(1,2),(2,2),(3,2)]))
# WAVE R #2/#3: labor market + forex — pure S&D structure, exact QP model (supply through origin)
def sd_relabel(xl,yl,dlab,slab,plab,qlab):
    a=axes(xl,yl)+_demandQP(100)+_supplyQP(0); Q,P=eqQP()
    return a+dotQP(Q,P)+guideQP(Q,P)+clabel('D',100,dlab,"#1d4ed8")+clabel('S',0,slab,"#b91c1c")+txt(52,sy(P)+4,plab,12,"#333","end")+txt(sx(Q),296,qlab,12)
emit("u_econ_labor_market__labeled.svg", sd_relabel("Quantity of Labour","Wage","D = MRP","S","W*","L*"))
emit("u_econ_labor_market__plain.svg", axes("Quantity of Labour","Wage")+_demandQP(100)+_supplyQP(0))
emit("u_econ_forex_market__labeled.svg", sd_relabel("Quantity of $","Exchange rate","D $","S $","e*","Q*"))
emit("u_econ_forex_market__plain.svg", axes("Quantity of $","Exchange rate")+_demandQP(100)+_supplyQP(0))
# WAVE R #1: perfect-competition FIRM + MARKET side-by-side (720-wide). Cost curves pass through the
# AVC min (q=8) and ATC min (q=10); MC = 7q-20 runs through BOTH minima. Long-run: P = ATC min = 50 →
# firm produces q*=10 where MC=P=ATC → ZERO economic profit. The #1 AP-Micro FRQ graph.
def firm_market(labeled=True):
    W2,H2,PT,PB=720,300,40,250
    def py(P): return round(PT+(PB-PT)*(100-P)/100.0,1)
    def frame(x0,x1,title):
        s=f'<line x1="{x0}" y1="{PT}" x2="{x0}" y2="{PB}" stroke="#333" stroke-width="2"/><line x1="{x0}" y1="{PB}" x2="{x1}" y2="{PB}" stroke="#333" stroke-width="2"/>'
        s+=f'<text x="{(x0+x1)/2}" y="28" font-family="sans-serif" font-size="13" font-weight="700" fill="#333" text-anchor="middle">{title}</text>'
        s+=f'<text x="{x1}" y="{PB+15}" font-family="sans-serif" font-size="11" fill="#555" text-anchor="end">Q</text>'
        s+=f'<text x="{x0-6}" y="{PT+2}" font-family="sans-serif" font-size="11" fill="#555" text-anchor="end">$</text>'
        return s
    def dash(x1,y1,x2,y2,col="#999",w=1): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{w}" stroke-dasharray="4 4"/>'
    def T(x,y,t,fill="#333",anc="middle",sz=11): return f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{sz}" fill="{fill}" text-anchor="{anc}">{t}</text>'
    b=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W2} {H2}"><rect width="{W2}" height="{H2}" fill="#fff"/>'
    # LEFT market panel
    mx0,mx1=60,300
    def mfx(Q): return round(mx0+(mx1-mx0)*Q/100.0,1)
    b+=frame(mx0,mx1,"Market")
    b+=f'<line x1="{mfx(2)}" y1="{py(98)}" x2="{mfx(97)}" y2="{py(3)}" stroke="#1d4ed8" stroke-width="2.5"/>'
    b+=f'<line x1="{mfx(0)}" y1="{py(0)}" x2="{mfx(97)}" y2="{py(97)}" stroke="#b91c1c" stroke-width="2.5"/>'
    if labeled:
        b+=dash(mx0,py(50),mfx(50),py(50))+dash(mfx(50),py(50),mfx(50),PB)+f'<circle cx="{mfx(50)}" cy="{py(50)}" r="4" fill="#333"/>'
        b+=T(mfx(9),py(93),"D","#1d4ed8")+T(mfx(90),py(93),"S","#b91c1c","end")+T(mx0-5,py(50)+4,"Pe","#333","end")+T(mfx(50),PB+15,"Qe")
    # RIGHT firm panel
    fx0,fx1=420,680
    def ffx(q): return round(fx0+(fx1-fx0)*q/20.0,1)
    b+=frame(fx0,fx1,"Firm")
    AVC=lambda q:36+0.9*(q-8)**2; ATC=lambda q:50+0.9*(q-10)**2; MC=lambda q:7*q-20
    def curve(fn,color,q0=3.5,q1=18.5):
        pts=[]; q=q0
        while q<=q1+1e-6: pts.append(f"{ffx(q)},{py(fn(q))}"); q+=0.5
        return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2.2"/>'
    b+=curve(AVC,"#f59e0b")+curve(ATC,"#0f766e")
    b+=f'<line x1="{ffx(5)}" y1="{py(MC(5))}" x2="{ffx(16.5)}" y2="{py(MC(16.5))}" stroke="#b91c1c" stroke-width="2.2"/>'   # MC = 7q-20
    b+=f'<line x1="{fx0}" y1="{py(50)}" x2="{fx1}" y2="{py(50)}" stroke="#1d4ed8" stroke-width="2"/>'   # P=MR=D at 50
    if labeled:
        b+=f'<circle cx="{ffx(10)}" cy="{py(50)}" r="4" fill="#333"/>'+dash(ffx(10),py(50),ffx(10),PB)
        b+=T(ffx(10),PB+15,"q*")+T(fx1-2,py(50)-5,"P = MR = D","#1d4ed8","end")
        b+=T(ffx(16.3)+4,py(MC(16.3)),"MC","#b91c1c","start")+T(ffx(15)+6,py(ATC(15)),"ATC","#0f766e","start")+T(ffx(12.5)+6,py(AVC(12.5))+2,"AVC","#f59e0b","start")
    b+=dash(mfx(50),py(50),fx0,py(50),"#cbd5e1",1)   # "firm takes the market price" connector
    b+='</svg>'
    return b
OUT["u_econ_perfect_comp_firm_market__labeled.svg"]=firm_market(True)
OUT["u_econ_perfect_comp_firm_market__plain.svg"]=firm_market(False)
# WAVE O: cost curves standalone. Consistent model: AVC=18+0.3(q-8)^2 (min q=8), AFC=130/q (hyperbola),
# ATC=AVC+AFC (min ~q=10.4, RIGHT of AVC min), MC=18+0.3(q-8)^2+0.6q(q-8) crosses AVC & ATC at their minima.
def cost_curves(labeled=True):
    qx=lambda q:sx(q*5)   # q 0..20 -> Q 0..100
    AVC=lambda q:18+0.3*(q-8)**2; AFC=lambda q:130.0/q; ATC=lambda q:AVC(q)+AFC(q)
    MC=lambda q:18+0.3*(q-8)**2+0.6*q*(q-8)
    def cv(fn,color,q0,q1):
        pts=[]; q=q0
        while q<=q1+1e-6:
            p=fn(q)
            if 2<=p<=99: pts.append(f"{qx(q)},{sy(p)}")
            q+=0.5
        return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2.2"/>'
    b=axes("Q","$")+cv(AFC,"#94a3b8",3,20)+cv(AVC,"#f59e0b",3,20)+cv(ATC,"#0f766e",3,20)+cv(MC,"#b91c1c",4,15)
    if labeled:
        b+=dot(qx(8),sy(AVC(8)))+dot(qx(10.4),sy(ATC(10.4)))
        b+=txt(qx(14.5)+3,sy(MC(14.5)),"MC",11,"#b91c1c","start")+txt(qx(19)+2,sy(ATC(19)),"ATC",11,"#0f766e","start")+txt(qx(19)+2,sy(AVC(19))+4,"AVC",11,"#f59e0b","start")+txt(qx(18)+2,sy(AFC(18))+4,"AFC",11,"#94a3b8","start")
    return b
OUT["u_econ_cost_curves__labeled.svg"]=head()+cost_curves(True)+tail()
OUT["u_econ_cost_curves__plain.svg"]=head()+cost_curves(False)+tail()
# WAVE O: monopolistic competition LONG-RUN (tangency). D tangent to ATC at q*=7 -> P=ATC=zero profit;
# MR=MC at that same q*. ATC=40+0.4(q-10)^2 (min q=10); D=60.4-2.4q (tangent at (7,43.6)); MR=60.4-4.8q;
# MC=4.4q-4 (through the tangency's MR=MC point (7,26.8) and the ATC min (10,40)).
def monop_comp(labeled=True):
    qx=lambda q:sx(q*4)   # q 0..25 -> Q 0..100
    ATC=lambda q:40+0.4*(q-10)**2; D=lambda q:60.4-2.4*q; MR=lambda q:60.4-4.8*q; MC=lambda q:4.4*q-4
    def cv(fn,color,q0,q1,w=2.4):
        pts=[]; q=q0
        while q<=q1+1e-6:
            p=fn(q)
            if 1<=p<=99: pts.append(f"{qx(q)},{sy(p)}")
            q+=0.5
        return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="{w}"/>'
    b=axes("Q","$")+cv(ATC,"#0f766e",3,17)
    b+=f'<line x1="{qx(0)}" y1="{sy(D(0))}" x2="{qx(24)}" y2="{sy(D(24))}" stroke="#1d4ed8" stroke-width="2.4"/>'
    b+=f'<line x1="{qx(0)}" y1="{sy(MR(0))}" x2="{qx(12)}" y2="{sy(MR(12))}" stroke="#60a5fa" stroke-width="2"/>'
    b+=cv(MC,"#b91c1c",2,16)
    if labeled:
        b+=ln(qx(7),Y0,qx(7),sy(43.6),"#999",1,"4 4")+dot(qx(7),sy(43.6))+dot(qx(7),sy(26.8))
        b+=txt(48,sy(43.6)+4,"P=ATC",10,"#333","end")+txt(qx(7),296,"q*",11)
        b+=txt(qx(20)+3,sy(D(20)),"D",11,"#1d4ed8","start")+txt(qx(9.7)+2,sy(MR(9.7)),"MR",11,"#60a5fa","start")+txt(qx(14.5)+3,sy(MC(14.5)),"MC",11,"#b91c1c","start")+txt(qx(15.5)+3,sy(ATC(15.5)),"ATC",11,"#0f766e","start")
        b+=txt(qx(1.5),sy(93),"LR equilibrium: P = ATC (zero profit)",10,"#0f766e","start")
    return b
OUT["u_econ_monopolistic_comp__labeled.svg"]=head()+monop_comp(True)+tail()
OUT["u_econ_monopolistic_comp__plain.svg"]=head()+monop_comp(False)+tail()
# write + validate
os.makedirs(".",exist_ok=True); n=0
for name,svg in OUT.items():
    ET.fromstring(svg)   # raises on malformed XML
    with open(name,"w") as f: f.write(svg)
    n+=1
print(f"WROTE {n} SVGs, all XML-valid")
