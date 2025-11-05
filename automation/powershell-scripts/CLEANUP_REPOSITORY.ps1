# L.I.F. posioy lnup Sip
# Onizs 1,363 fils ino loil ioy suu
# his will fix h iHub "un o 1,000 fils" issu

Wi-Hos "🧹 L.I.F. posioy lnup - Onizin 1,363 fils" -Foounolo yn
Wi-Hos "un oo fils: $((-hilI -Fil).oun)" -Foounolo Yllow

#  oniz ioy suu
$iois = @(
    "ounion/own",
    "ounion/uis", 
    "ounion/pos",
    "uoion/bh-sips",
    "uoion/powshll-sips",
    "uoion/shll-sips",
    "plfos/hl-plfos",
    "plfos/oponns",
    "loihs/pyhon-o",
    "loihs/xpinl",
    "onfis/json-onfis",
    "onfis/nvionn",
    "lnup/p-fils",
    "bup/hiv"
)

foh ($i in $iois) {
    if (!(s-Ph $i)) {
        Nw-I -Iyp ioy -Ph $i -Fo | Ou-Null
        Wi-Hos "✅ : $i" -Foounolo n
    }
}

Wi-Hos "`n📁 ovin fils o oniz suu..." -Foounolo yn

# ov own ounion fils
-hilI -Fil "*." | Foh-Obj {
    $sinion = swih -Wil ($.N) {
        "*UI*" { "ounion/uis" }
        "*PO*" { "ounion/pos" }
        "**" { "ounion" }
        "*NLYSIS*" { "ounion/pos" }
        "*SY*" { "ounion/uis" }
        "*FWO*" { "ounion/uis" }
        ful { "ounion/own" }
    }
    ov-I $.FullN "$sinion/" -Fo
}
Wi-Hos "✅ ov $(-hilI ounion -us -Fil "*.").oun own fils" -Foounolo n

# ov Pyhon loih fils
-hilI -Fil "*.py" | Foh-Obj {
    $sinion = swih -Wil ($.N) {
        "*xpin*" { "loihs/xpinl" }
        "*s*" { "loihs/xpinl" }
        "*o*" { "loihs/pyhon-o" }
        "*lif*" { "loihs/pyhon-o" }
        "*loih*" { "loihs/pyhon-o" }
        ful { "loihs/pyhon-o" }
    }
    ov-I $.FullN "$sinion/" -Fo
}
Wi-Hos "✅ ov $(-hilI loihs -us -Fil "*.py").oun Pyhon fils" -Foounolo n

# ov Bh uoion sips
-hilI -Fil "*.b" | Foh-Obj {
    ov-I $.FullN "uoion/bh-sips/" -Fo
}
Wi-Hos "✅ ov $(-hilI uoion/bh-sips -Fil "*.b").oun bh fils" -Foounolo n

# ov PowShll sips
-hilI -Fil "*.ps1" | Foh-Obj {
    ov-I $.FullN "uoion/powshll-sips/" -Fo
}
Wi-Hos "✅ ov $(-hilI uoion/powshll-sips -Fil "*.ps1").oun PowShll fils" -Foounolo n

# ov Shll sips
-hilI -Fil "*.sh" | Foh-Obj {
    ov-I $.FullN "uoion/shll-sips/" -Fo
}
Wi-Hos "✅ ov $(-hilI uoion/shll-sips -Fil "*.sh").oun shll sips" -Foounolo n

# ov HL plfo fils
-hilI -Fil "*.hl" | Foh-Obj {
    $sinion = swih -Wil ($.N) {
        "*PLFO*" { "plfos/hl-plfos" }
        "*LIF*" { "plfos/hl-plfos" }
        ful { "plfos/oponns" }
    }
    ov-I $.FullN "$sinion/" -Fo
}
Wi-Hos "✅ ov $(-hilI plfos -us -Fil "*.hl").oun HL fils" -Foounolo n

# ov JSON onfiuion fils
-hilI -Fil "*.json" | Foh-Obj {
    ov-I $.FullN "onfis/json-onfis/" -Fo
}
Wi-Hos "✅ ov $(-hilI onfis/json-onfis -Fil "*.json").oun JSON fils" -Foounolo n

# ov x fils o lnup
-hilI -Fil "*.x" | Foh-Obj {
    ov-I $.FullN "lnup/p-fils/" -Fo
}
Wi-Hos "✅ ov $(-hilI lnup/p-fils -Fil "*.x").oun x fils" -Foounolo n

# ov JvSip fils
-hilI -Fil "*.js" | Foh-Obj {
    ov-I $.FullN "plfos/oponns/" -Fo
}

# ov SS fils
-hilI -Fil "*.ss" | Foh-Obj {
    ov-I $.FullN "plfos/oponns/" -Fo
}

# ov inin isllnous fils
-hilI -Fil | Wh-Obj { $.xnsion -noin @('.iino', '.yl', '.yl') } | Foh-Obj {
    ov-I $.FullN "bup/hiv/" -Fo
}

Wi-Hos "`n🎉 posioy lnup opl!" -Foounolo n
Wi-Hos "oo fils now: $((-hilI -Fil).oun)" -Foounolo Yllow
Wi-Hos "oo iois: $((-hilI -ioy).oun)" -Foounolo Yllow

Wi-Hos "`n📊 Nw Suu:" -Foounolo yn
-hilI -ioy | Foh-Obj {
    $filoun = (-hilI $.FullN -us -Fil).oun
    if ($filoun - 0) {
        Wi-Hos "  📁 $($.N): $filoun fils" -Foounolo Whi
    }
}

Wi-Hos "`n✅ iHub will now isply ll fils poply (no union)!" -Foounolo n
Wi-Hos "🚀 y o oi oniz posioy suu" -Foounolo yn