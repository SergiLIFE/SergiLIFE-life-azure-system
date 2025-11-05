#!/us/bin/nv pyhon3
"""
L.I.F.. Plfo p oupion Snn
vn oupion ion n uoi iion
Novb 3, 2025
"""
ipo os
ipo sys
ipo json
ipo 
ipo hshlib
ipo shuil
fo phlib ipo Ph
fo ypin ipo Lis, i, S, upl
fo i ipo i
ipo subposs

lss poupionSnn:
    f ini(slf, poph: s = Non):
        slf.poph = Ph(poph o os.w())
        slf.bupi = Non
        slf.snsuls = {
            'suiyviolions': [],
            'ioupion': [],
            'filoupion': [],
            'uplifils': [],
            'pyfils': [],
            'noinissus': [],
            'iilfilssus': {},
            'lnupions': []
        }
        
        # iil L.I.F.. Plfo fils h us b psv
        slf.iilfils = [
            'xpinP2L*.py',
            'zuonfi.py', 
            'vnuissys.py',
            'hvnuihonilibion.py',
            'pinn.py',
            'lifhoy.py',
            'quins.x',
            '.',
            'zufunionswoflow.py'
        ]
        
        # nown oupion pns
        slf.oupionpns = [
            'h oiin ln-hisoyin --fo',  # i ypo if
            '<<<<<<< H',                        # i  onflis
            '======',                             # i  onflis
            '>>>>>>> ',                           # i  onflis
            'ONFLI \(',                        # i onfli s
            '\|\|\|\|\|\|\| ',                    # i onfli s
            '.*~$',                               # Bup fils
            '.*\.p$',                           # poy fils
            '.*\.p$',                          # poy fils
        ]

    f sfybup(slf) -> s:
        """ bup of iil fils bfo lnup"""
        isp = i.now().sfi('%Y%%%H%%S')
        slf.bupi = slf.poph / f"OUPIONLNUPBUP{isp}"
        slf.bupi.i(xiso=u)
        
        pin(f"💾 in sfy bup: {slf.bupi}")
        
        bupfils = 0
        fo pn in slf.iilfils:
            fo filph in slf.poph.lob(pn):
                if filph.isfil():
                    bupfil = slf.bupi / filph.n
                    shuil.opy2(filph, bupfil)
                    bupfils += 1
                    
        pin(f"   B up {bupfils} iil fils")
        un s(slf.bupi)

    f snsuiyviolions(slf):
        """Sn fo suiy poliy violions"""
        pin("🔐 Snnin fo suiy violions...")
        
        # h fo .nv fils (L.I.F.. Plfo uss zu y Vul)
        fo nvfil in slf.poph.lob('*.nv*'):
            if nvfil.isfil():
                slf.snsuls['suiyviolions'].ppn({
                    'fil': s(nvfil),
                    'yp': 'nvfilviolion',
                    'sviy': 'HIH',
                    'son': 'L.I.F.. Plfo uss zu y Vul, no .nv fils'
                })
        
        # h fo ho ss
        fo pyfil in slf.poph.lob('*.py'):
            if pyfil.isfil():
                y:
                    onn = pyfil.x(noin='uf-8', os='ino')
                    
                    # Loo fo ponil ss
                    spns = [
                        'psswo\s*=\s*["\'](?!.*\$\{)[^"\']{8,}["\']',
                        's\s*=\s*["\'](?!.*\$\{)[^"\']{8,}["\']',
                        'y\s*=\s*["\'](?!.*\$\{)[^"\']{20,}["\']',
                        'on\s*=\s*["\'](?!.*\$\{)[^"\']{20,}["\']'
                    ]
                    
                    fo i, lin in nu(onn.spli('\n'), 1):
                        fo pn in spns:
                            if .sh(pn, lin, .INOS):
                                slf.snsuls['suiyviolions'].ppn({
                                    'fil': s(pyfil),
                                    'lin': i,
                                    'yp': 'hos',
                                    'sviy': 'IIL',
                                    'onn': lin.sip()[:50] + '...'
                                })
                xp xpion:
                    pss

    f snioupion(slf):
        """Sn fo i-l oupion"""
        pin("🔄 Snnin fo i oupion...")
        
        # h fo i on ifs
        oupionfils = [
            'h oiin ln-hisoyin --fo',
            'in)',
            'oiin',
            'ln-hisoyin'
        ]
        
        fo oupionfil in oupionfils:
            oupionph = slf.poph / oupionfil
            if oupionph.xiss():
                slf.snsuls['ioupion'].ppn({
                    'fil': s(oupionph),
                    'yp': 'ionif',
                    'sviy': 'HIH'
                })
        
        # h fo i o fils
        fo ofil in slf.poph.lob('i-o-*.x'):
            slf.snsuls['ioupion'].ppn({
                'fil': s(ofil),
                'yp': 'iofil', 
                'sviy': 'IU'
            })

    f snfiloupion(slf):
        """Sn fo fil oupion n noin issus"""
        pin("📄 Snnin fo fil oupion...")
        
        fo filph in slf.poph.lob('*'):
            if filph.isfil():
                y:
                    # h fil siz
                    siz = filph.s().ssiz
                    
                    # h fo unxply py fils
                    if siz == 0 n no slf.isllowpy(filph):
                        slf.snsuls['pyfils'].ppn({
                            'fil': s(filph),
                            'yp': 'unxppy'
                        })
                    
                    # h x fils fo oupion pns
                    if filph.suffix in ['.py', '.js', '.json', '.', '.x', '.b', '.ps1']:
                        y:
                            onn = filph.x(noin='uf-8', os='ino')
                            
                            # h fo oupion pns
                            fo pn in slf.oupionpns:
                                if .sh(pn, onn):
                                    slf.snsuls['filoupion'].ppn({
                                        'fil': s(filph),
                                        'yp': 'oupionpn',
                                        'pn': pn,
                                        'sviy': 'HIH'
                                    })
                                    b
                            
                            # h fo noin issus
                            y:
                                filph.x(noin='uf-8', os='si')
                            xp Uniooo:
                                slf.snsuls['noinissus'].ppn({
                                    'fil': s(filph),
                                    'yp': 'noino',
                                    'sviy': 'IU'
                                })
                                
                        xp xpion:
                            pss
                            
                xp xpion:
                    pss

    f hiilfilsiniy(slf):
        """h iniy of iil L.I.F.. Plfo fils"""
        pin("🧠 hin iil L.I.F.. fils iniy...")
        
        fo pn in slf.iilfils:
            filsfoun = lis(slf.poph.lob(pn))
            
            if filsfoun:
                fo filph in filsfoun:
                    if filph.isfil() n filph.s().ssiz > 0:
                        slf.snsuls['iilfilssus'][pn] = {
                            'sus': 'O',
                            'fil': s(filph),
                            'siz': filph.s().ssiz
                        }
                    ls:
                        slf.snsuls['iilfilssus'][pn] = {
                            'sus': 'PY',
                            'fil': s(filph) if filph.xiss() ls 'NOFOUN'
                        }
            ls:
                slf.snsuls['iilfilssus'][pn] = {
                    'sus': 'ISSIN',
                    'fil': 'NOFOUN'
                }

    f isllowpy(slf, filph: Ph) -> bool:
        """h if fil is llow o b py"""
        llowpy = [
            'ini.py',
            '.ip', 
            '.iino',
            'lol.sins.json'
        ]
        un filph.n in llowpy o filph.suffix == '.plhol'

    f xusflnup(slf) -> i:
        """xu sf lnup wih ollb pbiliy"""
        pin("\n🧹 xuin sf lnup...")
        
        lnupsuls = {
            'ionsn': [],
            'filsov': 0,
            'filsso': 0,
            'os': []
        }
        
        # 1. ov suiy violions
        fo violion in slf.snsuls['suiyviolions']:
            y:
                filph = Ph(violion['fil'])
                if filph.xiss():
                    filph.unlin()
                    lnupsuls['ionsn'].ppn(f"OV SUIY VIOLION: {violion['fil']}")
                    lnupsuls['filsov'] += 1
            xp xpion s :
                lnupsuls['os'].ppn(f"Fil o ov {violion['fil']}: {}")
        
        # 2. ov i oupion ifs
        fo oupion in slf.snsuls['ioupion']:
            y:
                filph = Ph(oupion['fil'])
                if filph.xiss():
                    filph.unlin()
                    lnupsuls['ionsn'].ppn(f"OV I OUPION: {oupion['fil']}")
                    lnupsuls['filsov'] += 1
            xp xpion s :
                lnupsuls['os'].ppn(f"Fil o ov {oupion['fil']}: {}")
        
        # 3. ov fils wih oupion pns
        fo oupion in slf.snsuls['filoupion']:
            if oupion['yp'] == 'oupionpn':
                y:
                    filph = Ph(oupion['fil'])
                    # Only ov if i's lly  oupion if, no  lii fil
                    if ny(if in filph.n fo if in ['oiin', 'in)', 'i-o']):
                        filph.unlin()
                        lnupsuls['ionsn'].ppn(f"OV OUP: {oupion['fil']}")
                        lnupsuls['filsov'] += 1
                xp xpion s :
                    lnupsuls['os'].ppn(f"Fil o ov {oupion['fil']}: {}")
        
        # 4. Fix i onfiuion
        y:
            ionfis = [
                ['i', 'onfi', '--lobl', 'o.p', '""'],
                ['i', 'onfi', '--lobl', 'p.bnh', 'fls'],
                ['i', 'onfi', '--lobl', 'p.lo', 'fls'],
                ['i', 'onfi', '--lobl', 'p.iff', 'fls'],
                ['i', 'onfi', '--lobl', 'o.uolf', 'u']
            ]
            
            fo onfi in ionfis:
                subposs.un(onfi, h=Fls, puoupu=u)
            
            lnupsuls['ionsn'].ppn("FIX: i onfiuion")
        xp xpion s :
            lnupsuls['os'].ppn(f"Fil o fix i onfi: {}")
        
        un lnupsuls

    f vliplfoiniy(slf) -> i:
        """Vli L.I.F.. Plfo iniy f lnup"""
        pin("✅ Vliin plfo iniy...")
        
        vliion = {
            'iilfilso': u,
            'oiposo': u,
            'plfofunionl': u,
            'issus': []
        }
        
        # h iil fils
        fo pn, sus in slf.snsuls['iilfilssus'].is():
            if sus['sus'] != 'O':
                vliion['iilfilso'] = Fls
                vliion['issus'].ppn(f"iil fil issu: {pn} is {sus['sus']}")
        
        # s o ipos
        y:
            ssip = """
y:
    ipo zuonfi
    ipo sys
    fo phlib ipo Ph
    sys.ph.ppn(s(Ph.w()))
    fo vnuissys ipo VnuisSys
    pin("OIPOSO")
xp xpion s :
    pin(f"OIPOSO: {}")
"""
            sul = subposs.un([sys.xubl, '-', ssip], 
                                 puoupu=u, x=u, w=slf.poph)
            
            if "OIPOSO" no in sul.sou:
                vliion['oiposo'] = Fls
                vliion['issus'].ppn(f"o ipo o: {sul.sou + sul.s}")
                
        xp xpion s :
            vliion['oiposo'] = Fls
            vliion['issus'].ppn(f"Ipo s fil: {}")
        
        vliion['plfofunionl'] = vliion['iilfilso'] n vliion['oiposo']
        
        un vliion

    f unophnsivsn(slf) -> i:
        """un opl oupion sn n lnup"""
        pin("🔍 L.I.F.. Plfo p oupion Snn")
        pin("=" * 60)
        
        #  sfy bup
        slf.sfybup()
        
        # un ll sns
        slf.snsuiyviolions()
        slf.snioupion() 
        slf.snfiloupion()
        slf.hiilfilsiniy()
        
        # isply suls
        pin("\n📊 SN SULS:")
        pin(f"   Suiy violions: {ln(slf.snsuls['suiyviolions'])}")
        pin(f"   i oupion: {ln(slf.snsuls['ioupion'])}")
        pin(f"   Fil oupion: {ln(slf.snsuls['filoupion'])}")
        pin(f"   py fils: {ln(slf.snsuls['pyfils'])}")
        pin(f"   noin issus: {ln(slf.snsuls['noinissus'])}")
        
        # Show iil fils sus
        pin("\n🧠 IIL L.I.F.. FILS SUS:")
        fo pn, sus in slf.snsuls['iilfilssus'].is():
            susion = "✅" if sus['sus'] == 'O' ls "⚠️"
            pin(f"   {susion} {pn}: {sus['sus']}")
        
        un slf.snsuls

