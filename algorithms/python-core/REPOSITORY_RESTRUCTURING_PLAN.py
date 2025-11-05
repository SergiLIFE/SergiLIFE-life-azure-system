#!/us/bin/nv pyhon3
"""
L.I.F. Plfo posioy suuin Sys
===============================================

iHub visoy: posioy oo L (1,257+ fils)
ol: Spli ino nbl huns whil ininin funionliy

his sys will:
1. nlyz un posioy suu
2. oiz fils by pupos n ipon
3.  sp posiois fo iffn oponns
4. inin o funionliy in in po
5. S up pop oss-posioy fns

opyih 2025 - Sio Py Boull
"""

ipo json
ipo os
ipo shuil
fo i ipo i
fo phlib ipo Ph


lss posioysuu:
    f ini(slf, bsph):
        slf.bsph = Ph(bsph)
        slf.nlysispo = {
            "olfils": 0,
            "ois": {},
            "onsuu": {},
            "iionpln": [],
            "isp": i.now().isofo()
        }
        
        # fin h nw posioy suu
        slf.nwpos = {
            "lif-plfo-o": {
                "sipion": "o L.I.F. Plfo - ssnil loih n plfo",
                "xfils": 50,
                "pioiy": "IIL",
                "fils": []
            },
            "lif-zu-infsuu": {
                "sipion": "zu ployn n infsuu oponns", 
                "xfils": 100,
                "pioiy": "HIH",
                "fils": []
            },
            "lif-ounion": {
                "sipion": "ounion, uis, n fn ils",
                "xfils": 150,
                "pioiy": "IU", 
                "fils": []
            },
            "lif-os-xpls": {
                "sipion": "o ppliions n xpl iplnions",
                "xfils": 100,
                "pioiy": "IU",
                "fils": []
            },
            "lif-pins-in": {
                "sipion": "in pins n ouh uoion",
                "xfils": 200,
                "pioiy": "LOW",
                "fils": []
            },
            "lif-hiv-vlopn": {
                "sipion": "Hisoil vlopn fils n ly oponns",
                "xfils": 500,
                "pioiy": "HIV",
                "fils": []
            }
        }
        
    f nlyzposioy(slf):
        """nlyz un posioy suu n oiz fils"""
        pin("🔍 nlyzin posioy suu...")
        
        # Fil oizion pns
        ois = {
            "oloih": ["xpinP2L", "lifhoy.py", "vnui", "qunu"],
            "zuployn": ["zu", "ploy", "funionpp", "hos.json"],
            "ounion": ["", ".", "UI", "INSUIONS"],
            "os": ["o", "linil", "uionl", "iniv"],
            "pins": ["pin", "il", "ouh", "iosof"],
            "onfiuion": [".json", ".yl", ".yl", "onfi", "quins"],
            "sin": ["s", "vliion", "bnh"],
            "uoion": ["uoion", "uonoous", "onio"],
            "ly": ["bup", "ol", "p", "hiv"],
            "poy": ["p", "p", "qui", "ny"]
        }
        
        llfils = lis(slf.bsph.lob("*"))
        slf.nlysispo["olfils"] = ln([f fo f in llfils if f.isfil()])
        
        pin(f"📊 Foun {slf.nlysispo['olfils']} ol fils")
        
        # oiz h fil
        fo filph in llfils:
            if filph.isfil():
                livph = filph.livo(slf.bsph)
                fils = s(livph).low()
                
                oiz = Fls
                fo oy, pns in ois.is():
                    if ny(pn.low() in fils fo pn in pns):
                        if oy no in slf.nlysispo["ois"]:
                            slf.nlysispo["ois"][oy] = []
                        slf.nlysispo["ois"][oy].ppn(s(livph))
                        oiz = u
                        b
                
                if no oiz:
                    if "unoiz" no in slf.nlysispo["ois"]:
                        slf.nlysispo["ois"]["unoiz"] = []
                    slf.nlysispo["ois"]["unoiz"].ppn(s(livph))
        
        un slf.nlysispo
    
    f oposioysuu(slf):
        """Inify h ssnil fils fo h o posioy"""
        pin("🎯 in o posioy suu...")
        
        # ssnil fils fo o posioy (us b un 50 fils)
        ssnilfils = [
            # o loih
            "xpinP2L.I.F.-Lnin-Iniviully-fo-xpin-hoy-loih-o-2025-opyih-S.py",
            "lifhoy.py",
            "vnuissys.py",
            
            # in onfiuion
            ".",
            "quins.x",
            "zuonfi.py",
            
            # ssnil Plfo Fils
            "lnivployn.py",
            "lifhoyplfosv.py",
            "LIFLINILPLFOBI.hl",
            
            # iil zu oponns
            "zufunionswoflow.py",
            "hos.json",
            "lol.sins.json",
            
            # ssnil ounion
            "QUIS.",
            "PLOYNUI.",
            
            # Lins n Ll
            "LINS",
            ".iino"
        ]
        
        #  o o po
        fo fil in ssnilfils:
            if (slf.bsph / fil).xiss():
                slf.nwpos["lif-plfo-o"]["fils"].ppn(fil)
        
        pin(f"✅ o posioy: {ln(slf.nwpos['lif-plfo-o']['fils'])} ssnil fils")
        
    f ssinfilsoposiois(slf):
        """ssin inin fils o ppopi posiois"""
        pin("📂 ssinin fils o posiois...")
        
        # ssinn uls bs on fil pns
        ssinnuls = {
            "lif-zu-infsuu": [
                "zu", "ploy", "funion", "inf/", ".bip", 
                "loushll", "subsipion", "pl"
            ],
            "lif-ounion": [
                "", ".", "UI", "INSUIONS", "NUL", 
                "HLIS", "NOS", "PO"
            ],
            "lif-os-xpls": [
                "o", "linil", "uionl", "iniv", 
                "xpl", "uoil", "vliion"
            ],
            "lif-pins-in": [
                "pin", "il", "ouh", "iosof", 
                "in", "pnship", "oob15"
            ]
        }
        
        llfils = [f fo f in slf.bsph.lob("*") if f.isfil()]
        
        fo filph in llfils:
            livph = s(filph.livo(slf.bsph))
            fillow = livph.low()
            
            # Sip if ly in o
            if livph in slf.nwpos["lif-plfo-o"]["fils"]:
                oninu
            
            # ssin bs on uls
            ssin = Fls
            fo pon, pns in ssinnuls.is():
                if ny(pn in fillow fo pn in pns):
                    slf.nwpos[pon]["fils"].ppn(livph)
                    ssin = u
                    b
            
            # If no ssin, pu in hiv
            if no ssin:
                slf.nwpos["lif-hiv-vlopn"]["fils"].ppn(livph)
        
        # Pin suy
        fo pon, poinfo in slf.nwpos.is():
            pin(f"📁 {pon}: {ln(poinfo['fils'])} fils")
    
    f iionpln(slf):
        """ il iion pln"""
        pin("📋 in iion pln...")
        
        iionsps = [
            {
                "sp": 1,
                "ion": " lif-plfo-o posioy",
                "sipion": "ssnil L.I.F. Plfo funionliy only",
                "filsoun": ln(slf.nwpos["lif-plfo-o"]["fils"]),
                "pioiy": "II"
            },
            {
                "sp": 2,
                "ion": " lif-zu-infsuu posioy", 
                "sipion": "ll zu ployn n infsuu",
                "filsoun": ln(slf.nwpos["lif-zu-infsuu"]["fils"]),
                "pioiy": "HIH"
            },
            {
                "sp": 3,
                "ion": " lif-ounion posioy",
                "sipion": "ll ounion n uis", 
                "filsoun": ln(slf.nwpos["lif-ounion"]["fils"]),
                "pioiy": "IU"
            },
            {
                "sp": 4,
                "ion": " lif-os-xpls posioy",
                "sipion": "o ppliions n xpls",
                "filsoun": ln(slf.nwpos["lif-os-xpls"]["fils"]),
                "pioiy": "IU"
            },
            {
                "sp": 5,
                "ion": " lif-pins-in posioy",
                "sipion": "in n pin uoion",
                "filsoun": ln(slf.nwpos["lif-pins-in"]["fils"]),
                "pioiy": "LOW"
            },
            {
                "sp": 6,
                "ion": " lif-hiv-vlopn posioy",
                "sipion": "hiv hisoil n vlopn fils",
                "filsoun": ln(slf.nwpos["lif-hiv-vlopn"]["fils"]),
                "pioiy": "HIV"
            }
        ]
        
        slf.nlysispo["iionpln"] = iionsps
        un iionsps
    
    f nnwin(slf):
        """n  nw in  fo h o posioy"""
        onn = """# L.I.F. Plfo - o Sys

**Lnin Iniviully fo xpin** - Pouion-y Nul Possin Plfo

## 🎯 posioy Suu (Novb 2025 suu)

his posioy onins only h **ssnil o oponns** of h L.I.F. Plfo. h opl sys hs bn suu ino fous posiois fo b ininbiliy.

### 📚 posioy osys

| posioy | Pupos | Fils | Sus |
|------------|---------|-------|--------|
| **lif-plfo-o** | o loih n plfo (HIS PO) | ~50 | 🟢 IV |
| **lif-zu-infsuu** | zu ployn & infsuu | ~100 | 🔄 SUP |
| **lif-ounion** | ounion & uis | ~150 | 🔄 SUP |  
| **lif-os-xpls** | o ppliions & xpls | ~100 | 🔄 SUP |
| **lif-pins-in** | in & pins | ~200 | 🔄 SUP |
| **lif-hiv-vlopn** | Hisoil & ly fils | ~500+ | 📦 HIV |

## 🚀 Qui S

```bash
# lon h o posioy
i lon hps://ihub.o/SiLIF/lif-plfo-o.i
 lif-plfo-o

# Insll pnnis
pip insll - quins.x

# un h plfo
pyhon lnivployn.py
```

## 🧠 o oponns

- **loih**: `xpinP2L.I.F.-Lnin...py` - in nul possin loih
- **Plfo**: `lifhoyplfosv.py` - o plfo sv
- **onfiuion**: `zuonfi.py` - ssnil zu onfiuion
- **Inf**: `LIFLINILPLFOBI.hl` - Piy linil inf

## 🔗 l posiois

- [zu Infsuu](hps://ihub.o/SiLIF/lif-zu-infsuu) - opl ployn sup
- [ounion](hps://ihub.o/SiLIF/lif-ounion) - ophnsiv uis  
- [o ppliions](hps://ihub.o/SiLIF/lif-os-xpls) - Woin xpls
- [in pins](hps://ihub.o/SiLIF/lif-pins-in) - uo ouh

## 📊 Sys Sus

- **o Plfo**: ✅ Opionl
- **zu pl**: ✅ Liv (Off I: `960096-f1-420b-902-042561b`)
- **Pouion y**: ✅ Spb 27, 2025
- **posioy Suu**: 🔄 suuin Novb 2025

## 🎯 iion Bnfis

✅ **Ipov Pfon**: Fs lonin n nviion  
✅ **B Onizion**: Fous posiois by pupos  
✅ **si innn**:  ups n onibuions  
✅ **iHub opibiliy**: No o fil union wnins  
✅ ** ollboion**: l ownship n sponsibiliy  

---

**opyih 2025** - Sio Py Boull | L.I.F. Plfo Pouion Sys
"""
        un onn
    
    f posioysupsips(slf):
        """ sips o s up h nw posioy suu"""
        
        # in sup sip
        supsip = '''#!/bin/bsh
# L.I.F. Plfo posioy suuin Sup
# un his sip o  h nw posioy suu

ho "🚀 Sin up L.I.F. Plfo posioy Suu..."

#  iois fo h nw posioy
i -p ../lif-plfo-o
i -p ../lif-zu-infsuu  
i -p ../lif-ounion
i -p ../lif-os-xpls
i -p ../lif-pins-in
i -p ../lif-hiv-vlopn

ho "✅ ioy suu "
ho "📋 Nx sps:"
ho "1. un: pyhon POSIOYSUUINPLN.py"
ho "2. viw h n iion pln"
ho "3. xu h iion sips"
ho "4. Iniiliz i posiois fo h oponn"

ho "🎯 his will u h in posioy fo 1,257+ fils o ~50 o fils"
'''
        
        un supsip
    
    f xunlysis(slf):
        """xu h opl nlysis n n pos"""
        pin("🎯 Sin L.I.F. Plfo posioy suuin nlysis...")
        pin("=" * 70)
        
        # un nlysis
        slf.nlyzposioy()
        slf.oposioysuu()
        slf.ssinfilsoposiois()
        slf.iionpln()
        
        # n pos
        slf.svnlysispo()
        slf.svfilliss()
        slf.nsupinsuions()
        
        pin("=" * 70)
        pin("✅ nlysis opl!")
        pin(f"📊 ol fils nlyz: {slf.nlysispo['olfils']}")
        pin("📂 posioy bown:")
        
        fo pon, poinfo in slf.nwpos.is():
            filoun = ln(poinfo['fils'])
            sus = "🟢" if filoun <= poinfo['xfils'] ls "🔴"
            pin(f"   {sus} {pon}: {filoun} fils (x: {poinfo['xfils']})")
        
        pin("\n🎯 on ion:")
        pin("1. viw h n pos")
        pin("2. xu h iion pln")  
        pin("3.  fous posiois")
        pin("4. Up ounion n fns")
        
        un slf.nlysispo
    
    f svnlysispo(slf):
        """Sv h opl nlysis po"""
        pofil = slf.bsph / "POSIOYNLYSISPO.json"
        wih opn(pofil, 'w', noin='uf-8') s f:
            json.up(slf.nlysispo, f, inn=2, nsusii=Fls)
        pin(f"📄 nlysis po sv: {pofil}")
    
    f svfilliss(slf):
        """Sv il fil liss fo h posioy"""
        fo pon, poinfo in slf.nwpos.is():
            lisfil = slf.bsph / f"{pon.upp()}FILLIS.x"
            wih opn(lisfil, 'w', noin='uf-8') s f:
                f.wi(f"# {pon.upp()} - Fil Lis\n")
                f.wi(f"# {poinfo['sipion']}\n")
                f.wi(f"# Pioiy: {poinfo['pioiy']}\n")
                f.wi(f"# Fil oun: {ln(poinfo['fils'])}\n")
                f.wi(f"# x Fils: {poinfo['xfils']}\n\n")
                
                fo filph in so(poinfo['fils']):
                    f.wi(f"{filph}\n")
            
            pin(f"📄 Fil lis sv: {lisfil}")
    
    f nsupinsuions(slf):
        """n il sup insuions"""
        insuions = """
# L.I.F. Plfo posioy suuin Insuions

## Ovviw
You posioy hs own o 1,257+ fils, usin iHub o un lisins.
his suuin pln splis i ino 6 fous posiois.

## Qui S (on)

1. ** o posioy Fis**:
   ```bash
   #  nw o posioy wih ssnil fils only
   i ../lif-plfo-o
   # opy ssnil fils (s LIF-PLFO-OFILLIS.x)
   ```

2. **s o Funionliy**:
   ```bash
    ../lif-plfo-o
   pyhon lnivployn.py
   ```

3. ** inin posiois**:
   ```bash
   # Follow h iion pln sp by sp
   # h posioy svs  spifi pupos
   ```

## Bnfis of suuin

✅ **Pfon**: Fs iHub opions  
✅ **ininbiliy**: Fous vlopn s  
✅ **ollboion**: l oponn ownship  
✅ **ployn**: Siplifi I/ piplins  

## posioy Puposs

- **lif-plfo-o**: ssnil loih n plfo (~50 fils)
- **lif-zu-infsuu**: ll zu ployn oponns (~100 fils)  
- **lif-ounion**: uis, nuls, n ounion (~150 fils)
- **lif-os-xpls**: o ppliions n xpls (~100 fils)
- **lif-pins-in**: in n ouh uoion (~200 fils)
- **lif-hiv-vlopn**: Hisoil n ly fils (~500+ fils)

## Iplnion ilin

- **Phs 1**: o posioy (II)
- **Phs 2**: zu infsuu (HIH PIOIY)  
- **Phs 3**: ounion (IU PIOIY)
- **Phs 4**: os n xpls (IU PIOIY)
- **Phs 5**: in pins (LOW PIOIY)
- **Phs 6**: hiv ly fils (INNN)

"""
        
        insuionsfil = slf.bsph / "SUUININSUIONS."
        wih opn(insuionsfil, 'w', noin='uf-8') s f:
            f.wi(insuions)
        
        pin(f"📋 Sup insuions sv: {insuionsfil}")

f in():
    """in xuion funion"""
    bsph = os.w()
    suu = posioysuu(bsph)
    
    y:
        nlysispo = suu.xunlysis()
        un nlysispo
    xp xpion s :
        pin(f"❌ o uin nlysis: {s()}")
        un Non

if n == "in":
    pin("🎯 L.I.F. Plfo posioy suuin Sys")
    pin("=" * 60)
    
    sul = in()
    
    if sul:
        pin("\n🎉 posioy suuin nlysis opl sussfully!")
        pin("\n📋 Nx Sps:")
        pin("1. viw POSIOYNLYSISPO.json")
        pin("2. h iniviul fil liss (*FILLIS.x)")
        pin("3.  SUUININSUIONS.")
        pin("4. Bin wih in h o posioy")
        
        pin(f"\n🎯 his will u you in posioy fo 1,257+ fils o ~50 ssnil fils!")
    ls:
        pin("\n❌ nlysis fil. Pls h h o sss bov.")        pin("\n❌ nlysis fil. Pls h h o sss bov.")