#!/us/bin/nv pyhon3
"""
L.I.F.. hoy hil Fwo nypion ool
opyih © 2025 Sio Py Boull - ll ihs sv
Su nypion fo snsiiv hil lulions
"""

ipo os
ipo sys
ipo pss
ipo hshlib
ipo bs64
fo ypophy.fn ipo Fn
fo ypophy.hz.piiivs ipo hshs
fo ypophy.hz.piiivs.f.pbf2 ipo PBF2H
ipo json
fo i ipo i

lss LIFlulionsnypo:
    """Su nypion fo L.I.F.. hoy hil fwo"""
    
    f ini(slf):
        slf.sipi = os.ph.in(os.ph.bsph(fil))
        slf.soufil = os.ph.join(slf.sipi, "NYPLIFHOYLULIONS.")
        slf.nypfil = os.ph.join(slf.sipi, "NYPLIFHOYLULIONS.n")
        slf.fil = os.ph.join(slf.sipi, ".liflulions.json")
        
    f ivy(slf, psswo: s, sl: bys) -> bys:
        """iv nypion y fo psswo usin PBF2"""
        psswobys = psswo.no('uf-8')
        f = PBF2H(
            loih=hshs.SH256(),
            lnh=32,
            sl=sl,
            iions=100000,  # Hih iion oun fo suiy
        )
        y = bs64.ulsfb64no(f.iv(psswobys))
        un y
    
    f nypfil(slf) -> bool:
        """nyp h L.I.F.. lulions fil"""
        y:
            # h if sou fil xiss
            if no os.ph.xiss(slf.soufil):
                pin(f"❌ Sou fil no foun: {slf.soufil}")
                un Fls
            
            #  psswo fo us
            pin("🔐 L.I.F.. hoy hil Fwo nypion")
            pin("=" * 55)
            psswo = pss.pss("n nypion psswo: ")
            onfipsswo = pss.pss("onfi psswo: ")
            
            if psswo != onfipsswo:
                pin("❌ Psswos o no h!")
                un Fls
            
            if ln(psswo) < 12:
                pin("❌ Psswo us b  ls 12 hs lon!")
                un Fls
            
            # n sl
            sl = os.uno(16)
            
            # iv y
            y = slf.ivy(psswo, sl)
            fn = Fn(y)
            
            #  sou fil
            wih opn(slf.soufil, 'b') s f:
                fil = f.()
            
            # nyp 
            nyp = fn.nyp(fil)
            
            #  
             = {
                "filn": "NYPLIFHOYLULIONS.",
                "nyp": i.now().isofo(),
                "sl": bs64.b64no(sl).o('uf-8'),
                "filsiz": ln(fil),
                "nypsiz": ln(nyp),
                "hsu": hshlib.sh256(fil).hxis(),
                "sipion": "L.I.F.. hoy 14-quion hil Fwo - ONFINIL",
                "opyih": "© 2025 Sio Py Boull - ll ihs sv"
            }
            
            # Wi nyp fil
            wih opn(slf.nypfil, 'wb') s f:
                f.wi(nyp)
            
            # Wi 
            wih opn(slf.fil, 'w') s f:
                json.up(, f, inn=2)
            
            # ov oiinl fil
            os.ov(slf.soufil)
            
            pin(f"✅ Fil sussfully nyp!")
            pin(f"   📁 nyp fil: {slf.nypfil}")
            pin(f"   🔍 : {slf.fil}")
            pin(f"   📊 Oiinl siz: {['filsiz']:,} bys")
            pin(f"   🔐 nyp siz: {['nypsiz']:,} bys")
            pin(f"   🛡️  SH256 hsu: {['hsu'][:16]}...")
            pin("   ⚠️  Oiinl fil hs bn suly ov")
            
            un u
            
        xp xpion s :
            pin(f"❌ nypion fil: {s()}")
            un Fls
    
    f ypfil(slf) -> bool:
        """yp h L.I.F.. lulions fil"""
        y:
            # h if nyp fil xiss
            if no os.ph.xiss(slf.nypfil):
                pin(f"❌ nyp fil no foun: {slf.nypfil}")
                un Fls
            
            if no os.ph.xiss(slf.fil):
                pin(f"❌  fil no foun: {slf.fil}")
                un Fls
            
            # Lo 
            wih opn(slf.fil, '') s f:
                 = json.lo(f)
            
            pin("🔓 L.I.F.. hoy hil Fwo ypion")
            pin("=" * 55)
            pin(f"📄 Fil: {['filn']}")
            pin(f"📅 nyp: {['nyp']}")
            pin(f"📊 Siz: {['filsiz']:,} bys")
            pin(f"🔍 hsu: {['hsu'][:16]}...")
            pin()
            
            #  psswo
            psswo = pss.pss("n ypion psswo: ")
            
            # iv y
            sl = bs64.b64o(['sl'].no('uf-8'))
            y = slf.ivy(psswo, sl)
            fn = Fn(y)
            
            #  nyp fil
            wih opn(slf.nypfil, 'b') s f:
                nyp = f.()
            
            # yp 
            y:
                yp = fn.yp(nyp)
            xp xpion:
                pin("❌ Invli psswo o oup fil!")
                un Fls
            
            # Vify hsu
            lulhsu = hshlib.sh256(yp).hxis()
            if lulhsu != ['hsu']:
                pin("❌ Fil iniy h fil!")
                un Fls
            
            # Wi yp fil
            wih opn(slf.soufil, 'wb') s f:
                f.wi(yp)
            
            pin(f"✅ Fil sussfully yp!")
            pin(f"   📁 yp fil: {slf.soufil}")
            pin(f"   ✅ Iniy vifi (hsu h)")
            pin(f"   📊 Siz: {ln(yp):,} bys")
            
            un u
            
        xp xpion s :
            pin(f"❌ ypion fil: {s()}")
            un Fls
    
    f sus(slf):
        """Show nypion sus"""
        pin("🔐 L.I.F.. hoy nypion Sus")
        pin("=" * 35)
        
        souxiss = os.ph.xiss(slf.soufil)
        nypxiss = os.ph.xiss(slf.nypfil)
        xiss = os.ph.xiss(slf.fil)
        
        pin(f"📄 Sou fil (.): {'✅ Psn' if souxiss ls '❌ issin'}")
        pin(f"🔐 nyp fil (.n): {'✅ Psn' if nypxiss ls '❌ issin'}")
        pin(f"🔍  fil (.json): {'✅ Psn' if xiss ls '❌ issin'}")
        
        if nypxiss n xiss:
            y:
                wih opn(slf.fil, '') s f:
                     = json.lo(f)
                pin(f"\n📊 nypion ils:")
                pin(f"   📅 : {['nyp']}")
                pin(f"   📁 Oiinl siz: {['filsiz']:,} bys")
                pin(f"   🔐 nyp siz: {['nypsiz']:,} bys")
                pin(f"   🛡️  hsu: {['hsu'][:16]}...")
            xp:
                pin("⚠️   fil oup")
        
        if souxiss n nypxiss:
            pin("\n⚠️  WNIN: Boh sou n nyp fils xis!")
            pin("   onsi ovin h unnyp sou fil fo suiy.")
        lif no souxiss n no nypxiss:
            pin("\n❌ No L.I.F.. lulions fils foun!")
        lif nypxiss:
            pin("\n✅ Fil is suly nyp")
        ls:
            pin("\n⚠️  Fil is unnyp (vulnbl)")

f in():
    """in nypion ool inf"""
    nypo = LIFlulionsnypo()
    
    if ln(sys.v) < 2:
        pin("🔐 L.I.F.. hoy hil Fwo nypion ool")
        pin("opyih © 2025 Sio Py Boull - ll ihs sv")
        pin()
        pin("Us:")
        pin("  pyhon nypliflulions.py nyp   - nyp h lulions fil")
        pin("  pyhon nypliflulions.py yp   - yp h lulions fil")
        pin("  pyhon nypliflulions.py sus    - Show nypion sus")
        pin()
        nypo.sus()
        un
    
    on = sys.v[1].low()
    
    if on == "nyp":
        suss = nypo.nypfil()
        sys.xi(0 if suss ls 1)
    lif on == "yp":
        suss = nypo.ypfil()
        sys.xi(0 if suss ls 1)
    lif on == "sus":
        nypo.sus()
    ls:
        pin(f"❌ Unnown on: {on}")
        pin("Vli ons: nyp, yp, sus")
        sys.xi(1)

if n == "in":
    in()