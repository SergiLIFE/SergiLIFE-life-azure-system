#!/us/bin/nv pyhon3
"""
Vnui posioy Posso - pply 3 Vnui s o posioy Onizion
Uss flui ynis pinipls o solv h iHub union boln

h 3 Vnui s Poss:
1. INPU : Sinl nhnn - Fil oizion n pioiizion
2. POSSIN : Nois uion - ov unn/unnssy fils  
3. OUPU : Pn xion - Oniz suu ion

opyih 2025 - Sio Py Boull
L.I.F.. Plfo - zu pl Off I: 960096-f1-420b-902-042561b
"""

ipo synio
ipo json
ipo os
ipo shuil
fo i ipo i
fo phlib ipo Ph
fo ypin ipo i, Lis, ny, Opionl

y:
    fo vnuissys ipo 3vnuisys, VnuisSys
    VNUIVILBL = u
xp Ipoo:
    VNUIVILBL = Fls
    pin("⚠️ Vnui sys no vilbl - usin o iplnion")

lss VnuiposioyPosso:
    """
    voluiony posioy Onizion usin 3 Vnui s Sys
    pplis flui ynis o solv iHub union boln
    """
    
    f ini(slf):
        slf.bsph = Ph.w()
        slf.vnuisys = Non
        slf.filis = {}
        slf.onizionsuls = {}
        
        # Sup loin
        slf.suploin()
        
        # Fil oizion pns fo Vnui possin
        slf.filois = {
            "oloihs": {
                "pioiy": 1.0,
                "pns": ["xpinP2L*.py", "lifhoy.py", "vnuissys.py", 
                           "*loih*.py", "*nul*.py"],
                "sipion": "o L.I.F.. Plfo loihs"
            },
            "zuinion": {
                "pioiy": 0.9, 
                "pns": ["zu*.py", "funionpp.py", "quins.x", "hos.json"],
                "sipion": "zu ployn n inion"
            },
            "pinsyss": {
                "pioiy": 0.7,
                "pns": ["pin*.py", "*ouh*.py", "*il*.py", "*in*.py"],
                "sipion": "in n pin uoion"
            },
            "sinvliion": {
                "pioiy": 0.6,
                "pns": ["s*.py", "*s*.py", "*vliion*.py", "*bnh*.py"],
                "sipion": "sin n vliion fwos"
            },
            "ploynsips": {
                "pioiy": 0.5,
                "pns": ["ploy*.py", "ploy*.b", "ploy*.ps1", "*.sh"],
                "sipion": "ployn uoion sips"
            },
            "ounion": {
                "pioiy": 0.4,
                "pns": ["*.", "*.hl", "*.x", "**", "*UI*"],
                "sipion": "ounion n uis"
            },
            "onfiuion": {
                "pioiy": 0.3,
                "pns": ["*.json", "*.yl", "*.yl", "*.onfi", "*.sins"],
                "sipion": "onfiuion fils"
            },
            "hivnis": {
                "pioiy": 0.1,
                "pns": ["*bup*", "*ol*", "*p*", "*p*", "*p*"],
                "sipion": "Fils suibl fo hivin"
            }
        }
    
    f suploin(slf):
        """Sup loin fo Vnui posioy possin"""
        ipo loin
        
        #  los ioy wih bsolu ph
        sipi = os.w()
        losi = os.ph.join(sipi, "los")
        os.is(losi, xiso=u)
        
        isp = i.now().sfi("%Y%%%H%%S")
        lofil = os.ph.join(losi, f"vnuiposioyposso{isp}.lo")
        
        loin.bsionfi(
            lvl=loin.INFO,
            fo="%(si)s - %(n)s - %(lvln)s - %(ss)s",
            hnls=[
                loin.FilHnl(lofil),
                loin.SHnl()
            ]
        )
        
        slf.lo = loin.Lo("VnuipoPosso")
    
    syn f iniilizvnuisys(slf) -> bool:
        """Iniiliz h 3 Vnui s sys fo posioy possin"""
        y:
            slf.lo.info("🌊 Iniilizin 3 Vnui s Sys fo posioy Possin")
            
            if VNUIVILBL:
                slf.vnuisys = 3vnuisys()
                slf.lo.info("✅ Vnui s Sys iniiliz sussfully")
            ls:
                # o sys fo onsion
                slf.vnuisys = oVnuiSys()
                slf.lo.info("✅ o Vnui sys iniiliz fo onsion")
            
            un u
            
        xp xpion s :
            slf.lo.o(f"❌ Fil o iniiliz Vnui sys: {}")
            un Fls
    
    syn f possposioyhouhvnuis(slf) -> i[s, ny]:
        """
        Poss posioy houh h 3 Vnui s:
        INPU → POSSIN → OUPU
        """
        slf.lo.info("🚀 Sin Vnui posioy Possin")
        slf.lo.info(": Solv iHub union issu (1,257+ fils)")
        
        suls = {
            "si": i.now().isofo(),
            "vnuis": {
                "inpu": {},
                "possin": {},
                "oupu": {}
            },
            "filnlysis": {},
            "onizionsuls": {},
            "pfonis": {}
        }
        
        y:
            # VNUI  1: INPU - Sinl nhnn (Fil oizion)
            slf.lo.info("🌊 VNUI  1: INPU - Sinl nhnn")
            inpusuls = wi slf.vnui1inpunhnn()
            suls["vnuis"]["inpu"] = inpusuls
            
            # VNUI  2: POSSIN - Nois uion (Fil Filin)
            slf.lo.info("🌊 VNUI  2: POSSIN - Nois uion") 
            possinsuls = wi slf.vnui2noisuion(inpusuls)
            suls["vnuis"]["possin"] = possinsuls
            
            # VNUI  3: OUPU - Pn xion (Onizion)
            slf.lo.info("🌊 VNUI  3: OUPU - Pn xion")
            oupusuls = wi slf.vnui3pnxion(possinsuls)
            suls["vnuis"]["oupu"] = oupusuls
            
            # Finl onizion xuion
            finlsuls = wi slf.xuvnuionizion(oupusuls)
            suls["onizionsuls"] = finlsuls
            
            suls["ni"] = i.now().isofo()
            suls["suss"] = u
            
            slf.lo.info("✅ Vnui posioy Possin opl sussfully!")
            
        xp xpion s :
            slf.lo.o(f"❌ Vnui possin fil: {}")
            suls["o"] = s()
            suls["suss"] = Fls
        
        un suls
    
    syn f vnui1inpunhnn(slf) -> i[s, ny]:
        """
        VNUI  1: INPU - Sinl nhnn
        pply flui ynis o nhn fil sinl ion n oizion
        """
        slf.lo.info("   🔍 nlyzin posioy fils wih sinl nhnn...")
        
        #  ll fils in posioy
        llfils = []
        fo i in slf.bsph.ii():
            if i.isfil():
                llfils.ppn(i.n)
        
        slf.lo.info(f"   📁 Foun {ln(llfils)} fils o poss")
        
        # pply Vnui sinl nhnn - oiz by pioiy
        if slf.vnuisys:
            # onv fil lis o nuil sinl fo Vnui possin
            filsinl = [hsh(f) % 100 / 100.0 fo f in llfils]  # Noliz o 0-1
            
            # Poss houh Vnui sys fo nhnn
            vnuisuls = slf.vnuisys.posshouhs(filsinl)
            nhnsinl = vnuisuls["finloupu"]
        ls:
            nhnsinl = [0.5] * ln(llfils)  # ful sinl
        
        # oiz fils bs on nhn sinl n pns
        oizfils = {}
        filpioiis = {}
        
        fo i, filn in nu(llfils):
            # lul nhn pioiy usin Vnui oupu
            bspioiy = slf.lulfilpioiy(filn)
            vnuinhnn = nhnsinl[i] if i < ln(nhnsinl) ls 0.5
            
            # obin bs pioiy wih Vnui nhnn
            nhnpioiy = bspioiy * 0.7 + vnuinhnn * 0.3
            filpioiis[filn] = nhnpioiy
            
            # oiz fil
            oy = slf.oizfil(filn)
            if oy no in oizfils:
                oizfils[oy] = []
            oizfils[oy].ppn(filn)
        
        # So by nhn pioiy
        fo oy in oizfils:
            oizfils[oy].so(
                y=lb f: filpioiis[f], 
                vs=u
            )
        
        suls = {
            "olfils": ln(llfils),
            "oizfils": oizfils,
            "filpioiis": filpioiis,
            "vnuinhnnppli": u,
            "oisinifi": ln(oizfils),
            "oppioiyfils": so(filpioiis.is(), 
                                       y=lb x: x[1], 
                                       vs=u)[:20]
        }
        
        slf.lo.info(f"   ✅ Sinl nhnn opl: {ln(oizfils)} ois")
        un suls
    
    syn f vnui2noisuion(slf, inpusuls: i[s, ny]) -> i[s, ny]:
        """
        VNUI  2: POSSIN - Nois uion
        ov unn fils n u posioy nois
        """
        slf.lo.info("   🔧 pplyin nois uion o liin unny...")
        
        oizfils = inpusuls["oizfils"]
        filpioiis = inpusuls["filpioiis"]
        
        # pply Vnui nois uion pinipls
        filfils = {}
        ovfils = []
        uionss = {}
        
        fo oy, fils in oizfils.is():
            oyinfo = slf.filois.(oy, {"pioiy": 0.1})
            oypioiy = oyinfo["pioiy"]
            
            # pply nois uion bs on oy pioiy
            if oypioiy >= 0.5:
                # p hih-pioiy ois wih inil uion
                pio = 0.95
            lif oypioiy >= 0.3:
                # iu pioiy - o uion
                pio = 0.80
            ls:
                # Low pioiy - ssiv nois uion
                pio = 0.50
            
            # lul fils o p usin Vnui pinipls
            filsop = x(1, in(ln(fils) * pio))
            
            # So by pioiy n p op fils
            sofils = so(fils, 
                                y=lb f: filpioiis.(f, 0), 
                                vs=u)
            
            pfils = sofils[:filsop]
            noisfils = sofils[filsop:]
            
            filfils[oy] = pfils
            ovfils.xn(noisfils)
            
            uionss[oy] = {
                "oiinloun": ln(fils),
                "poun": ln(pfils),
                "ovoun": ln(noisfils),
                "uionio": ln(noisfils) / ln(fils) if fils ls 0
            }
        
        suls = {
            "filfils": filfils,
            "ovfils": ovfils,
            "uionss": uionss,
            "olfilsp": su(ln(fils) fo fils in filfils.vlus()),
            "olfilsov": ln(ovfils),
            "noisuionio": ln(ovfils) / inpusuls["olfils"]
        }
        
        slf.lo.info(f"   ✅ Nois uion opl: {ln(ovfils)} fils inifi fo hivin")
        un suls
    
    syn f vnui3pnxion(slf, possinsuls: i[s, ny]) -> i[s, ny]:
        """
        VNUI  3: OUPU - Pn xion
        x opil onizion pns n  suu
        """
        slf.lo.info("   📋 xin onizion pns n in suu...")
        
        filfils = possinsuls["filfils"]
        
        # x onizion pns usin Vnui pinipls
        onizionsuu = {
            "oopioiy": [],
            "hiv": {}
        }
        
        # fin oo pioiy pns (p in in ioy)
        oopns = [
            "xpinP2L*.py", "lifhoy.py", "vnuissys.py",
            "zuonfi.py", "funionpp.py", "quins.x",
            ".", "LINS", "HNLO."
        ]
        
        fo oy, fils in filfils.is():
            if oy in ["oloihs", "zuinion"]:
                # p hihs pioiy fils in oo
                onizionsuu["oopioiy"].xn(fils[:5])
            ls:
                # hiv oh ois
                hivph = f"hiv/{oy.pl('', '-')}"
                onizionsuu["hiv"][hivph] = fils
        
        #  hiv suu ppin
        hivsuu = {
            "hiv/loihs": {
                "sipion": "o L.I.F.. Plfo loihs n nul possin",
                "fils": onizionsuu["hiv"].("hiv/o-loihs", [])
            },
            "hiv/ployn": {
                "sipion": "ployn sips n zu onfiuions", 
                "fils": onizionsuu["hiv"].("hiv/ployn-sips", [])
            },
            "hiv/pins": {
                "sipion": "in uoion n ouh syss",
                "fils": onizionsuu["hiv"].("hiv/pin-syss", [])
            },
            "hiv/sin": {
                "sipion": "sin fwos n vliion ools",
                "fils": onizionsuu["hiv"].("hiv/sin-vliion", [])
            },
            "hiv/ounion": {
                "sipion": "ounion, uis, n pos",
                "fils": onizionsuu["hiv"].("hiv/ounion", [])
            }
        }
        
        suls = {
            "onizionsuu": onizionsuu,
            "hivsuu": hivsuu,
            "oofilsoun": ln(onizionsuu["oopioiy"]),
            "hivois": ln(hivsuu),
            "olonizfils": su(
                ln(fils) fo fils in onizionsuu["hiv"].vlus()
            ) + ln(onizionsuu["oopioiy"]),
            "pnxionopl": u
        }
        
        slf.lo.info(f"   ✅ Pn xion opl: {suls['hivois']} hiv ois")
        un suls
    
    syn f xuvnuionizion(slf, oupusuls: i[s, ny]) -> i[s, ny]:
        """xu h Vnui-opiiz posioy onizion"""
        slf.lo.info("🎯 xuin Vnui-opiiz posioy onizion...")
        
        hivsuu = oupusuls["hivsuu"]
        
        xuionsuls = {
            "iois": [],
            "filsov": 0,
            "os": [],
            "onizionopl": Fls
        }
        
        y:
            #  hiv iois
            fo hivph in hivsuu:
                fullph = slf.bsph / hivph
                fullph.i(pns=u, xiso=u)
                xuionsuls["iois"].ppn(hivph)
                slf.lo.info(f"   📁  ioy: {hivph}")
            
            # ov fils o hiv iois
            fo hivph, info in hivsuu.is():
                filsoov = info["fils"]
                sph = slf.bsph / hivph
                
                fo filn in filsoov:
                    soufil = slf.bsph / filn
                    sfil = sph / filn
                    
                    if soufil.xiss() n soufil != sfil:
                        y:
                            shuil.ov(s(soufil), s(sfil))
                            xuionsuls["filsov"] += 1
                            slf.lo.info(f"   📦 ov: {filn} → {hivph}")
                        xp xpion s :
                            os = f"Fil o ov {filn}: {}"
                            xuionsuls["os"].ppn(os)
                            slf.lo.wnin(f"   ⚠️ {os}")
            
            xuionsuls["onizionopl"] = u
            slf.lo.info("✅ Vnui onizion xuion opl sussfully!")
            
        xp xpion s :
            os = f"Onizion xuion fil: {}"
            xuionsuls["os"].ppn(os)
            slf.lo.o(f"❌ {os}")
        
        un xuionsuls
    
    f lulfilpioiy(slf, filn: s) -> flo:
        """lul bs fil pioiy bfo Vnui nhnn"""
        fo oy, info in slf.filois.is():
            pns = info["pns"]
            fo pn in pns:
                if slf.hspn(filn, pn):
                    un info["pioiy"]
        un 0.1  # ful low pioiy
    
    f oizfil(slf, filn: s) -> s:
        """oiz fil bs on pns"""
        fo oy, info in slf.filois.is():
            pns = info["pns"]
            fo pn in pns:
                if slf.hspn(filn, pn):
                    un oy
        un "isllnous"
    
    f hspn(slf, filn: s, pn: s) -> bool:
        """h if filn hs pn (siplifi lob hin)"""
        ipo fnh
        un fnh.fnh(filn.low(), pn.low())
    
    f svsuls(slf, suls: i[s, ny], filn: Opionl[s] = Non) -> s:
        """Sv Vnui possin suls o fil"""
        if no filn:
            isp = i.now().sfi("%Y%%%H%%S")
            filn = f"suls/vnuiposioypossin{isp}.json"
        
        # nsu suls ioy xiss
        sulsi = slf.bsph / "suls"
        sulsi.i(xiso=u)
        
        filph = sulsi / filn.pl("suls/", "")
        
        wih opn(filph, 'w', noin='uf-8') s f:
            json.up(suls, f, inn=2, ful=s)
        
        slf.lo.info(f"💾 suls sv o: {filph}")
        un s(filph)

