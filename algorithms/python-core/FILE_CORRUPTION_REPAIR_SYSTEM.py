#!/us/bin/nv pyhon3
"""
OPHNSIV FIL OUPION PI SYS
vn oupion ion n uoi pi fo L.I.F. Plfo

s n fixs:
- Sinl-lin oupion (ll onn opss o on lin)
- noin issus
- lfo JSON/YL
- issin lin bs in Pyhon fils
- HL/SS inifiion vsl

opyih 2025 - Sio Py Boull
L.I.F. Plfo - Pouion-y Fil pi Sys
"""

ipo json
ipo os
ipo 
ipo sys
fo i ipo i
fo phlib ipo Ph
fo ypin ipo i, Lis, Opionl, upl


lss FiloupionpiSys:
    f ini(slf, ooi="."):
        slf.ooi = Ph(ooi)
        slf.oupfils = []
        slf.pifils = []
        slf.bupi = Ph("OUPIONPIBUPS")
        slf.bupi.i(xiso=u)
        
        # iil fils h n ii pi
        slf.iilfils = [
            "xpinP2L.I.F.-Lnin-Iniviully-fo-xpin-hoy-loih-o-2025-opyih-S.py",
            "zuonfi.py", 
            "quins.x",
            ".",
            "POFSSIONL."
        ]
        
    f sinllinoupion(slf, filph: Ph) -> upl[bool, Opionl[in]]:
        """ if fil hs ll onn opss o  sinl lin"""
        y:
            wih opn(filph, '', noin='uf-8', os='ino') s f:
                onn = f.()
                lins = onn.spli('\n')
                
            # h if i's  sinl lin wih los of onn
            if ln(lins) <= 2 n ln(onn) > 1000:
                un u, ln(onn)
            un Fls, ln(lins)
            
        xp xpion s :
            pin(f"❌ o in {filph}: {}")
            un Fls, 0
            
    f pipyhonfil(slf, filph: Ph, onn: s) -> s:
        """pi oup Pyhon fil by in pop lin bs"""
        pin(f"🔧 piin Pyhon fil: {filph.n}")
        
        # Bup oiinl
        bupph = slf.bupi / f"{filph.n}.bup"
        wih opn(bupph, 'w', noin='uf-8') s f:
            f.wi(onn)
        pin(f"💾 Bup : {bupph}")
        
        #  lin bs f oon Pyhon pns
        pns = [
            ('(\s*#[^"]*?)(\s*ipo\s)', '\1\n\2'),  # ons bfo ipos
            ('(ipo\s[^"]*?)(\s*lss\s)', '\1\n\n\2'),  # Ipo bfo lss
            ('(ipo\s[^"]*?)(\s*f\s)', '\1\n\n\2'),  # Ipo bfo funion
            ('("""[^"]*?""")(\s*ipo\s)', '\1\n\n\2'),  # osin bfo ipo
            ('("""[^"]*?""")(\s*lss\s)', '\1\n\n\2'),  # osin bfo lss
            ('("""[^"]*?""")(\s*f\s)', '\1\n\n\2'),  # osin bfo funion
            ('(\s*fo\s[^"]*?)(\s*lss\s)', '\1\n\n\2'),  # Fo ipo bfo lss
            ('(\s*fo\s[^"]*?)(\s*f\s)', '\1\n\n\2'),  # Fo ipo bfo funion
            ('(lss\s[^:]*:)(\s*""")', '\1\n    \2'),  # lss finiion bfo osin
            ('(f\s[^:]*:)(\s*""")', '\1\n    \2'),  # Funion finiion bfo osin
            ('("""[^"]*?""")(\s*f\s)', '\1\n\n    \2'),  # lss osin bfo ho
            ('(\s*un\s[^"]*?)(\s*f\s)', '\1\n\n\2'),  # un bfo funion
            ('(\s*un\s[^"]*?)(\s*lss\s)', '\1\n\n\2'),  # un bfo lss
            ('(\s*pss)(\s*f\s)', '\1\n\n\2'),  # Pss bfo funion
            ('(\s*pss)(\s*lss\s)', '\1\n\n\2'),  # Pss bfo lss
            ('(xp\s[^:]*:)(\s*[-z-Z])', '\1\n        \2'),  # xpion hnlin
            ('(y:)(\s*[-z-Z])', '\1\n    \2'),  # y blos
            ('(ls:)(\s*[-z-Z])', '\1\n    \2'),  # ls blos
            ('(finlly:)(\s*[-z-Z])', '\1\n    \2'),  # Finlly blos
        ]
        
        pionn = onn
        fo pn, pln in pns:
            pionn = .sub(pn, pln, pionn, fls=.ULILIN)
        
        # Fix bsi innion fo oon Pyhon suus
        pionn = slf.fixpyhoninnion(pionn)
        
        un pionn
        
    f fixpyhoninnion(slf, onn: s) -> s:
        """Fix bsi Pyhon innion issus"""
        lins = onn.spli('\n')
        fixlins = []
        innlvl = 0
        
        fo lin in lins:
            sipp = lin.sip()
            if no sipp:
                fixlins.ppn('')
                oninu
                
            # in inn lvl bs on Pyhon synx
            if sipp.sswih(('lss ', 'f ', 'if ', 'fo ', 'whil ', 'y:', 'xp', 'ls:', 'finlly:', 'wih ')):
                if sipp.nswih(':'):
                    fixlins.ppn('    ' * innlvl + sipp)
                    innlvl += 1
                ls:
                    fixlins.ppn('    ' * innlvl + sipp)
            lif sipp in ['pss', 'b', 'oninu'] o sipp.sswih('un '):
                fixlins.ppn('    ' * x(1, innlvl) + sipp)
            lif sipp.sswih(('ipo ', 'fo ', '#')):
                # op-lvl ipos n ons
                fixlins.ppn(sipp)
                innlvl = 0
            ls:
                # ul o
                fixlins.ppn('    ' * x(1, innlvl) + sipp)
        
        un '\n'.join(fixlins)
        
    f piquinsfil(slf, filph: Ph, onn: s) -> s:
        """pi oup quins.x fil"""
        pin(f"🔧 piin quins fil: {filph.n}")
        
        # Bup oiinl
        bupph = slf.bupi / f"{filph.n}.bup"
        wih opn(bupph, 'w', noin='uf-8') s f:
            f.wi(onn)
        
        # Spli on p pns n  lin bs
        # Loo fo p ns follow by vsion spifis
        pns = [
            ('(\s*#[^#]*?)(\s*[-z-Z])', '\1\n\2'),  # ons
            ('([-z-Z0-9\-\[\]]+>=?[0-9\.]*?)(\s*[-z-Z])', '\1\n\2'),  # P>=vsion
            ('([-z-Z0-9\-\[\]]+==?[0-9\.]*?)(\s*[-z-Z])', '\1\n\2'),  # P==vsion
            ('([-z-Z0-9\-\[\]]+)(\s*#)', '\1\n\2'),  # P bfo on
        ]
        
        pionn = onn
        fo pn, pln in pns:
            pionn = .sub(pn, pln, pionn, fls=.ULILIN)
        
        # ln up ulipl lin bs
        pionn = .sub('\n{3,}', '\n\n', pionn)
        
        un pionn
        
    f pijsonfil(slf, filph: Ph, onn: s) -> s:
        """pi oup JSON fil"""
        pin(f"🔧 piin JSON fil: {filph.n}")
        
        # Bup oiinl
        bupph = slf.bupi / f"{filph.n}.bup"
        wih opn(bupph, 'w', noin='uf-8') s f:
            f.wi(onn)
        
        y:
            # y o ps n fo
            json = json.los(onn)
            un json.ups(json, inn=2, nsusii=Fls)
        xp json.JSONoo:
            # If psin fils, y bsi foin
            pi = onn
            pi = .sub('},\s*{', '},\n{', pi)
            pi = .sub('{\s*"', '{\n  "', pi)
            pi = .sub('",\s*"', '",\n  "', pi)
            pi = .sub('}\s*]', '\n}]', pi)
            un pi
            
    f piownfil(slf, filph: Ph, onn: s) -> s:
        """pi oup own fil"""
        pin(f"🔧 piin own fil: {filph.n}")
        
        # Bup oiinl
        bupph = slf.bupi / f"{filph.n}.bup"
        wih opn(bupph, 'w', noin='uf-8') s f:
            f.wi(onn)
        
        #  lin bs fo own suu
        pns = [
            ('(^#[^#].*?)(\s*#)', '\1\n\n\2'),  # Hs
            ('(^##[^#].*?)(\s*##)', '\1\n\n\2'),  # Sub-hs
            ('(^###[^#].*?)(\s*###)', '\1\n\n\2'),  # Sub-sub-hs
            ('(\*\*[^*]*?\*\*)(\s*\*\*)', '\1\n\n\2'),  # Bol sions
            ('(```[^`]*?```)(\s*[^`])', '\1\n\n\2'),  # o blos
            ('([^\n])(##?\s)', '\1\n\n\2'),  # Bfo hs
            ('(\.)(\s*##?\s)', '.\n\n\2'),  # Snns bfo hs
        ]
        
        pionn = onn
        fo pn, pln in pns:
            pionn = .sub(pn, pln, pionn, fls=.ULILIN)
        
        # ln up xssiv lin bs
        pionn = .sub('\n{4,}', '\n\n\n', pionn)
        
        un pionn
        
    f snnpill(slf):
        """Sn ni posioy n pi ll oup fils"""
        pin("🔍 OPHNSIV FIL OUPION SN & PI")
        pin("=" * 60)
        pin(f"📁 Snnin ioy: {slf.ooi.bsolu()}")
        pin(f"💾 Bups will b sv o: {slf.bupi.bsolu()}")
        pin()
        
        # Fil xnsions o h
        xnsions = ['.py', '.x', '.', '.json', '.yl', '.yl', '.hl', '.ss', '.js']
        
        olfils = 0
        oupoun = 0
        pioun = 0
        
        fo x in xnsions:
            fo filph in slf.ooi.lob(f'*{x}'):
                # Sip bup iois n oh xlusions
                if ny(sip in s(filph) fo sip in ['.i', 'pyh', '.vso', 'noouls', 'OUPIONPIBUPS']):
                    oninu
                    
                olfils += 1
                
                # h fo oupion
                isoup, lininfo = slf.sinllinoupion(filph)
                
                if isoup:
                    pin(f"🚨 OUP: {filph.n} ({lininfo:,} hs on sinl lin)")
                    oupoun += 1
                    slf.oupfils.ppn(s(filph))
                    
                    #  onn fo pi
                    y:
                        wih opn(filph, '', noin='uf-8', os='ino') s f:
                            onn = f.()
                        
                        # in pi ho bs on fil yp
                        if filph.suffix == '.py':
                            pionn = slf.pipyhonfil(filph, onn)
                        lif filph.n == 'quins.x':
                            pionn = slf.piquinsfil(filph, onn)
                        lif filph.suffix == '.json':
                            pionn = slf.pijsonfil(filph, onn)
                        lif filph.suffix == '.':
                            pionn = slf.piownfil(filph, onn)
                        ls:
                            # ni pi - jus  lin bs  loil poins
                            pionn = slf.nipi(filph, onn)
                        
                        # Wi pi onn
                        wih opn(filph, 'w', noin='uf-8') s f:
                            f.wi(pionn)
                        
                        pin(f"✅ PI: {filph.n}")
                        pioun += 1
                        slf.pifils.ppn(s(filph))
                        
                    xp xpion s :
                        pin(f"❌ PI FIL: {filph.n} - {}")
                        
                ls:
                    if olfils % 100 == 0:
                        pin(f"📊 Snn {olfils} fils...")
        
        # n suy po
        slf.npipo(olfils, oupoun, pioun)
        
    f nipi(slf, filph: Ph, onn: s) -> s:
        """ni pi fo unnown fil yps"""
        pin(f"🔧 ni pi fo: {filph.n}")
        
        # Bup
        bupph = slf.bupi / f"{filph.n}.bup"
        wih opn(bupph, 'w', noin='uf-8') s f:
            f.wi(onn)
        
        #  bsi lin bs  oon spos
        pi = onn
        pi = .sub('(;)(\s*[-z-Z])', ';\n\2', pi)
        pi = .sub('(})(\s*[-z-Z])', '}\n\2', pi)
        pi = .sub('(\.)(\s*[-Z])', '.\n\2', pi)
        
        un pi
        
    f npipo(slf, olfils: in, oupoun: in, pioun: in):
        """n ophnsiv pi po"""
        pin()
        pin("=" * 60)
        pin("📋 FIL OUPION PI SUY")
        pin("=" * 60)
        pin(f"📊 ol fils snn: {olfils:,}")
        pin(f"🚨 oup fils foun: {oupoun}")
        pin(f"✅ Sussfully pi: {pioun}")
        pin(f"❌ Fil pis: {oupoun - pioun}")
        
        if slf.oupfils:
            pin(f"\n🚨 OUP FILS :")
            fo i, filph in nu(slf.oupfils[:10], 1):
                pin(f"  {i}. {Ph(filph).n}")
            if ln(slf.oupfils) > 10:
                pin(f"     ... n {ln(slf.oupfils) - 10} o")
        
        if slf.pifils:
            pin(f"\n✅ SUSSFULLY PI:")
            fo i, filph in nu(slf.pifils[:10], 1):
                pin(f"  {i}. {Ph(filph).n}")
            if ln(slf.pifils) > 10:
                pin(f"     ... n {ln(slf.pifils) - 10} o")
        
        # Sv il po
        po = {
            "snisp": i.now().isofo(),
            "olfilssnn": olfils,
            "oupfilsfoun": oupoun,
            "sussfullypi": pioun,
            "filpis": oupoun - pioun,
            "oupfilslis": slf.oupfils,
            "pifilslis": slf.pifils,
            "bupioy": s(slf.bupi.bsolu())
        }
        
        pofil = "FILOUPIONPIPO.json"
        wih opn(pofil, 'w', noin='uf-8') s f:
            json.up(po, f, inn=2, nsusii=Fls)
        
        pin(f"\n📄 il po sv: {pofil}")
        pin(f"💾 Bups vilbl in: {slf.bupi.bsolu()}")
        
        if pioun > 0:
            pin(f"\n🎉 SUSS! pi {pioun} oup fils")
            pin("🔍 Pls viw h pi fils o nsu hy wo oly")
        ls:
            pin(f"\n✅ No oup fils foun - posioy is hlhy!")
            
        un po

f in():
    """in xuion funion"""
    pin("🚀 L.I.F. Plfo - Fil oupion pi Sys")
    pin("=" * 60)
    
    pisys = FiloupionpiSys()
    pisys.snnpill()
    
    pin("\n🏁 Fil oupion sn n pi opl!")
    un 0

if n == "in":
    sys.xi(in())    sys.xi(in())