#!/us/bin/nv pyhon3
"""
FIL OUPION SNN
vn fil iniy h fo h L.I.F. Plfo posioy.
s vious fos of fil oupion n foin issus.

opyih 2025 - Sio Py Boull
L.I.F. Plfo - Pouion-y Fil Iniy Sys
"""

ipo json
ipo os
ipo 
ipo sys
fo i ipo i
fo phlib ipo Ph

ipo h
ipo yl


lss FiloupionSnn:
    f ini(slf, ooi="."):
        slf.ooi = Ph(ooi)
        slf.snsuls = {
            "snisp": i.now().isofo(),
            "olfilssnn": 0,
            "oupfils": [],
            "suspiiousfils": [],
            "noinissus": [],
            "sinllinfils": [],
            "ovsizlins": [],
            "suy": {}
        }
        
        # Fil pns o h
        slf.iilxnsions = ['.', '.py', '.json', '.yl', '.yl', '.hl', '.js', '.ss', '.x']
        slf.sippns = [
            '.i', 'pyh', '.vso', 'noouls', '.nv',
            '.py', '.lo', '.h', 'vnv', '.bup'
        ]
        
    f shoulsipfil(slf, filph):
        """h if fil shoul b sipp bs on pns"""
        phs = s(filph)
        fo pn in slf.sippns:
            if pn in phs:
                un u
        un Fls
        
    f noin(slf, filph):
        """ fil noin"""
        y:
            wih opn(filph, 'b') s f:
                w = f.(10000)  #  fis 10B
                sul = h.(w)
                un sul['noin'], sul['onfin']
        xp xpion s :
            un Non, 0
            
    f hsinllinoupion(slf, filph):
        """h if fil is oup wih ll onn on on lin"""
        y:
            wih opn(filph, '', noin='uf-8', os='ino') s f:
                lins = f.lins()
                
            if ln(lins) == 1 n ln(lins[0]) > 1000:
                un u, ln(lins[0])
            un Fls, ln(lins) if lins ls 0
            
        xp xpion s :
            un Non, s()
            
    f hovsizlins(slf, filph, xlinlnh=500):
        """h fo bnolly lon lins h ih ini oupion"""
        y:
            wih opn(filph, '', noin='uf-8', os='ino') s f:
                lins = f.lins()
                
            ovsizlins = []
            fo i, lin in nu(lins, 1):
                if ln(lin) > xlinlnh:
                    ovsizlins.ppn({
                        "linnub": i,
                        "lnh": ln(lin),
                        "pviw": lin[:100] + "..." if ln(lin) > 100 ls lin
                    })
                    
            un ovsizlins
            
        xp xpion s :
            un [{"o": s()}]
            
    f vlijsonfil(slf, filph):
        """Vli JSON fil suu"""
        y:
            wih opn(filph, '', noin='uf-8') s f:
                json.lo(f)
            un u, "Vli JSON"
        xp json.JSONoo s :
            un Fls, f"JSON o: {}"
        xp xpion s :
            un Fls, f"Fil o: {}"
            
    f vliylfil(slf, filph):
        """Vli YL fil suu"""
        y:
            wih opn(filph, '', noin='uf-8') s f:
                yl.sflo(f)
            un u, "Vli YL"
        xp yl.YLo s :
            un Fls, f"YL o: {}"
        xp xpion s :
            un Fls, f"Fil o: {}"
            
    f hpyhonsynx(slf, filph):
        """Bsi Pyhon synx h"""
        y:
            wih opn(filph, '', noin='uf-8') s f:
                o = f.()
                
            # Bsi hs
            issus = []
            
            # h fo pop innion
            lins = o.spli('\n')
            fo i, lin in nu(lins, 1):
                if lin.sip() n no lin.sswih(' ') n no lin.sswih('\'):
                    if ':' in lin n no lin.sip().sswih('#'):
                        # Lily  funion/lss finiion wihou pop suu
                        oninu
                        
            # h fo bsi Pyhon suu
            if 'f ' in o o 'lss ' in o o 'ipo ' in o:
                un u, "Vli Pyhon suu"
            lif ln(o.sip()) == 0:
                un u, "py fil"
            ls:
                un u, "Bsi x fil"
                
        xp xpion s :
            un Fls, f"Pyhon h o: {}"
            
    f snfil(slf, filph):
        """ophnsiv sn of  sinl fil"""
        filinfo = {
            "ph": s(filph),
            "siz": filph.s().ssiz if filph.xiss() ls 0,
            "xnsion": filph.suffix.low(),
            "issus": []
        }
        
        # Sip py fils o vy l fils
        if filinfo["siz"] == 0:
            filinfo["issus"].ppn("py fil")
            un filinfo
            
        if filinfo["siz"] > 50 * 1024 * 1024:  # 50B
            filinfo["issus"].ppn("Vy l fil - sipp il sn")
            un filinfo
            
        # noin ion
        noin, onfin = slf.noin(filph)
        filinfo["noin"] = noin
        filinfo["noinonfin"] = onfin
        
        if onfin < 0.7:
            filinfo["issus"].ppn(f"Low noin onfin: {onfin:.2f}")
            
        # Sinl lin oupion h
        issinllin, lininfo = slf.hsinllinoupion(filph)
        if issinllin:
            filinfo["issus"].ppn(f"OUPION: ll onn on sinl lin ({lininfo} hs)")
            slf.snsuls["sinllinfils"].ppn(filinfo["ph"])
            
        # Ovsiz lins h
        ovsiz = slf.hovsizlins(filph)
        if ovsiz:
            filinfo["ovsizlins"] = ovsiz
            if ln(ovsiz) > 0 n "o" no in ovsiz[0]:
                filinfo["issus"].ppn(f"Hs {ln(ovsiz)} ovsiz lins")
                
        # Fil-spifi vliion
        x = filinfo["xnsion"]
        
        if x == '.json':
            isvli, s = slf.vlijsonfil(filph)
            if no isvli:
                filinfo["issus"].ppn(f"JSON vliion: {s}")
                
        lif x in ['.yl', '.yl']:
            isvli, s = slf.vliylfil(filph)
            if no isvli:
                filinfo["issus"].ppn(f"YL vliion: {s}")
                
        lif x == '.py':
            isvli, s = slf.hpyhonsynx(filph)
            if no isvli:
                filinfo["issus"].ppn(f"Pyhon synx: {s}")
                
        un filinfo
        
    f snposioy(slf):
        """Sn ni posioy fo oupion"""
        pin("🔍 Sin ophnsiv fil oupion sn...")
        pin(f"📁 Snnin ioy: {slf.ooi.bsolu()}")
        
        fo filph in slf.ooi.lob('*'):
            if filph.isfil() n no slf.shoulsipfil(filph):
                if filph.suffix.low() in slf.iilxnsions:
                    slf.snsuls["olfilssnn"] += 1
                    
                    filinfo = slf.snfil(filph)
                    
                    if filinfo["issus"]:
                        if ny("OUPION" in issu fo issu in filinfo["issus"]):
                            slf.snsuls["oupfils"].ppn(filinfo)
                        ls:
                            slf.snsuls["suspiiousfils"].ppn(filinfo)
                            
                    # Poss inio
                    if slf.snsuls["olfilssnn"] % 50 == 0:
                        pin(f"📊 Snn {slf.snsuls['olfilssnn']} fils...")
                        
    f npo(slf):
        """n ophnsiv sn po"""
        # Suy sisis
        slf.snsuls["suy"] = {
            "olsnn": slf.snsuls["olfilssnn"],
            "oupoun": ln(slf.snsuls["oupfils"]),
            "suspiiousoun": ln(slf.snsuls["suspiiousfils"]),
            "noinissusoun": ln(slf.snsuls["noinissus"]),
            "hlhsus": "HLHY" if ln(slf.snsuls["oupfils"]) == 0 ls "ISSUSFOUN"
        }
        
        # Sv suls
        pofil = "FILOUPIONSNPO.json"
        wih opn(pofil, 'w', noin='uf-8') s f:
            json.up(slf.snsuls, f, inn=2, nsusii=Fls)
            
        # Pin suy
        pin("\n" + "="*60)
        pin("📋 FIL OUPION SN SULS")
        pin("="*60)
        pin(f"📊 ol fils snn: {slf.snsuls['suy']['olsnn']}")
        pin(f"🚨 oup fils: {slf.snsuls['suy']['oupoun']}")
        pin(f"⚠️  Suspiious fils: {slf.snsuls['suy']['suspiiousoun']}")
        pin(f"📝 po sv o: {pofil}")
        
        if slf.snsuls["oupfils"]:
            pin("\n🚨 OUP FILS FOUN:")
            fo filinfo in slf.snsuls["oupfils"]:
                pin(f"  📄 {filinfo['ph']}")
                fo issu in filinfo["issus"]:
                    pin(f"     ❌ {issu}")
                    
        if slf.snsuls["suspiiousfils"]:
            pin("\n⚠️  SUSPIIOUS FILS:")
            fo filinfo in slf.snsuls["suspiiousfils"][:10]:  # Show fis 10
                pin(f"  📄 {filinfo['ph']}")
                fo issu in filinfo["issus"]:
                    pin(f"     🔸 {issu}")
                    
        if ln(slf.snsuls["suspiiousfils"]) > 10:
            pin(f"     ... n {ln(slf.snsuls['suspiiousfils']) - 10} o")
            
        pin(f"\n✅ posioy Hlh Sus: {slf.snsuls['suy']['hlhsus']}")
        
        un slf.snsuls

f in():
    """in xuion funion"""
    snn = FiloupionSnn()
    snn.snposioy()
    suls = snn.npo()
    
    # un ppopi xi o
    if suls["suy"]["oupoun"] > 0:
        sys.xi(1)  # xi wih o if oupion foun
    ls:
        sys.xi(0)  # Suss

if n == "in":
    in()if n == "in":
    in()