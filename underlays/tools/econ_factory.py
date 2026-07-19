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
    x=(240+(off_d+off_s)/2); y=170+(off_s-off_d)/2   # midpoint eq of the two lines given symmetric slopes
    return x,y
def grid():
    s=''
    for gx in range(X0+38,X1,38): s+=ln(gx,Y1,gx,Y0,"#e2e8f0",1)
    for gy in range(Y1+30,Y0,30): s+=ln(X0,gy,X1,gy,"#e2e8f0",1)
    return s
def tail(): return '</svg>'
OUT={}
def emit(name,body): OUT[name]=head()+body+tail()

# F1 supply-demand core
b=axes()+demand()+supply(); x,y=eq()
emit("u_econ_sd_equilibrium__plain.svg", b)
emit("u_econ_sd_equilibrium__labeled.svg", b+dot(x,y)+guide(x,y)+txt(90,75,"D",14,"#1d4ed8")+txt(90,275,"S",14,"#b91c1c")+txt(52,y+4,"Pe",12,"#333","end")+txt(x,296,"Qe",12))
g=axes()+grid()+ln(80,70,400,250,"#1d4ed8",2.5)+ln(80,250,400,70,"#b91c1c",2.5)
emit("u_econ_sd_numeric_grid__plain.svg", g)
lab=g+dot(240,160)+guide(240,160)
for i,p in enumerate(range(12,0,-2)): lab+=txt(50,Y0-(i+0)*40+4 if False else Y0-((i)*40)+4,"",1)   # skip fancy ticks
prices=[("$12",40),("$9",100),("$6",160),("$3",220)]
for t,yy in prices: lab+=txt(50,yy+4,t,11,"#333","end")
qs=[("30",150),("60",240),("90",330)]
for t,xx in qs: lab+=txt(xx,296,t,11)
emit("u_econ_sd_numeric_grid__labeled.svg", lab+txt(90,75,"D",14,"#1d4ed8")+txt(90,275,"S",14,"#b91c1c"))
for slug,dd,ss,dl in [("demand_shift_right",55,0,"D1→D2 right"),("demand_shift_left",-55,0,"D1→D2 left"),("supply_shift_right",0,55,"S1→S2 right"),("supply_shift_left",0,-55,"S1→S2 left")]:
    base=axes()+demand()+supply()
    shifted = demand(dd,"7 5") if dd else supply(ss,"7 5")
    x2,y2=eq(dd,ss); x1,y1=eq()
    ar = arrow(240+(15 if (dd>0 or ss>0) else -15),165,240+(45 if (dd>0 or ss>0) else -45),165)
    emit(f"u_econ_{slug}__plain.svg", base)   # plain = curves only, student draws the shift
    labl=("D1" if dd else "S1", "D2" if dd else "S2")
    col="#1d4ed8" if dd else "#b91c1c"
    emit(f"u_econ_{slug}__labeled.svg", base+shifted+ar+dot(x1,y1)+dot(x2,y2)+guide(x2,y2)+txt(90,75 if dd else 275,labl[0],13,col)+txt(90+(dd or ss),(75 if dd else 275),labl[1],13,col))
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
lf=axes("Q of Loanable Funds","Real r")+demand()+supply()
emit("u_econ_loanable_funds__labeled.svg", lf+txt(90,75,"D (borrowers)",11,"#1d4ed8","start")+txt(90,275,"S (savers)",11,"#b91c1c","start")+dot(240,170)+guide(240,170)+txt(52,174,"r*",12,"#333","end"))
ph=axes("Unemployment","Inflation")+f'<path d="M 100 70 Q 170 220 400 250" fill="none" stroke="#1d4ed8" stroke-width="2.5"/>'+ln(220,Y0,220,Y1,"#7c3aed",2.5)
emit("u_econ_phillips_sr_lr__labeled.svg", ph+txt(120,80,"SRPC",12,"#1d4ed8")+txt(220,34,"LRPC",12,"#7c3aed")+txt(220,296,"NRU",11))
emit("u_econ_phillips_sr_lr__plain.svg", axes("Unemployment","Inflation")+f'<path d="M 100 70 Q 170 220 400 250" fill="none" stroke="#1d4ed8" stroke-width="2.5"/>'+ln(220,Y0,220,Y1,"#7c3aed",2.5))
# F7 demand schedule table
def table(title,heads,rows,blanks=()):
    ox,oy,cw,ch=110,70,130,34
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
# monopoly (labeled only tonight — geometry needs care)
mono=axes("Q","$")+ln(80,80,400,260,"#1d4ed8",2.5)+ln(80,80,300,300-20,"#60a5fa",2)+f'<path d="M 100 240 Q 200 150 380 60" fill="none" stroke="#b91c1c" stroke-width="2.5"/>'
qm_x=205; mono+=ln(qm_x,Y0,qm_x,163,"#999",1,"4 4")+ln(X0,163,qm_x,163,"#999",1,"4 4")+dot(qm_x,163)
emit("u_econ_monopoly__labeled.svg", mono+txt(90,75,"D",13,"#1d4ed8")+txt(255,268,"MR",12,"#60a5fa")+txt(360,66,"MC",12,"#b91c1c")+txt(qm_x,296,"Qm",12)+txt(52,167,"Pm",12,"#333","end"))
# write + validate
os.makedirs(".",exist_ok=True); n=0
for name,svg in OUT.items():
    ET.fromstring(svg)   # raises on malformed XML
    with open(name,"w") as f: f.write(svg)
    n+=1
print(f"WROTE {n} SVGs, all XML-valid")