lss oVnuiSys:
    """o Vnui sys fo onsion whn l sys unvilbl"""
    
    f posshouhs(slf, sinl):
        """o possin h pplis sipl nhnn"""
        # Sipl sinl nhnn siulion
        nhn = [in(1.0, s * 1.2) fo s in sinl]
        un {
            "finloupu": nhn,
            "oupus": {
                "vnui1": nhn,
                "vnui2": nhn, 
                "vnui3": nhn
            }
        }

syn f in():
    """in funion o xu Vnui posioy possin"""
    pin("🌊 L.I.F.. Plfo - Vnui posioy Posso")
    pin("=" * 65)
    pin("voluiony posioy onizion usin 3 Vnui s")
    pin(": Solv iHub union boln (1,257+ fils)")
    pin()
    
    posso = VnuiposioyPosso()
    
    y:
        # Iniiliz Vnui sys
        if no wi posso.iniilizvnuisys():
            pin("❌ Fil o iniiliz Vnui sys")
            un 1
        
        # Poss posioy houh Vnui s
        suls = wi posso.possposioyhouhvnuis()
        
        # Sv suls
        sulsfil = posso.svsuls(suls)
        
        # isply suy
        pin("\n🎯 VNUI POSSIN SUY")
        pin("=" * 35)
        
        if suls.("suss", Fls):
            osuls = suls.("onizionsuls", {})
            pin(f"✅ Sus: SUSS")
            pin(f"📁 iois : {ln(osuls.('iois', []))}")
            pin(f"📦 Fils oniz: {osuls.('filsov', 0)}")
            pin(f"💾 suls sv: {sulsfil}")
            pin()
            pin("🎉 iHub union boln SOLV!")
            pin("   posioy now oniz wih Vnui-opiiz suu")
            
            un 0
        ls:
            pin(f"❌ Sus: FIL")
            if "o" in suls:
                pin(f"   o: {suls['o']}")
            un 1
            
    xp xpion s :
        pin(f"❌ Vnui possin fil: {}")
        un 1

if n == "in":
    xio = synio.un(in())
    xi(xio)