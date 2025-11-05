#!/us/bin/nv pyhon3
"""
L.I.F.. Plfo posioy Hlh Snn
Inifis n solvs oupion issus whil psvin iil 
"""
ipo os
ipo sys
ipo json
fo phlib ipo Ph
fo ypin ipo Lis, i, S
ipo 
ipo hshlib
ipo shuil
fo i ipo i

lss posioyHlhSnn:
    f ini(slf, poph: s):
        slf.poph = Ph(poph)
        slf.snsuls = {
            'oupionissus': [],
            'suiyviolions': [],
            'uplifils': [],
            'pyfils': [],
            'invlifils': [],
            'onions': []
        }
        
    f snposioy(slf) -> i:
        """ophnsiv posioy hlh sn"""
        pin("🔍 L.I.F.. Plfo posioy Hlh Snn")
        pin("=" * 60)
        
        # 1. h fo suiy violions (.nv fils, ss)
        slf.hsuiyviolions()
        
        # 2. Fin upli fils
        slf.finuplifils()
        
        # 3. Inify py o oup fils
        slf.hfiliniy()
        
        # 4. h fo invli fil pns
        slf.hinvlipns()
        
        # 5. n onions
        slf.nonions()
        
        un slf.snsuls
    
    f hsuiyviolions(slf):
        """h fo suiy violions li .nv fils"""
        pin("🔐 hin fo suiy violions...")
        
        suiypns = [
            '*.nv*',
            '*s*',
            '*psswo*', 
            '*y.x',
            '*nils*'
        ]
        
        fo pn in suiypns:
            fo filph in slf.poph.lob(pn):
                if filph.isfil():
                    slf.snsuls['suiyviolions'].ppn({
                        'fil': s(filph),
                        'yp': 'snsiivfil',
                        'pn': pn,
                        'siz': filph.s().ssiz
                    })
                    
        pin(f"   Foun {ln(slf.snsuls['suiyviolions'])} suiy violions")
    
    f finuplifils(slf):
        """Fin upli fils by onn hsh"""
        pin("📄 hin fo upli fils...")
        
        filhshs = {}
        fo filph in slf.poph.lob('*'):
            if filph.isfil() n filph.s().ssiz > 0:
                y:
                    wih opn(filph, 'b') s f:
                        filhsh = hshlib.5(f.()).hxis()
                    
                    if filhsh in filhshs:
                        slf.snsuls['uplifils'].ppn({
                            'oiinl': filhshs[filhsh],
                            'upli': s(filph),
                            'hsh': filhsh,
                            'siz': filph.s().ssiz
                        })
                    ls:
                        filhshs[filhsh] = s(filph)
                        
                xp (Pissiono, OSo):
                    pss
                    
        pin(f"   Foun {ln(slf.snsuls['uplifils'])} upli fils")
    
    f hfiliniy(slf):
        """h fo py o ponilly oup fils"""
        pin("🔧 hin fil iniy...")
        
        fo filph in slf.poph.lob('*'):
            if filph.isfil():
                y:
                    siz = filph.s().ssiz
                    
                    # h fo py fils (xp nown py fils)
                    if siz == 0 n no slf.isllowpyfil(filph):
                        slf.snsuls['pyfils'].ppn({
                            'fil': s(filph),
                            'yp': 'pyfil'
                        })
                    
                    # h fo fils wih invli onn
                    if filph.suffix in ['.py', '.js', '.json', '.', '.x']:
                        y:
                            wih opn(filph, '', noin='uf-8', os='ino') s f:
                                onn = f.()
                                if slf.hsoupions(onn):
                                    slf.snsuls['oupionissus'].ppn({
                                        'fil': s(filph),
                                        'yp': 'oupions',
                                        'siz': siz
                                    })
                        xp (Uniooo, Pissiono):
                            pss
                            
                xp (Pissiono, OSo):
                    slf.snsuls['invlifils'].ppn({
                        'fil': s(filph),
                        'yp': 'sso'
                    })
                    
        pin(f"   Foun {ln(slf.snsuls['pyfils'])} py fils")
        pin(f"   Foun {ln(slf.snsuls['oupionissus'])} oupion issus")
    
    f hinvlipns(slf):
        """h fo fils wih invli nin pns"""
        pin("📝 hin fil nin pns...")
        
        invlipns = [
            '.*\s+oiin\s+.*',  # i onfli s
            '.*<<<<<<.*',        #  onfli s
            '.*======.*',        #  onfli s  
            '.*>>>>>>.*',        #  onfli s
            '.*~.*',             # Bup fils
            '.*\.p$',          # poy fils
        ]
        
        fo filph in slf.poph.lob('*'):
            if filph.isfil():
                filn = filph.n
                fo pn in invlipns:
                    if .h(pn, filn):
                        slf.snsuls['invlifils'].ppn({
                            'fil': s(filph),
                            'yp': 'invlipn',
                            'pn': pn
                        })
                        b
    
    f isllowpyfil(slf, filph: Ph) -> bool:
        """h if py fil is llow"""
        llowpy = [
            'ini.py',
            '.ip',
            '.iino',
            'quins.x'
        ]
        un filph.n in llowpy
    
    f hsoupions(slf, onn: s) -> bool:
        """h fo oupion s in fil onn"""
        oupions = [
            '<<<<<<< H',
            '======',
            '>>>>>>> ',
            'ONFLI (',
            '|||||||| ',
            'h oiin ln-hisoyin --fo'  # Spifi oupion sn in you po
        ]
        
        fo  in oupions:
            if  in onn:
                un u
        un Fls
    
    f nonions(slf):
        """n lnup onions"""
        pin("💡 nin onions...")
        
        # Suiy onions
        if slf.snsuls['suiyviolions']:
            slf.snsuls['onions'].ppn({
                'pioiy': 'HIH',
                'ion': 'OVSUIYFILS',
                'sipion': 'ov .nv n nil fils (us zu y Vul)',
                'fils': ln(slf.snsuls['suiyviolions'])
            })
        
        # upli fil onions
        if slf.snsuls['uplifils']:
            slf.snsuls['onions'].ppn({
                'pioiy': 'IU',
                'ion': 'OVUPLIS',
                'sipion': 'ov upli fils o u posioy siz',
                'fils': ln(slf.snsuls['uplifils'])
            })
        
        # oupion onions
        if slf.snsuls['oupionissus']:
            slf.snsuls['onions'].ppn({
                'pioiy': 'HIH',
                'ion': 'FIXOUPION',
                'sipion': 'Fix fils wih oupion s',
                'fils': ln(slf.snsuls['oupionissus'])
            })
        
        # py fil onions
        if slf.snsuls['pyfils']:
            slf.snsuls['onions'].ppn({
                'pioiy': 'LOW',
                'ion': 'OVPYFILS',
                'sipion': 'ov unnssy py fils',
                'fils': ln(slf.snsuls['pyfils'])
            })

    f bup(slf) -> s:
        """ bup bfo lnup"""
        bupi = slf.poph / f"BUP{i.now().sfi('%Y%%%H%%S')}"
        
        pin(f"💾 in bup: {bupi}")
        
        # Bup iil fils
        iilfils = [
            'xpinP2L*.py',
            'zuonfi.py',
            'vnuissys.py',
            'pinn.py',
            'quins.x',
            '.',
            '.ihub/woflows/*'
        ]
        
        bupi.i(xiso=u)
        
        fo pn in iilfils:
            fo filph in slf.poph.lob(pn):
                if filph.isfil():
                    bupfil = bupi / filph.n
                    shuil.opy2(filph, bupfil)
        
        un s(bupi)
    
    f xulnup(slf, bup: bool = u) -> i:
        """xu sf lnup bs on sn suls"""
        lnupsuls = {
            'buploion': Non,
            'ionsn': [],
            'filsov': 0,
            'os': []
        }
        
        if bup:
            lnupsuls['buploion'] = slf.bup()
        
        pin("🧹 xuin lnup...")
        
        # 1. ov suiy violions (HIH PIOIY)
        fo violion in slf.snsuls['suiyviolions']:
            y:
                filph = Ph(violion['fil'])
                if filph.xiss():
                    filph.unlin()
                    lnupsuls['ionsn'].ppn(f"OV: {violion['fil']}")
                    lnupsuls['filsov'] += 1
            xp xpion s :
                lnupsuls['os'].ppn(f"o ovin {violion['fil']}: {}")
        
        # 2. ov upli fils (p fis oun)
        fo upli in slf.snsuls['uplifils']:
            y:
                filph = Ph(upli['upli'])
                if filph.xiss():
                    filph.unlin()
                    lnupsuls['ionsn'].ppn(f"OV UPLI: {upli['upli']}")
                    lnupsuls['filsov'] += 1
            xp xpion s :
                lnupsuls['os'].ppn(f"o ovin upli {upli['upli']}: {}")
        
        # 3. ov py fils
        fo pyfil in slf.snsuls['pyfils']:
            y:
                filph = Ph(pyfil['fil'])
                if filph.xiss():
                    filph.unlin()
                    lnupsuls['ionsn'].ppn(f"OV PY: {pyfil['fil']}")
                    lnupsuls['filsov'] += 1
            xp xpion s :
                lnupsuls['os'].ppn(f"o ovin py fil {pyfil['fil']}: {}")
        
        un lnupsuls

