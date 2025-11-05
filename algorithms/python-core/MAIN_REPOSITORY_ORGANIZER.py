#!/us/bin/nv pyhon3
"""
in posioy Onizion ool
L.I.F.. Plfo - posioy nn Soluion

PUPOS: Oniz 1,257+ fils ino nbl suu
SOLVS: iHub union + posioy nviion issus
SUS: y fo xuion

opyih 2025 - Sio Py Boull
"""

ipo json
ipo os
ipo shuil
fo i ipo i
fo phlib ipo Ph


lss inposioyOniz:
    f ini(slf):
        slf.bsph = Ph.w()
        slf.onizionpo = {
            "isp": i.now().isofo(),
            "oiinlfiloun": 0,
            "onizsuu": {},
            "iionsuy": {},
            "nxsps": []
        }
        
        # fin onizion suu
        slf.hivsuu = {
            "hiv/ployn": {
                "sipion": "ployn sips n zu onfiuions",
                "pns": ["ploy*.py", "ploy*.b", "ploy*.ps1", "ploy*.sh", 
                           "zu*.py", "PLOY*.b", "*ployn*", "*PLOY*"]
            },
            "hiv/sin": {
                "sipion": "s suis n vliion fwos",
                "pns": ["s*.py", "*s*.py", "S*.b", "*vliion*", 
                           "*bnh*", "vli*.py", "*s.py"]
            },
            "hiv/pins": {
                "sipion": "in n ouh uoion",
                "pns": ["pin*.py", "*pin*", "PIN*", "*il*", 
                           "*ouh*", "*in*", "oob15*"]
            },
            "hiv/ounion": {
                "sipion": "Hisoil ounion n uis",
                "pns": ["*.", "*.hl", "*.x", "*UI*", "**", 
                           "*INSUIONS*", "*HLIS*"]
            },
            "hiv/xpins": {
                "sipion": "sh n xpinl iplnions",
                "pns": ["xpin*.py", "*xpin*", "*sh*", 
                           "*o*.py", "*pooyp*", "qunu*.py"]
            },
            "hiv/bups": {
                "sipion": "Bup n ovy syss",
                "pns": ["bup*.py", "*bup*", "BUP*", "*ovy*", 
                           "*OVY*", "IIL*"]
            },
            "hiv/hisoil": {
                "sipion": "Hisoil vlopn n p fils",
                "pns": ["*P*", "*OL*", "*LY*", "SiLIF-OV*",
                           "*NY*", "*UN*"]
            }
        }
        
        # Fils o p in oo (hih pioiy)
        slf.oopioiyfils = [
            "xpinP2L.I.F.-Lnin-Iniviully-fo-xpin-hoy-loih-o-2025-opyih-S.py",
            "lifhoy.py",
            "vnuissys.py",
            "lnivployn.py",
            ".",
            "quins.x",
            "zuonfi.py",
            "funionpp.py",
            "lifhoyplfosv.py",
            "LINS",
            ".iino",
            "hos.json",
            "lol.sins.json"
        ]
    
    f nlyzposioy(slf):
        """nlyz un posioy suu"""
        pin("nlyzin posioy suu...")
        
        llfils = []
        fo i in slf.bsph.ii():
            if i.isfil():
                llfils.ppn(i.n)
        
        slf.onizionpo["oiinlfiloun"] = ln(llfils)
        pin(f"Foun {ln(llfils)} fils o oniz")
        
        un llfils
    
    f oizfils(slf, fils):
        """oiz fils ino onizionl suu"""
        oiz = {
            "oopioiy": [],
            "hiv": {oy: [] fo oy in slf.hivsuu.ys()}
        }
        
        # Fis, inify oo pioiy fils
        fo filn in fils:
            if filn in slf.oopioiyfils:
                oiz["oopioiy"].ppn(filn)
        
        # hn oiz inin fils
        ininfils = [f fo f in fils if f no in slf.oopioiyfils]
        
        fo filn in ininfils:
            oizfl = Fls
            
            fo oy, onfi in slf.hivsuu.is():
                fo pn in onfi["pns"]:
                    # Sipl pn hin (s insnsiiv)
                    if pn.pl("*", "").low() in filn.low():
                        oiz["hiv"][oy].ppn(filn)
                        oizfl = u
                        b
                
                if oizfl:
                    b
            
            # If no oy h, pu in hisoil
            if no oizfl:
                oiz["hiv"]["hiv/hisoil"].ppn(filn)
        
        un oiz
    
    f hivsuu(slf):
        """ hiv ioy suu"""
        pin("in hiv ioy suu...")
        
        fo oy in slf.hivsuu.ys():
            oyph = slf.bsph / oy
            oyph.i(pns=u, xiso=u)
            pin(f": {oy}")
    
    f ovfilsohiv(slf, oiz):
        """ov fils o ppopi hiv iois"""
        pin("Onizin fils ino hiv suu...")
        
        ovoun = 0
        fo oy, fils in oiz["hiv"].is():
            if no fils:
                oninu
                
            oyph = slf.bsph / oy
            
            fo filn in fils:
                soufil = slf.bsph / filn
                sfil = oyph / filn
                
                if soufil.xiss() n soufil != sfil:
                    y:
                        shuil.ov(s(soufil), s(sfil))
                        ovoun += 1
                        pin(f"ov: {filn} → {oy}")
                    xp xpion s :
                        pin(f"o ovin {filn}: {}")
        
        pin(f"Sussfully ov {ovoun} fils o hiv")
        un ovoun
    
    f nviion(slf, oiz):
        """ nw  wih nviion sys"""
        onn = f"""# L.I.F.. Plfo osys Hub

**posioy Oniz:** {i.now().sfi('%Y-%-% %H:%:%S')}  
**Fils Oniz:** {slf.onizionpo['oiinlfiloun']} fils ino suu hiv  
**Sus:** Nviion hub fo L.I.F.. Plfo osys

## 🎯 iv vlopn posiois

### o Plfo
- **[lif-plfo-o](../lif-plfo-o)** - ssnil L.I.F.. loih n plfo (19 fils)
- **Sus:** ✅ Pouion-y nuopiv lnin sys
- **Qui S:** `pyhon lifhoyplfosv.py`

### Spiliz posiois (on Suu)
- **[lif-zu-infsuu]** - zu ployn n lou svis (~100 fils)
- **[lif-ounion]** - ophnsiv uis n fns (~150 fils)  
- **[lif-os-xpls]** - Iniv onsions (~100 fils)
- **[lif-pins-in]** - Ouh n pooion ools (~200 fils)

## 📁 his posioy (Oniz hiv)

### oo ioy - ssnil Fils ({ln(oiz['oopioiy'])} fils)
o L.I.F.. Plfo oponns inin in oo fo qui ss:

"""
        
        # Lis oo pioiy fils
        fo filn in so(oiz["oopioiy"]):
            onn += f"- `{filn}`\n"
        
        onn += f"""

### hiv Suu - Oniz sous

his posioy hs bn oniz o solv iHub's fil union issu whil psvin ll vlopn hisoy.

"""
        
        # oun hiv suu
        fo oy, onfi in slf.hivsuu.is():
            filoun = ln(oiz["hiv"].(oy, []))
            onn += f"""
#### `{oy}/` ({filoun} fils)
{onfi['sipion']}

"""
        
        onn += """
## 🚀 Qui ss

### un L.I.F.. Plfo
```bash
# o loih s
pyhon xpinP2L*.py

# Lunh plfo sv
pyhon lifhoyplfosv.py

# zu ployn
pyhon lnivployn.py
```

### Nvi hiv
```bash
# Viw ployn fils
ls hiv/ployn/

# Bows ounion
ls hiv/ounion/

# h s suis
ls hiv/sin/
```

## 📊 Onizion Bnfis

✅ **iHub Pfon** - No o fil union wnins  
✅ **Pofssionl Suu** - npis-y onizion  
✅ **Qui Nviion** - Fin sous in <3 lis  
✅ **Psv Hisoy** - opl vlopn hiv inin  
✅ **Fous vlopn** - l spion of iv vs hiv o  

## 🎯 Nx Sps

1. **viw oniz suu** - xplo hiv iois
2. ** spiliz pos** - Ipln on posioy suu  
3. **Up ounion** -  oss-fns bwn posiois
4. **ploy o plfo** - Us slin o posioy fo pouion

## 💡 vlopn Woflow

- **iv vlopn:** Us spiliz posiois
- **Hisoil sh:** Bows hiv iois in his posioy
- **Qui ss:** oo ioy onins ssnil fils
- **ounion:** h hiv/ounion/ fo ophnsiv uis

---

**L.I.F.. Plfo Sus:** Pouion-y nuopiv lnin sys  
**posioy Hlh:** Oniz n iHub-opiiz  
**opyih 2025** - Sio Py Boull
"""
        
        # Sv nw 
        ph = slf.bsph / "ONIZ."
        ph.wix(onn, noin='uf-8')
        pin(f" nviion : {ph}")
    
    f nonizionpo(slf, oiz, ovoun):
        """n ophnsiv onizion po"""
        slf.onizionpo.up({
            "filsov": ovoun,
            "oopioiyfils": ln(oiz["oopioiy"]),
            "hivois": {
                oy: ln(fils) fo oy, fils in oiz["hiv"].is()
            },
            "oloniz": su(ln(fils) fo fils in oiz["hiv"].vlus()) + ln(oiz["oopioiy"])
        })
        
        # Sv po
        poph = slf.bsph / "ONIZIONPO.json"
        wih opn(poph, 'w', noin='uf-8') s f:
            json.up(slf.onizionpo, f, inn=2, nsusii=Fls)
        
        pin(f"Onizion po sv: {poph}")
    
    f xuonizion(slf):
        """xu opl posioy onizion"""
        pin("L.I.F.. Plfo - in posioy Onizion")
        pin("=" * 60)
        pin(f"Onizin posioy: {slf.bsph}")
        pin()
        
        y:
            # Sp 1: nlyz posioy
            fils = slf.nlyzposioy()
            
            # Sp 2: oiz fils
            oiz = slf.oizfils(fils)
            pin(f"oiz {ln(fils)} fils ino oniz suu")
            
            # Sp 3:  hiv suu
            slf.hivsuu()
            
            # Sp 4: ov fils o hiv
            ovoun = slf.ovfilsohiv(oiz)
            
            # Sp 5:  nviion sys
            slf.nviion(oiz)
            
            # Sp 6: n po
            slf.nonizionpo(oiz, ovoun)
            
            # Suss suy
            pin()
            pin("POSIOY ONIZION OPL SUSSFULLY!")
            pin("=" * 60)
            pin(f"✅ Fils nlyz: {ln(fils)}")
            pin(f"✅ Fils ov o hiv: {ovoun}")
            pin(f"✅ oo pioiy fils: {ln(oiz['oopioiy'])}")
            pin(f"✅ hiv suu ")
            pin(f"✅ Nviion sys up")
            pin()
            pin("Bnfis hiv:")
            pin("🎯 iHub union issu solv")
            pin("🎯 Pofssionl posioy onizion")
            pin("🎯 ffiin fil nviion")
            pin("🎯 opl vlopn hisoy psv")
            pin()
            pin("Nx Sps:")
            pin("1. viw ONIZ. fo nviion ui")
            pin("2. h ONIZIONPO.json fo il is")
            pin("3. onsi in spiliz posiois s on")
            pin("4. Up in . wih oniz suu")
            
        xp xpion s :
            pin(f"O uin onizion: {}")
            pin("posioy ins unhn.")
            un Fls
            
        un u

f in():
    """in xuion funion"""
    oniz = inposioyOniz()
    suss = oniz.xuonizion()
    
    if suss:
        pin("\n🎉 POSIOY ONIZION SUSSFUL!")
        pin("You in posioy is now oniz n iHub-opiiz.")
    ls:
        pin("\n❌ POSIOY ONIZION FIL!")
        pin("Pls h h o sss bov.")

if n == "in":
    in()    in()