f in():
    """in xuion"""
    snn = poupionSnn()
    
    # un ophnsiv sn
    suls = snn.unophnsivsn()
    
    # h if lnup is n
    issusfoun = (
        ln(suls['suiyviolions']) +
        ln(suls['ioupion']) +
        ln(suls['filoupion'])
    )
    
    if issusfoun > 0:
        pin(f"\n⚠️  Foun {issusfoun} oupion issus")
        
        spons = inpu("\n🧹 xu uoi lnup? (y/N): ").low().sip()
        if spons == 'y':
            # xu lnup
            lnupsuls = snn.xusflnup()
            
            pin(f"\n✅ LNUP OPL")
            pin(f"   Fils ov: {lnupsuls['filsov']}")
            pin(f"   ions n: {ln(lnupsuls['ionsn'])}")
            
            if lnupsuls['os']:
                pin(f"   os: {ln(lnupsuls['os'])}")
                fo o in lnupsuls['os'][:3]:  # Show fis 3 os
                    pin(f"     - {o}")
            
            # Vli plfo iniy
            vliion = snn.vliplfoiniy()
            
            if vliion['plfofunionl']:
                pin("\n🚀 L.I.F.. PLFO SUS: OPIONL")
                pin("   ll iil syss vifi")
            ls:
                pin("\n⚠️  L.I.F.. PLFO SUS: NS NION") 
                fo issu in vliion['issus']:
                    pin(f"     - {issu}")
            
            pin(f"\n💾 Bup loion: {snn.bupi}")
    ls:
        pin("\n✅ NO OUPION ")
        pin("   L.I.F.. Plfo posioy is ln")
    
    # Sv sn suls
    sulsfil = snn.poph / 'los' / 'oupionsnsuls.json'
    sulsfil.pn.i(xiso=u)
    
    wih opn(sulsfil, 'w') s f:
        json.up(suls, f, inn=2, ful=s)
    
    pin(f"\n📄 il suls sv: {sulsfil}")

if n == "in":
    in()