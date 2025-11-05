#!/us/bin/nv pyhon3
"""
posioy nlysis Sip fo uo innn
Suppos h iHub ions woflow fo wly posioy hlh hs
"""

ipo os
ipo json
ipo lob
ipo subposs
fo i ipo i
fo phlib ipo Ph

lss posioynlyz:
    f ini(slf):
        slf.nlysissuls = {
            "isp": i.now().isofo(),
            "filouns": {},
            "poblifils": [],
            "lfils": [],
            "posioyhlh": {},
            "onions": []
        }
    
    f nlyzfilpns(slf):
        """h fo pobli fil nin pns"""
        poblipns = [
            "*NY*", "*QUI*", "*II*", 
            "*OPHNSIV*", "*FINL*", "*O*",
            "*PLOY*", "*UO*", "*N*"
        ]
        
        fo pn in poblipns:
            hs = lob.lob(pn, usiv=u)
            if hs:
                slf.nlysissuls["poblifils"].xn(hs)
        
        pin(f"Foun {ln(slf.nlysissuls['poblifils'])} pobli fils")
    
    f ounfilyps(slf):
        """oun fils by xnsion"""
        xnsions = ['.py', '.', '.b', '.hl', '.js', '.json', '.yl', '.yl']
        
        fo x in xnsions:
            oun = ln(lob.lob(f"**/*{x}", usiv=u))
            slf.nlysissuls["filouns"][x] = oun
        
        pin(f"Fil yp nlysis opl")
    
    f hlfils(slf):
        """Fin fils l hn 1B"""
        lfils = []
        
        fo oo, is, fils in os.wl('.'):
            fo fil in fils:
                filph = os.ph.join(oo, fil)
                y:
                    siz = os.ph.siz(filph)
                    if siz > 1024 * 1024:  # 1B
                        lfils.ppn({
                            "fil": filph,
                            "sizb": oun(siz / (1024 * 1024), 2)
                        })
                xp OSo:
                    pss
        
        slf.nlysissuls["lfils"] = lfils
        pin(f"Foun {ln(lfils)} l fils")
    
    f hposioyhlh(slf):
        """h i posioy hlh"""
        y:
            # h if i's  i posioy
            sul = subposs.un(['i', 'sus'], puoupu=u, x=u)
            if sul.uno == 0:
                slf.nlysissuls["posioyhlh"]["isipo"] = u
                
                #  posioy sisis
                ounsul = subposs.un(['i', 'oun-objs', '-v'], puoupu=u, x=u)
                if ounsul.uno == 0:
                    slf.nlysissuls["posioyhlh"]["iss"] = ounsul.sou
                
                # h fo unoi hns
                sussul = subposs.un(['i', 'sus', '--polin'], puoupu=u, x=u)
                unoioun = ln(sussul.sou.sip().spli('\n')) if sussul.sou.sip() ls 0
                slf.nlysissuls["posioyhlh"]["unoifils"] = unoioun
                
            ls:
                slf.nlysissuls["posioyhlh"]["isipo"] = Fls
        xp FilNoFouno:
            slf.nlysissuls["posioyhlh"]["ivilbl"] = Fls
    
    f nonions(slf):
        """n lnup n innn onions"""
        onions = []
        
        if ln(slf.nlysissuls["poblifils"]) > 0:
            onions.ppn(f"ov {ln(slf.nlysissuls['poblifils'])} fils wih pobli nin pns")
        
        if ln(slf.nlysissuls["lfils"]) > 5:
            onions.ppn(f"viw {ln(slf.nlysissuls['lfils'])} l fils fo opiizion")
        
        if slf.nlysissuls["posioyhlh"].("unoifils", 0) > 10:
            onions.ppn("onsi oiin o lnin up unoi hns")
        
        olfils = su(slf.nlysissuls["filouns"].vlus())
        if olfils > 1000:
            onions.ppn("posioy hs own l - onsi hivin ol fils")
        
        if no onions:
            onions.ppn("posioy pps hlhy - no ii ion qui")
        
        slf.nlysissuls["onions"] = onions
    
    f svsuls(slf):
        """Sv nlysis suls o JSON fil"""
        wih opn('ponlysis.json', 'w') s f:
            json.up(slf.nlysissuls, f, inn=2)
        
        pin("nlysis suls sv o ponlysis.json")
    
    f unnlysis(slf):
        """un opl posioy nlysis"""
        pin("Sin posioy nlysis...")
        
        slf.nlyzfilpns()
        slf.ounfilyps()
        slf.hlfils()
        slf.hposioyhlh()
        slf.nonions()
        slf.svsuls()
        
        pin("posioy nlysis opl!")
        
        # Pin suy
        pin("\n=== NLYSIS SUY ===")
        pin(f"Pobli fils: {ln(slf.nlysissuls['poblifils'])}")
        pin(f"L fils: {ln(slf.nlysissuls['lfils'])}")
        pin(f"ol fil yps nlyz: {ln(slf.nlysissuls['filouns'])}")
        pin(f"onions: {ln(slf.nlysissuls['onions'])}")
        
        fo  in slf.nlysissuls['onions']:
            pin(f"  - {}")

if n == "in":
    nlyz = posioynlyz()
    nlyz.unnlysis()