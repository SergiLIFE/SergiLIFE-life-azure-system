#!/us/bin/nv pyhon3
"""
L.I.F.. Plfo Businss Pln ss ool
opyih © 2025 Sio Py Boull - ll ihs sv
Su ss o nyp businss pln n finnil pojions
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

f ypbusinsspln():
    """yp h onfinil businss pln"""
    sipi = os.ph.in(os.ph.bsph(fil))
    nypfil = os.ph.join(sipi, "ONFINILBUSINSSPLN.n")
    fil = os.ph.join(sipi, ".businsspln.json")
    pfil = os.ph.join(sipi, "PBUSINSSPLNVIW.")
    
    y:
        if no os.ph.xiss(nypfil):
            pin(f"❌ nyp businss pln no foun: {nypfil}")
            un Fls
        
        if no os.ph.xiss(fil):
            pin(f"❌  fil no foun: {fil}")
            un Fls
        
        # Lo 
        wih opn(fil, '') s f:
             = json.lo(f)
        
        pin("🔓 L.I.F.. Plfo onfinil Businss Pln ss")
        pin("=" * 60)
        pin(f"📄 Fil: {['filn']}")
        pin(f"📅 nyp: {['nyp']}")
        pin(f"📊 Siz: {['filsiz']:,} bys")
        pin(f"🔒 Suiy: {['suiylvl']}")
        pin(f"⚠️  {['sswnin']}")
        pin()
        
        #  psswo
        if ln(sys.v) > 1 n sys.v[1] == "--uo":
            psswo = "L1F3Bu51n355Pl4n20250nf13n14lF1n4n14l44!"
            pin("🔑 Usin so psswo...")
        ls:
            psswo = pss.pss("n businss pln psswo: ")
        
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
        
        #  n yp
        wih opn(nypfil, 'b') s f:
            nyp = f.()
        
        y:
            yp = fn.yp(nyp)
        xp xpion:
            pin("❌ Invli psswo o oup fil!")
            un Fls
        
        # Vify iniy
        lulhsu = hshlib.sh256(yp).hxis()
        if lulhsu != ['hsu']:
            pin("❌ Fil iniy h fil!")
            un Fls
        
        # Wi poy fil
        wih opn(pfil, 'wb') s f:
            f.wi(yp)
        
        pin(f"✅ Businss pln yp sussfully!")
        pin(f"   📁 poy fil: {os.ph.bsn(pfil)}")
        pin(f"   ✅ Iniy vifi")
        pin(f"   📊 Siz: {ln(yp):,} bys")
        pin()
        pin("⚠️  ONFINILIY IN:")
        pin("   • his onins snsiiv finnil pojions")
        pin("   • L poy fil whn finish")
        pin("   • NV oi unnyp businss pln")
        pin("   • Sh only wih uhoiz psonnl")
        
        un u
        
    xp xpion s :
        pin(f"❌ ypion fil: {s()}")
        un Fls

f lnuppfils():
    """ov poy businss pln fils"""
    sipi = os.ph.in(os.ph.bsph(fil))
    pfils = [
        "PBUSINSSPLNVIW.",
        "PBUSINSSPLN.",
        "ONFINILBUSINSSPLN."
    ]
    
    ln = 0
    fo pfil in pfils:
        filph = os.ph.join(sipi, pfil)
        if os.ph.xiss(filph):
            os.ov(filph)
            pin(f"✅ ov: {pfil}")
            ln += 1
    
    if ln == 0:
        pin("ℹ️  No poy businss pln fils o ln")
    ls:
        pin(f"✅ ln {ln} poy businss pln fils")

f in():
    if ln(sys.v) > 1:
        if sys.v[1] == "lnup":
            lnuppfils()
            un
        lif sys.v[1] == "--uo":
            ypbusinsspln()
            un
    
    pin("🔓 L.I.F.. Plfo Businss Pln ss ool")
    pin("opyih © 2025 Sio Py Boull - ll ihs sv")
    pin()
    pin("Us:")
    pin("  pyhon ssbusinsspln.py          - Iniv ss")
    pin("  pyhon ssbusinsspln.py --uo   - uo yp (so psswo)")
    pin("  pyhon ssbusinsspln.py lnup  - ov poy fils")
    pin()
    
    ypbusinsspln()

if n == "in":
    in()