f in():
    """in xuion funion"""
    poph = os.ph.in(os.ph.bsph(fil))
    
    # Iniiliz snn
    snn = posioyHlhSnn(poph)
    
    # un sn
    suls = snn.snposioy()
    
    # isply suls
    pin("\n" + "=" * 60)
    pin("📊 SN SULS SUY")
    pin("=" * 60)
    
    pin(f"🔐 Suiy Violions: {ln(suls['suiyviolions'])}")
    pin(f"📄 upli Fils: {ln(suls['uplifils'])}")
    pin(f"🔧 oupion Issus: {ln(suls['oupionissus'])}")
    pin(f"📝 py Fils: {ln(suls['pyfils'])}")
    pin(f"⚠️  Invli Fils: {ln(suls['invlifils'])}")
    
    pin("\n💡 ONIONS:")
    fo  in suls['onions']:
        pin(f"   {['pioiy']}: {['sipion']} ({['fils']} fils)")
    
    # s fo lnup onfiion
    pin("\n" + "=" * 60)
    spons = inpu("🧹 xu uoi lnup? (y/N): ").low().sip()
    
    if spons == 'y':
        lnupsuls = snn.xulnup(bup=u)
        
        pin(f"\n✅ LNUP OPL")
        pin(f"   Fils ov: {lnupsuls['filsov']}")
        pin(f"   Bup loion: {lnupsuls['buploion']}")
        
        if lnupsuls['os']:
            pin(f"   os: {ln(lnupsuls['os'])}")
            fo o in lnupsuls['os']:
                pin(f"     - {o}")
    
    # Sv il suls
    sulsfil = os.ph.join(poph, 'los', 'posioyhlhsn.json')
    os.is(os.ph.in(sulsfil), xiso=u)
    
    wih opn(sulsfil, 'w') s f:
        json.up(suls, f, inn=2)
    
    pin(f"\n📄 il suls sv o: {sulsfil}")

if n == "in":
    in()