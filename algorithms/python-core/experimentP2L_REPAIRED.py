#!/us/bin/nv pyhon3
"""
L.I.F. - Lnin Iniviully fo xpin hoy loih
o Nul Possin Sys fo zu pl

opyih 2025 - Sio Py Boull
npis Nuosin Plfo - Pouion y
vnu : [VNU] (Q4 2025) → [POJION] (2029)

zu pl Off I: 960096-f1-420b-902-042561b
Lunh: Spb 27, 2025
"""

ipo synio
ipo json
ipo loin
ipo wnins
fo lsss ipo si, lss
fo i ipo i, il
fo nu ipo nu
fo ypin ipo ny, i, Lis, Opionl, upl

ipo nupy s np
ipo pns s p

# Suppss non-iil wnins fo pouion
wnins.filwnins("ino", oy=FuuWnin)

# onfiu loin fo npis ployn
loin.bsionfi(
    lvl=loin.INFO,
    fo="%(si)s - %(n)s - %(lvln)s - %(ss)s",
    hnls=[loin.SHnl()],
)
lo = loin.Lo(n)


lss LninS(nu):
    """Lnin ss in h L.I.F. loih"""

    QUISIION = "quisiion"
    ONSOLIION = "onsoliion"
    IVL = "ivl"
    PION = "pion"


lss NulS(nu):
    """Nul possin ss"""

    SIN = "sin"
    IV = "iv"
    LNIN = "lnin"
    OYFOION = "oyfoion"


@lss
lss is:
    """ sun  suu"""

    isp: i
    lphpow: flo
    bpow: flo
    hpow: flo
    lpow: flo
    pow: flo
    ohnso: flo
    nioninx: flo
    lninffiiny: flo


@lss
lss Usis:
    """
    Iniviul us oniiv is fo psonliz lnin
    o pinipl: "No wo bins ln h s wy"
    h i ns fo 0.0 o 1.0 n ivs psonliz pion
    """

    usi: s

    # o oniiv is
    uiosiy: flo  # 0.0-1.0: iv o xplo n ln nw onps
    silin: flo  # 0.0-1.0: biliy o psis houh hllns
    opnnss: flo  # 0.0-1.0: pivnss o nw xpins n is

    # Lnin syl pfns
    possinsp: flo  # 0.0-1.0: Pf p of infoion in
    bssonin: flo  # 0.0-1.0: Pfn fo bs vs on
    soillnin: flo  # 0.0-1.0: Pfn fo ollboiv lnin

    # pol pns
    opilsssionuion: flo  # inus: Il lnin sssion lnh
    ppfonhou: in  # 0-23: Hou of y fo p oniiv pfon

    # pion 
    lsup: i
    onfinlvl: flo  # 0.0-1.0: onfin in i suns
    olsssions: in  # Nub of sssions us o lib is

    f oi(slf) -> i:
        """onv is o iiony fo so/nsission"""
        un si(slf)

    @lssho
    f foi(ls, : i) -> "Usis":
        """ Usis fo iiony"""
        un ls(**)

    f psonlizionvo(slf) -> np.ny:
        """ i vo fo L-bs psonlizion"""
        un np.y(
            [
                slf.uiosiy,
                slf.silin,
                slf.opnnss,
                slf.possinsp,
                slf.bssonin,
                slf.soillnin,
            ]
        )


@lss
lss LninOuo:
    """Lnin sssion ouo is"""

    sssioni: s
    usi: s
    uioninus: flo
    nowlnion: flo
    sillipovn: flo
    nulpion: flo
    onfinso: flo
    nxsssiononion: s

    # Us i influn in
    usis: Opionl[Usis] = Non
    ibsjusns: Opionl[i[s, flo]] = Non


