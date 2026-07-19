"""Shared AP-Econ SVG primitives — import into per-family generator scripts so multiple agy/jules
jobs can generate diagrams in PARALLEL without touching the same file. Economic-coordinate model:
Q,P in 0..100; supply passes through the origin; equilibria are EXACT algebraic intersections.
Usage in a gen script:  from viz_lib import *;  save("u_econ_foo__labeled.svg", axes()+_demandQP(100)+...)"""
import os, xml.etree.ElementTree as ET

W,H=480,320; X0,Y0,X1,Y1=60,280,440,40
OUTDIR=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))   # the underlays/ dir
def head(): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="#ffffff"/>'
def tail(): return '</svg>'
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
def dot(x,y): return f'<circle cx="{x}" cy="{y}" r="4" fill="#333"/>'
def poly(pts,fill,opacity=0.18): return f'<polygon points="{pts}" fill="{fill}" opacity="{opacity}"/>'
def arrow(x1,y1,x2,y2,color="#0f766e"):
    return f'<defs><marker id="ah{abs(int(x1+y2))}" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 z" fill="{color}"/></marker></defs>'+f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2" marker-end="url(#ah{abs(int(x1+y2))})"/>'
QX0,QX1,PY0,PY1 = 60,430,280,54
def sx(Q): return round(QX0+(QX1-QX0)*Q/100.0,1)
def sy(P): return round(PY0+(PY1-PY0)*P/100.0,1)
def lnQP(Q1,P1,Q2,P2,color,w=2.5,dash=None): return ln(sx(Q1),sy(P1),sx(Q2),sy(P2),color,w,dash)
def dotQP(Q,P): return dot(sx(Q),sy(P))
def guideQP(Q,P): return ln(QX0,sy(P),sx(Q),sy(P),"#999",1,"4 4")+ln(sx(Q),sy(P),sx(Q),PY0,"#999",1,"4 4")
def txtQP(Q,P,t,size=13,fill="#333",anchor="middle",bold=False): return txt(sx(Q),sy(P),t,size,fill,anchor,bold)
def polyQP(QPpts,fill,opacity=0.18): return poly(" ".join(f"{sx(q)},{sy(p)}" for q,p in QPpts),fill,opacity)
BOX=(0,97,0,98)
def _demandQP(a,dash=None,color="#1d4ed8"):
    qlo=max(BOX[0],a-BOX[3]); qhi=min(BOX[1],a-BOX[2]); return lnQP(qlo,a-qlo,qhi,a-qhi,color,2.5,dash)
def _supplyQP(b,dash=None,color="#b91c1c"):
    qlo=max(BOX[0],BOX[2]+b); qhi=min(BOX[1],BOX[3]+b); return lnQP(qlo,qlo-b,qhi,qhi-b,color,2.5,dash)
def eqQP(dsh=0,ssh=0):
    Q=(100+dsh+ssh)/2.0; return Q, Q-ssh
def demand_top(a): qlo=max(BOX[0],a-BOX[3]); return qlo, a-qlo
def supply_top(b): qhi=min(BOX[1],BOX[3]+b); return qhi, qhi-b
def clabel(kind,ab,name,color):
    if kind=='D': Q,P=demand_top(ab); return txt(sx(Q)+14,sy(P)+3,name,13,color,"start")
    Q,P=supply_top(ab); return txt(sx(Q)-14,sy(P)+3,name,13,color,"end")
def table(title,heads,rows,blanks=()):
    oy,ch=70,34; n=len(heads); cw=min(130,(440-40)//n); ox=(W-n*cw)//2
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
def save(name,body):
    """Wrap body in the SVG frame, validate XML, write to underlays/. Raises on malformed XML."""
    svg=head()+body+tail(); ET.fromstring(svg)
    with open(os.path.join(OUTDIR,name),"w") as f: f.write(svg)
    return name
