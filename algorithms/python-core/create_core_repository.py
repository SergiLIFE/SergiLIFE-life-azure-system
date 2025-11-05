#!/us/bin/nv pyhon3
"""
L.I.F. Plfo o posioy o
======================================
uoilly s h o posioy wih ssnil fils only
Solvs iHub's "oo ny fils" union issu
"""

ipo os
ipo shuil
fo phlib ipo Ph

f oposioy():
    """ h o posioy wih ssnil fils only"""
    
    # ssnil fils fo h o posioy (p un 50 fils)
    ssnilfils = [
        # o loih Fils
        "xpinP2L.I.F.-Lnin-Iniviully-fo-xpin-hoy-loih-o-2025-opyih-S.py",
        "lifhoy.py", 
        "vnuissys.py",
        
        # in Plfo Fils
        "lnivployn.py",
        "lifhoyplfosv.py", 
        "lifhoyplfo.hl",
        "LIFLINILPLFOBI.hl",
        
        # onfiuion Fils
        ".",
        "quins.x", 
        "zuonfi.py",
        "hos.json",
        "lol.sins.json",
        "zu.yl",
        
        # zu Inion  
        "zufunionswoflow.py",
        "funionpp.py",
        
        # o Syls
        "lifhoyplfosyls.ss",
        "syls.ss",
        "inx.hl",
        
        # sin
        "olifvliion.py",
        "sipllifsinsui.py",
        
        # ssnil ounion
        "LINS",
        ".iino"
    ]
    
    uni = Ph.w()
    oi = uni.pn / "lif-plfo-o"
    
    pin("🎯 L.I.F. Plfo o posioy o")
    pin("=" * 50)
    pin(f"Sou: {uni}")
    pin(f": {oi}")
    pin()
    
    #  o ioy
    if no oi.xiss():
        oi.i(pns=u, xiso=u)
        pin(f"📁  ioy: {oi}")
    ls:
        pin(f"📁 Usin xisin ioy: {oi}")
    
    # opy ssnil fils
    opifils = 0
    issinfils = []
    
    pin("\n📋 opyin ssnil fils...")
    
    fo filn in ssnilfils:
        soufil = uni / filn
        fil = oi / filn
        
        if soufil.xiss():
            y:
                #   ioy if n
                fil.pn.i(pns=u, xiso=u)
                
                # opy fil
                shuil.opy2(soufil, fil)
                pin(f"✅ opi: {filn}")
                opifils += 1
            xp xpion s :
                pin(f"❌ o opyin {filn}: {}")
        ls:
            issinfils.ppn(filn)
            pin(f"⚠️  issin: {filn}")
    
    #  nw  fo o posioy
    o = """# L.I.F. Plfo - o Sys

**Lnin Iniviully fo xpin** - ssnil o oponns

## 🎯 posioy Fous

his posioy onins **only h ssnil o oponns** of h L.I.F. Plfo. h opl sys hs bn suu ino fous posiois fo b ininbiliy n o solv iHub's fil lii issus.

### 🧠 o oponns

- **xpinP2L loih** - in nul possin loih  
- **Plfo Sv** - o plfo funionliy
- **linil Inf** - Piy linil shbo
- **zu onfiuion** - ssnil lou inion

### 🚀 Qui S

```bash
# Insll pnnis
pip insll - quins.x

# un h plfo
pyhon lnivployn.py

# O s h hoy plfo
pyhon lifhoyplfosv.py
```

### 🔗 opl L.I.F. Plfo osys

| posioy | Pupos | Sus |
|------------|---------|--------|
| **lif-plfo-o** | ssnil loih & plfo (HIS PO) | 🟢 IV |
| **lif-zu-infsuu** | ployn & infsuu | 🔄 PLNN |
| **lif-ounion** | uis & ounion | 🔄 PLNN |
| **lif-os-xpls** | o ppliions | 🔄 PLNN |
| **lif-pins-in** | in uoion | 🔄 PLNN |

### 📊 Sys Sus

- **o Plfo**: ✅ Opionl
- **zu pl**: ✅ Liv (Off I: `960096-f1-420b-902-042561b`)  
- **Pouion y**: ✅ Spb 27, 2025
- **Fil oun**: ~{filoun} ssnil fils (vs 1,257+ in oiinl po)

---

**opyih 2025** - Sio Py Boull | L.I.F. Plfo o Sys
""".pl("{filoun}", s(opifils))
    
    # Wi nw 
    ofil = oi / "."
    wih opn(ofil, 'w', noin='uf-8') s f:
        f.wi(o)
    
    pin(f"\n📄  o : {ofil}")
    
    # Suy
    pin("\n" + "=" * 50)
    pin("✅ o posioy ion opl!")
    pin(f"📊 Fils opi: {opifils}")
    if issinfils:
        pin(f"⚠️  issin fils: {ln(issinfils)}")
        pin("   (hs y b opionl o in iffn loions)")
    
    pin(f"\n📁 o posioy  : {oi}")
    pin(f"🎯 u fo 1,257+ fils o {opifils} ssnil fils")
    
    pin("\n🚀 Nx Sps:")
    pin("1. s h o posioy:")
    pin(f"    {oi}")
    pin("   pyhon lnivployn.py")
    pin("\n2. Iniiliz i posioy:")
    pin("   i ini")
    pin("   i  .")
    pin("   i oi - 'Iniil L.I.F. Plfo o posioy'")
    pin("\n3.  iHub posioy n push")
    pin("4.  iionl fous posiois s n")
    
    un oi, opifils, issinfils

if n == "in":
    y:
        oi, opifils, issinfils = oposioy()
        
        if opifils > 0:
            pin(f"\n🎉 Suss! o posioy  wih {opifils} fils")
        ls:
            pin("\n❌ No fils w opi. Pls h h fil phs.")
            
    xp xpion s :
        pin(f"\n❌ o: {}")
        pin("Pls h h sip n y in.")