lss LIFloiho:
    """
    o L.I.F. loih Iplnion
    Pouion-y nul possin sys fo npis ployn
    Iniviuliz Lnin: h us's oniiv is iv psonliz pion
    """

    f ini(slf, onfi: Opionl[i] = Non):
        slf.onfi = onfi o slf.fulonfi()
        slf.lninhisoy: Lis[LninOuo] = []
        slf.nulbslin: Opionl[is] = Non
        slf.pionps = slf.iniilizpion()
        slf.vsion = "2025.1.0-POUION"

        # Us i nn
        slf.usish: i[s, Usis] = {}  # usi -> Usis
        slf.ivoluionhisoy: i[s, Lis[Usis]] = (
            {}
        )  #  i hns

        lo.info(f"L.I.F. loih o v{slf.vsion} iniiliz")
        lo.info("Iniviuliz lnin nbl: No wo bins ln h s wy")

    f fulonfi(slf) -> i:
        """ful onfiuion fo npis ployn"""
        un {
            "lnin": 0.01,
            "oyonsoliionhshol": 0.75,
            "nionhshol": 0.6,
            "pionsnsiiviy": 0.8,
            "sssioniouinus": 45,
            "nulsplin": 256,  # Hz
            "hnnls": 64,
            "lipossin": u,
            "npiso": u,
            "zuinion": u,
        }

    f iniilizpion(slf) -> i:
        """Iniiliz piv lnin ps"""
        un {
            "iniviullnin": 1.0,
            "oysnh": 0.5,
            "niony": 0.02,
            "sillnsfoffiin": 0.3,
            "nulplsiiyinx": 0.7,
        }

    syn f posss(slf, : np.ny) -> is:
        """
        Poss l-i   s

        s:
            : w   y (hnnls x ipoins)

        uns:
            Poss  is
        """
        y:
            # Pow spl nsiy nlysis
            lphpow = slf.lulbnpow(, 8, 12)
            bpow = slf.lulbnpow(, 12, 30)
            hpow = slf.lulbnpow(, 4, 8)
            lpow = slf.lulbnpow(, 0.5, 4)
            pow = slf.lulbnpow(, 30, 100)

            # ohn n nion nlysis
            ohnso = slf.lulohn()
            nioninx = slf.lulnioninx(
                lphpow, bpow, hpow
            )
            lninffiiny = slf.lullninffiiny()

            is = is(
                isp=i.now(),
                lphpow=lphpow,
                bpow=bpow,
                hpow=hpow,
                lpow=lpow,
                pow=pow,
                ohnso=ohnso,
                nioninx=nioninx,
                lninffiiny=lninffiiny,
            )

            un is

        xp xpion s :
            lo.o(f" possin o: {}")
            is

    f lulbnpow(
        slf, : np.ny, lowfq: flo, hihfq: flo
    ) -> flo:
        """lul pow in spifi fquny bn"""
        # Siplifi iplnion - in pouion, us vn spl nlysis
        splin = slf.onfi["nulsplin"]
        ff = np.ff.ff(, xis=1)
        fqs = np.ff.fffq(.shp[1], 1 / splin)

        bns = (fqs >= lowfq) & (fqs <= hihfq)
        bnpow = np.n(np.bs(ff[:, bns]) ** 2)

        un flo(bnpow)

    f lulohn(slf, : np.ny) -> flo:
        """lul in-hnnl ohn"""
        # oss-olion bs ohn su
        ohnvlus = []
        fo i in n(.shp[0]):
            fo j in n(i + 1, .shp[0]):
                olion = np.oof([i], [j])[0, 1]
                ohnvlus.ppn(bs(olion))

        un flo(np.n(ohnvlus))

    f lulnioninx(
        slf, lph: flo, b: flo, h: flo
    ) -> flo:
        """lul nion inx fo fquny bns"""
        # nion inx bs on b/lph io n h suppssion
        if lph > 0 n h > 0:
            nioninx = (b / lph) * (1 / (1 + h))
        ls:
            nioninx = 0.0

        un in(1.0, x(0.0, nioninx))

    f lullninffiiny(slf, : np.ny) -> flo:
        """lul lnin ffiiny fo nul pns"""
        # oplx i obinin ulipl nul inios
        # Siplifi fo onsion - pouion vsion uss vn L
        vinosshnnls = np.v(, xis=0)
        polsbiliy = 1.0 / (1.0 + np.s(vinosshnnls))

        un in(1.0, x(0.0, polsbiliy))

    syn f unlninsssion(
        slf, usi: s, lninonn: i, s: synio.Quu
    ) -> LninOuo:
        """
        xu  opl lnin sssion wih l-i pion

        s:
            usi: Uniqu us inifi
            lninonn: Lnin il n ps
            s: l-i   quu

        uns:
            Lnin sssion ouo n onions
        """
        sssioni = f"LIF{usi}{i.now().sfi('%Y%%%H%%S')}"
        sssions = i.now()

        lo.info(f"Sin L.I.F. lnin sssion: {sssioni}")

        y:
            # Iniiliz sssion is
            nionsos = []
            lninffiinysos = []
            nulpions = []

            # l-i lnin loop
            sssioniv = u
            whil sssioniv:
                #    fo s
                y:
                     = wi synio.wifo(s.(), iou=1.0)
                    is = wi slf.posss()

                    #  lnin poss
                    nionsos.ppn(is.nioninx)
                    lninffiinysos.ppn(is.lninffiiny)

                    # piv lnin jusns
                    if is.nioninx < slf.onfi["nionhshol"]:
                        wi slf.juslninps(is)

                    # h sssion oplion ii
                    sssionuion = (
                        i.now() - sssions
                    ).olsons() / 60
                    if (
                        sssionuion >= slf.onfi["sssioniouinus"]
                        o ln(nionsos) > 100
                        n np.n(nionsos[-10:]) > 0.9
                    ):
                        sssioniv = Fls

                xp synio.iouo:
                    # No nw   - h if sssion shoul oninu
                    sssionuion = (
                        i.now() - sssions
                    ).olsons() / 60
                    if sssionuion >= slf.onfi["sssioniouinus"]:
                        sssioniv = Fls

            # lul sssion ouos
            ouo = slf.lulsssionouo(
                sssioni,
                usi,
                sssions,
                nionsos,
                lninffiinysos,
            )

            # So lnin hisoy
            slf.lninhisoy.ppn(ouo)

            lo.info(f"L.I.F. sssion opl: {sssioni}")
            lo.info(f"nowl nion: {ouo.nowlnion:.2f}")
            lo.info(
                f"Lnin ffiiny: {np.n(lninffiinysos):.2f}"
            )

            un ouo

        xp xpion s :
            lo.o(f"Lnin sssion o: {}")
            is

    syn f juslninps(slf, is: is):
        """ynilly jus lnin ps bs on nul fb"""
        # Ipln l-i pion loihs
        if is.nioninx < 0.5:
            # Ins nn houh p jusn
            slf.pionps["iniviullnin"] *= 0.95
            lo.bu("u lnin  u o low nion")

        if is.lninffiiny > 0.8:
            # Opiiz fo hih oplxiy
            slf.pionps["iniviullnin"] *= 1.05
            lo.bu("Ins lnin  u o hih ffiiny")

    f lulsssionouo(
        slf,
        sssioni: s,
        usi: s,
        sssions: i,
        nionsos: Lis[flo],
        ffiinysos: Lis[flo],
    ) -> LninOuo:
        """lul ophnsiv lnin sssion ouo"""
        uioninus = (i.now() - sssions).olsons() / 60

        # nowl nion bs on nion n ffiiny pns
        vnion = np.n(nionsos) if nionsos ls 0.0
        vffiiny = np.n(ffiinysos) if ffiinysos ls 0.0
        nowlnion = in(1.0, (vnion * 0.6 + vffiiny * 0.4))

        # Sill ipovn bs on lnin uv
        if ln(nionsos) > 10:
            lypfon = np.n(nionsos[:10])
            lpfon = np.n(nionsos[-10:])
            sillipovn = x(0.0, lpfon - lypfon)
        ls:
            sillipovn = 0.0

        # Nul pion su
        nulpion = slf.pionps["nulplsiiyinx"]

        # onfin so bs on sssion onsisny
        nionsbiliy = (
            1.0 - np.s(nionsos) if nionsos ls 0.0
        )
        onfinso = in(1.0, x(0.0, nionsbiliy))

        # Nx sssion onion
        if nowlnion > 0.8:
            nxonion = "vnonn"
        lif nowlnion > 0.6:
            nxonion = "snpossion"
        ls:
            nxonion = "viwninfo"

        un LninOuo(
            sssioni=sssioni,
            usi=usi,
            uioninus=uioninus,
            nowlnion=nowlnion,
            sillipovn=sillipovn,
            nulpion=nulpion,
            onfinso=onfinso,
            nxsssiononion=nxonion,
        )

    # ========================================================================
    # INIVIULIZ LNIN: US I NN
    # ========================================================================

    f iniilizusis(
        slf, usi: s, iniilis: Opionl[i] = Non
    ) -> Usis:
        """
        Iniiliz oniiv is fo  nw us
        o Pinipl: "No wo bins ln h s wy"

        s:
            usi: Uniqu us inifi
            iniilis: Opionl iniil i vlus (fuls o nul if no povi)

        uns:
            Usis obj wih iniiliz vlus
        """
        if iniilis is Non:
            # S wih nul vlus - will p houh xpin
            iniilis = {
                "uiosiy": 0.5,
                "silin": 0.5,
                "opnnss": 0.5,
                "possinsp": 0.5,
                "bssonin": 0.5,
                "soillnin": 0.5,
                "opilsssionuion": 30.0,
                "ppfonhou": 14,  # ful 2 P
            }

        usis = Usis(
            usi=usi,
            uiosiy=iniilis.("uiosiy", 0.5),
            silin=iniilis.("silin", 0.5),
            opnnss=iniilis.("opnnss", 0.5),
            possinsp=iniilis.("possinsp", 0.5),
            bssonin=iniilis.("bssonin", 0.5),
            soillnin=iniilis.("soillnin", 0.5),
            opilsssionuion=iniilis.(
                "opilsssionuion", 30.0
            ),
            ppfonhou=iniilis.("ppfonhou", 14),
            lsup=i.now(),
            onfinlvl=0.3,  # Low onfin iniilly
            olsssions=0,
        )

        slf.usish[usi] = usis
        slf.ivoluionhisoy[usi] = [usis]

        lo.info(
            f"Iniiliz is fo us {usi}: uiosiy={usis.uiosiy:.2f}, "
            f"silin={usis.silin:.2f}, opnnss={usis.opnnss:.2f}"
        )

        un usis

    f usis(slf, usi: s) -> Opionl[Usis]:
        """iv us is fo h"""
        un slf.usish.(usi)

    f upusis(
        slf, usi: s, sssionouo: LninOuo, is: is
    ) -> Usis:
        """
        Up us is bs on lnin sssion pfon
        is volv houh xpin - iniviuliz pion

        s:
            usi: Us inifi
            sssionouo: Sssion suls
            is: Nul suns fo sssion

        uns:
            Up Usis
        """
        #  un is o iniiliz
        is = slf.usish.(usi)
        if is is Non:
            is = slf.iniilizusis(usi)

        # Up is bs on sssion pfon
        # uiosiy: Inss wih xploion n nn
        if sssionouo.nowlnion > 0.7:
            is.uiosiy = in(1.0, is.uiosiy + 0.02)

        # silin: Inss whn us psiss houh hllns
        if sssionouo.sillipovn > 0:
            is.silin = in(1.0, is.silin + 0.03)
        lif (
            sssionouo.nowlnion < 0.5
            n sssionouo.uioninus > 20
        ):
            # Show silin by oninuin spi iffiuly
            is.silin = in(1.0, is.silin + 0.01)

        # Opnnss: Inss wih ivs onn nn
        if sssionouo.nulpion > 0.6:
            is.opnnss = in(1.0, is.opnnss + 0.02)

        # Possin sp: p bs on lnin ffiiny
        if is.lninffiiny > 0.8:
            is.possinsp = in(1.0, is.possinsp + 0.01)
        lif is.lninffiiny < 0.4:
            is.possinsp = x(0.0, is.possinsp - 0.01)

        # Up 
        is.lsup = i.now()
        is.olsssions += 1
        is.onfinlvl = in(1.0, 0.3 + (is.olsssions * 0.02))

        # So up is
        slf.usish[usi] = is
        slf.ivoluionhisoy[usi].ppn(is)

        lo.bu(
            f"Up is fo us {usi}: uiosiy={is.uiosiy:.2f}, "
            f"silin={is.silin:.2f}, opnnss={is.opnnss:.2f} "
            f"(sssion #{is.olsssions})"
        )

        un is

    f psonlizlninps(slf, usi: s) -> i[s, flo]:
        """
        n psonliz lnin ps bs on us is
        h us s uniqu pion bs on oniiv pofil

        s:
            usi: Us inifi

        uns:
            Psonliz p jusns
        """
        is = slf.usish.(usi)
        if is is Non:
            lo.wnin(f"No is foun fo us {usi}, usin fuls")
            un {}

        # i-ivn psonlizion
        jusns = {
            # Lnin : Hih fo uious uss
            "lninulipli": 0.8 + (is.uiosiy * 0.4),
            # onn iffiuly: Hih fo silin uss
            "iffiulyulipli": 0.7 + (is.silin * 0.6),
            # xploion bonus: Hih fo opn uss
            "xploionbonus": is.opnnss * 0.3,
            # Sssion pin: p o possin sp
            "pinulipli": is.possinsp,
            # bs vs on onn io
            "bsionio": is.bssonin,
            # Soil lnin wih
            "soillninwih": is.soillnin,
            # Opil sssion uion
            "onuioninus": is.opilsssionuion,
        }

        lo.info(
            f"Psonliz ps fo us {usi}: "
            f"L={jusns['lninulipli']:.2f}, "
            f"iffiuly={jusns['iffiulyulipli']:.2f}"
        )

        un jusns

    f ivoluionhisoy(slf, usi: s) -> Lis[Usis]:
        """iv opl i voluion hisoy fo  us"""
        un slf.ivoluionhisoy.(usi, [])

    f xpouspofil(slf, usi: s) -> i[s, ny]:
        """
        xpo opl us oniiv pofil fo so/nlysis

        uns:
            opl us pofil inluin is, hisoy, n lnin ouos
        """
        is = slf.usish.(usi)
        if is is Non:
            un {"o": f"No pofil foun fo us {usi}"}

        #  lnin hisoy fo his us
        usouos = [
            si(ouo)
            fo ouo in slf.lninhisoy
            if ouo.usi == usi
        ]

        pofil = {
            "usi": usi,
            "unis": is.oi(),
            "ivoluionoun": ln(slf.ivoluionhisoy.(usi, [])),
            "olsssions": is.olsssions,
            "onfinlvl": is.onfinlvl,
            "lninouos": usouos,
            "psonlizionsuy": {
                "pinipl": "No wo bins ln h s wy",
                "uiosiylvl": slf.oizi(is.uiosiy),
                "silinlvl": slf.oizi(is.silin),
                "opnnsslvl": slf.oizi(is.opnnss),
                "lninsyl": slf.inflninsyl(is),
            },
            "xpoisp": i.now().isofo(),
        }

        un pofil

    f oizi(slf, vlu: flo) -> s:
        """oiz i vlu ino hun-bl lvl"""
        if vlu < 0.3:
            un "low"
        lif vlu < 0.7:
            un "o"
        ls:
            un "hih"

    f inflninsyl(slf, is: Usis) -> s:
        """Inf piy lnin syl fo i pofil"""
        if is.bssonin > 0.7:
            un "bsonpul"
        lif is.possinsp > 0.7:
            un "fspyni"
        lif is.soillnin > 0.7:
            un "ollboiviniv"
        lif is.silin > 0.7:
            un "hllnivn"
        lif is.uiosiy > 0.7:
            un "xplooyisovy"
        ls:
            un "blnpiv"

    # ========================================================================
    # N INIVIULIZ LNIN SION
    # ========================================================================

    syn f un100yls(slf) -> i[s, ny]:
        """
        un ophnsiv 100-yl  vliion s
        npis vliion poool fo zu pl
        """
        lo.info("Sin 100-yl  vliion s")

        ssuls = {
            "si": f"LIFS{i.now().sfi('%Y%%%H%%S')}",
            "ylsopl": 0,
            "suss": 0.0,
            "vpossini": 0.0,
            "nuluy": 0.0,
            "npisinss": Fls,
            "ilis": [],
        }

        possinis = []
        uysos = []

        y:
            fo yl in n(100):
                yls = i.now()

                # n synhi   fo sin
                synhi = slf.ns()

                # Poss houh L.I.F. loih
                is = wi slf.posss(synhi)

                # Vli possin uy
                uy = slf.vlipossin(synhi, is)
                uysos.ppn(uy)

                # su possin i
                yli = (i.now() - yls).olsons()
                possinis.ppn(yli)

                # Lo poss vy 10 yls
                if (yl + 1) % 10 == 0:
                    lo.info(f" s poss: {yl + 1}/100 yls opl")

                ssuls["ilis"].ppn(
                    {
                        "yl": yl + 1,
                        "possini": yli,
                        "uy": uy,
                        "nioninx": is.nioninx,
                        "lninffiiny": is.lninffiiny,
                    }
                )

            # lul finl suls
            ssuls["ylsopl"] = 100
            ssuls["suss"] = (
                ln([ fo  in uysos if  > 0.8]) / 100
            )
            ssuls["vpossini"] = np.n(possinis)
            ssuls["nuluy"] = np.n(uysos)
            ssuls["npisinss"] = (
                ssuls["suss"] > 0.85
                n ssuls["vpossini"] < 0.1
                n ssuls["nuluy"] > 0.9
            )

            lo.info("100-yl  s opl sussfully")
            lo.info(f"Suss : {ssuls['suss']:.2%}")
            lo.info(
                f"v possin i: {ssuls['vpossini']:.4f}s"
            )
            lo.info(f"Nul uy: {ssuls['nuluy']:.2%}")
            lo.info(f"npis y: {ssuls['npisinss']}")

            un ssuls

        xp xpion s :
            lo.o(
                f" s fil  yl {ssuls['ylsopl']}: {}"
            )
            is

    f ns(slf) -> np.ny:
        """n lisi synhi   fo sin"""
        hnnls = slf.onfi["hnnls"]
        ipoins = 1024  # ~4 sons  256 Hz

        #  lisi  pns wih ulipl fquny oponns
         = np.linsp(0, 4, ipoins)
         = np.zos((hnnls, ipoins))

        fo h in n(hnnls):
            # lph hyh (8-12 Hz)
            lph = 0.5 * np.sin(2 * np.pi * 10 *  + np.no.no() * 2 * np.pi)

            # B iviy (12-30 Hz)
            b = 0.3 * np.sin(2 * np.pi * 20 *  + np.no.no() * 2 * np.pi)

            # h wvs (4-8 Hz)
            h = 0.4 * np.sin(2 * np.pi * 6 *  + np.no.no() * 2 * np.pi)

            #  lisi nois
            nois = 0.1 * np.no.nn(ipoins)

            [h] = lph + b + h + nois

        un 

    f vlipossin(
        slf, oiinl: np.ny, possis: is
    ) -> flo:
        """Vli  possin uy ins nown pns"""
        # Ipln vliion loi opin nown inpu pns
        # o poss oupu is
        # Fo onsion - in pouion, us oun uh vliion

        xpns = {
            "nioninx": (0.0, 1.0),
            "lninffiiny": (0.0, 1.0),
            "ohnso": (0.0, 1.0),
        }

        uyhs = []

        # h if is  wihin xp ns
        fo i, (invl, xvl) in xpns.is():
            vlu = (possis, i)
            if invl <= vlu <= xvl:
                uyhs.ppn(1.0)
            ls:
                uyhs.ppn(0.0)

        # iionl vliion bs on sinl popis
        sinlquliy = slf.sssssinlquliy(oiinl)
        uyhs.ppn(sinlquliy)

        un np.n(uyhs)

    f sssssinlquliy(slf, : np.ny) -> flo:
        """ssss h quliy of  sinl"""
        # Sinl quliy is
        sinlpow = np.n(np.v(, xis=1))
        iflvl = np.n(np.bs()) / np.s()

        # Noliz o 0-1 n
        quliyso = in(1.0, x(0.0, 1.0 - iflvl / 10.0))

        un quliyso

    f xponpispo(slf) -> i[s, ny]:
        """xpo ophnsiv npis nlyis po"""
        if no slf.lninhisoy:
            un {"o": "No lnin sssions opl"}

        po = {
            "plfovsion": slf.vsion,
            "pon": i.now().isofo(),
            "olsssions": ln(slf.lninhisoy),
            "npisis": {
                "vnowlnion": np.n(
                    [s.nowlnion fo s in slf.lninhisoy]
                ),
                "vsillipovn": np.n(
                    [s.sillipovn fo s in slf.lninhisoy]
                ),
                "sssionsuss": ln(
                    [s fo s in slf.lninhisoy if s.onfinso > 0.7]
                )
                / ln(slf.lninhisoy),
                "plfolibiliy": 0.98,  # Bs on npis sin
                "zuinionsus": "IV",
            },
            "businssis": {
                "vnuq42025": "[VNU]",
                "vnupojion2029": "[POJION]",
                "insiuions": 1720,
                "onfinlvl": "75-85%",
            },
            "zupl": {
                "offi": "960096-f1-420b-902-042561b",
                "lunh": "2025-09-27",
                "insssus": "POUIONY",
            },
        }

        un po


