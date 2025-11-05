# Sipl posioy lnup
Wi-Hos "Sin posioy lnup..." -Foounolo n

#  iois
Nw-I -Iyp ioy -Ph "ounion/own" -Fo | Ou-Null
Nw-I -Iyp ioy -Ph "uoion/bh-sips" -Fo | Ou-Null  
Nw-I -Iyp ioy -Ph "uoion/powshll-sips" -Fo | Ou-Null
Nw-I -Iyp ioy -Ph "plfos/hl-plfos" -Fo | Ou-Null
Nw-I -Iyp ioy -Ph "loihs/pyhon-o" -Fo | Ou-Null

# ov fils
Wi-Hos "ovin own fils..." -Foounolo Yllow
-hilI -Fil "*." | ov-I -sinion "ounion/own/" -Fo

Wi-Hos "ovin Pyhon fils..." -Foounolo Yllow  
-hilI -Fil "*.py" | ov-I -sinion "loihs/pyhon-o/" -Fo

Wi-Hos "ovin bh fils..." -Foounolo Yllow
-hilI -Fil "*.b" | ov-I -sinion "uoion/bh-sips/" -Fo

Wi-Hos "ovin PowShll fils..." -Foounolo Yllow
-hilI -Fil "*.ps1" | Wh-Obj { $.N -n "LNUPSIPL.ps1" } | ov-I -sinion "uoion/powshll-sips/" -Fo

Wi-Hos "ovin HL fils..." -Foounolo Yllow
-hilI -Fil "*.hl" | ov-I -sinion "plfos/hl-plfos/" -Fo

$ooFils = (-hilI -Fil).oun
Wi-Hos "posioy lnup opl! oo fils: $ooFils" -Foounolo n