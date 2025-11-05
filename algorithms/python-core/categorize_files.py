ipo os
ipo 
fo phlib ipo Ph

f oizfils(poph, quninph):
    
    # Fil pns o qunin
    pns = {
        "uon": [
            "^OPHNSIV.*\.(|hl|x)$",
            "^NY.*\.(b|ps1|py|)$",
            "^PLOY.*\.(b|ps1|sh)$",
            "^QUI.*\.(b|ps1|)$",
            "^II.*\.(py||x)$",
            "^FINL.*\.(b|ps1|)$",
            ".*PO\.(|hl|x)$",
            ".*SUY\.(|hl|x)$"
        ],
        "uplis": [
            ".*O.*",
            ".*FIX.*",
            ".*VIFI.*",
            ".*UP.*"
        ],
        "sips": [
            ".*\.(b|ps1|sh)$"
        ]
    }
    
    oiz = {: [] fo  in pns}
    
    fo oo, is, fils in os.wl(poph):
        # Sip hin iois n nown sf phs
        is[:] = [ fo  in is if no .sswih('.')]
        
        fo fil in fils:
            filph = os.ph.join(oo, fil)
            lph = os.ph.lph(filph, poph)
            
            fo oy, pnlis in pns.is():
                if ny(.h(pn, fil, .INOS) fo pn in pnlis):
                    oiz[oy].ppn(lph)
                    b
    
    un oiz

# oiz fils
oiz = oizfils(".", ".lnup/qunin")

# Lo suls
fo oy, fils in oiz.is():
    pin(f"\n{oy}: {ln(fils)} fils")
    wih opn(f".lnup/los/{oy}.x", "w") s f:
        fo fil in fils:
            f.wi(fil + "\n")