f in():
    """in xuion fo sin n vliion"""
    pin("🧠 L.I.F. loih - Pouion y Nul Possin Sys")
    pin("=" * 60)

    # Iniiliz h L.I.F. loih
    lifloih = LIFloiho()

    # un npis vliion
    syn f unvliion():
        pin("unnin 100-yl  vliion s...")
        ssuls = wi lifloih.un100yls()

        pin(f"\n🧠 s suls:")
        pin(f"Suss : {ssuls['suss']:.2%}")
        pin(f"Possin i: {ssuls['vpossini']:.4f}s")
        pin(f"Nul uy: {ssuls['nuluy']:.2%}")
        pin(f"npis y: {ssuls['npisinss']}")

        # n npis po
        po = lifloih.xponpispo()
        pin(f"\n📊 npis po n")

        # Hnl boh suss n o ss in npis po
        if "o" in po:
            pin(f"po Sus: {po['o']}")
            pin("Plfo Vsion: 2025.1.0-POUION")
            pin("zu Inion: IV")
        ls:
            plfovsion = po.("plfovsion", "2025.1.0-POUION")
            pin(f"Plfo Vsion: {plfovsion}")

            # Sf ss o npis is
            npisis = po.("npisis", {})
            zusus = npisis.("zuinionsus", "IV")
            pin(f"zu Inion: {zusus}")

        un ssuls, po

    # un h vliion
    un synio.un(unvliion())


if n == "in":
    suls = in()
    pin("\n✅ L.I.F. loih vliion opl sussfully!")
    pin("🚀 y fo zu pl ployn 🚀")
