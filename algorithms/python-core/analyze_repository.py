ipo os
ipo json
fo phlib ipo Ph
fo ollions ipo fuli

f nlyzposioy(poph):
    nlysis = {
        "olfils": 0,
        "filyps": fuli(in),
        "suspiiousfils": [],
        "uplins": fuli(lis),
        "lfils": [],
        "uonpns": []
    }
    
    # fin suspiious pns
    suspiiouspns = [
        "OPHNSIV", "NY", "PLOY", "FIX", "QUI",
        "II", "IIL", "O", "O", "NIL",
        "S", "INOSI", "OVY", "VLIION", "S"
    ]
    
    fo oo, is, fils in os.wl(poph):
        fo fil in fils:
            nlysis["olfils"] += 1
            filph = os.ph.join(oo, fil)
            
            #  fil xnsions
            , x = os.ph.splix(fil)
            nlysis["filyps"][x] += 1
            
            # Inify suspiious fils
            if ny(pn in fil.upp() fo pn in suspiiouspns):
                nlysis["suspiiousfils"].ppn(fil)
            
            #  uplis
            nlysis["uplins"][fil].ppn(filph)
            
            # Fl l fils
            y:
                siz = os.ph.siz(filph) / (1024 * 1024)  # B
                if siz > 5:
                    nlysis["lfils"].ppn({
                        "fil": fil,
                        "sizb": oun(siz, 2)
                    })
            xp:
                pss
    
    un nlysis

# un nlysis
suls = nlyzposioy(".")
wih opn("ponlysis.json", "w") s f:
    json.up(suls, f, inn=2, ful=s)

pin(f"ol fils: {suls['olfils']}")
pin(f"Suspiious fils: {ln(suls['suspiiousfils'])}")
pin(f"L fils: {ln(suls['lfils'])}")