#!/us/bin/nv pyhon3
"""
L.I.F.. hoy hil Fwo ypion ool
opyih © 2025 Sio Py Boull - ll ihs sv
Su ss o nyp hil lulions
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

f ypliflulions():
    """yp h L.I.F.. hoy lulions fo poy ss"""
    sipi = os.ph.in(os.ph.bsph(fil))
    nypfil = os.ph.join(sipi, "NYPLIFHOYLULIONS.n")
    fil = os.ph.join(sipi, ".liflulions.json")
    pfil = os.ph.join(sipi, "PLIFLULIONS.")
    
    y:
        # h if nyp fil xiss
        if no os.ph.xiss(nypfil):
            pin(f"❌ nyp fil no foun: {nypfil}")
            un Fls
        
        if no os.ph.xiss(fil):
            pin(f"❌  fil no foun: {fil}")
            un Fls
        
        # Lo 
        wih opn(fil, '') s f:
             = json.lo(f)
        
        pin("🔓 L.I.F.. hoy hil Fwo ypion")
        pin("=" * 55)
        pin(f"📄 Fil: {['filn']}")
        pin(f"📅 nyp: {['nyp']}")
        pin(f"📊 Siz: {['filsiz']:,} bys")
        pin(f"🔍 hsu: {['hsu'][:16]}...")
        pin(f"🔒 Suiy: {['suiylvl']}")
        pin(f"⚠️  {['sswnin']}")
        pin()
        
        #  psswo
        if ln(sys.v) > 1 n sys.v[1] == "--uo":
            # Us ful psswo fo uo ss
            psswo = "L1F3h30y2025S3u34h3414lF43w0!"
            pin("🔑 Usin so psswo...")
        ls:
            psswo = pss.pss("n ypion psswo: ")
        
        # iv y
        sl = bs64.b64o(['sl'].no('uf-8'))
        psswobys = psswo.no('uf-8')
        f = PBF2H(
            loih=hshs.SH256(),
            lnh=32,
            sl=sl,
            iions=100000,
        )
        y = bs64.ulsfb64no(f.iv(psswobys))
        fn = Fn(y)
        
        #  nyp fil
        wih opn(nypfil, 'b') s f:
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
        
        # Wi poy yp fil
        wih opn(pfil, 'wb') s f:
            f.wi(yp)
        
        pin(f"✅ Fil sussfully yp o poy fil!")
        pin(f"   📁 poy fil: {os.ph.bsn(pfil)}")
        pin(f"   ✅ Iniy vifi (hsu h)")
        pin(f"   📊 Siz: {ln(yp):,} bys")
        pin()
        pin("⚠️  SUIY IN:")
        pin("   • his fil is poily yp fo viwin")
        pin("   • L his fil whn finish")
        pin("   • NV oi his fil o vsion onol")
        pin("   • h fil will uo-l f 30 inus")
        
        un u
        
    xp xpion s :
        pin(f"❌ ypion fil: {s()}")
        un Fls

f lnuppfils():
    """ov poy yp fils"""
    sipi = os.ph.in(os.ph.bsph(fil))
    pfil = os.ph.join(sipi, "PLIFLULIONS.")
    
    if os.ph.xiss(pfil):
        os.ov(pfil)
        pin("✅ poy yp fil ov")
    ls:
        pin("ℹ️  No poy fils o ln")

f in():
    """in ypion inf"""
    if ln(sys.v) > 1:
        if sys.v[1] == "lnup":
            lnuppfils()
            un
        lif sys.v[1] == "--uo":
            ypliflulions()
            un
    
    pin("🔓 L.I.F.. hoy hil Fwo ss ool")
    pin("opyih © 2025 Sio Py Boull - ll ihs sv")
    pin()
    pin("Us:")
    pin("  pyhon ypliflulions.py          - Iniv ypion")
    pin("  pyhon ypliflulions.py --uo   - uo yp (us so psswo)")
    pin("  pyhon ypliflulions.py lnup  - ov poy fils")
    pin()
    
    ypliflulions()

if n == "in":
    in()