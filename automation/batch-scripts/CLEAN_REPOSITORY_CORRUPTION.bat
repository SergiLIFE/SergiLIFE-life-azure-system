@ho off
 L.I.F.. Plfo posioy oupion lnup
 Sf lnup wihou losin iil 
 Novb 3, 2025

ho ========================================
ho   L.I.F.. Plfo oupion lnup  
ho ========================================
ho.

 Sp 1:  bup of iil fils
ho [1/6] in sfy bup...
if no xis "OUPIONLNUPBUP" i "OUPIONLNUPBUP"
opy "xpinP2L*.py" "OUPIONLNUPBUP\" >nul 2>nul
opy "zuonfi.py" "OUPIONLNUPBUP\" >nul 2>nul
opy "vnuissys.py" "OUPIONLNUPBUP\" >nul 2>nul
opy "pinn.py" "OUPIONLNUPBUP\" >nul 2>nul
opy "quins.x" "OUPIONLNUPBUP\" >nul 2>nul
opy "." "OUPIONLNUPBUP\" >nul 2>nul
ho    Bup : OUPIONLNUPBUP/

 Sp 2: ov h pobli .nv fil (suiy violion)
ho [2/6] ovin suiy violions...
if xis "hiv\hisoil\.nv" (
    ho    OVIN: hiv\hisoil\.nv ^(suiy violion^)
    l /f "hiv\hisoil\.nv"
    ho    ✅ Suiy violion ov
) ls (
    ho    ✅ No .nv suiy violions foun
)

 Sp 3: ln up i on oupion ifs
ho [3/6] lnin i on ifs...
if xis "h oiin ln-hisoyin --fo" (
    ho    OVIN: "h oiin ln-hisoyin --fo" ^(i ypo if^)
    l /f "h oiin ln-hisoyin --fo"
)
if xis "in)" (
    ho    OVIN: "in)" ^(i ypo if^)
    l /f "in)"
)
if xis "i-o-*.x" (
    ho    OVIN: i o fils
    l /f "i-o-*.x"
)
ho    ✅ i ifs ln

 Sp 4: ov py fils (xp llow ons)
ho [4/6] ovin pobli py fils...
fo %%f in (*.p *.p *.lo~) o (
    if xis "%%f" (
        ho    OVIN: %%f ^(poy fil^)
        l /f "%%f"
    )
)
ho    ✅ poy fils ln

 Sp 5: Fix i onfiuion o pvn fuu oupion
ho [5/6] Fixin i onfiuion...
i onfi --lobl o.p ""
i onfi --lobl p.bnh fls
i onfi --lobl p.lo fls
i onfi --lobl p.iff fls
i onfi --lobl o.uolf u
i onfi --lobl o.sflf wn
ho    ✅ i onfiuion su

 Sp 6: Vli posioy iniy
ho [6/6] Vliin posioy iniy...
i sus --polin > psus.x
s /p isus=<psus.x
l psus.x

if xis "xpinP2L*.py" (
    ho    ✅ o L.I.F.. loihs in
) ls (
    ho    ⚠️  o loihs issin - soin fo bup
    opy "OUPIONLNUPBUP\xpinP2L*.py" . >nul 2>nul
)

if xis "zuonfi.py" (
    ho    ✅ zu onfiuion in
) ls (
    ho    ⚠️  zu onfi issin - soin fo bup
    opy "OUPIONLNUPBUP\zuonfi.py" . >nul 2>nul
)

if xis "vnuissys.py" (
    ho    ✅ Vnui s sys in
) ls (
    ho    ⚠️  Vnui sys issin - soin fo bup
    opy "OUPIONLNUPBUP\vnuissys.py" . >nul 2>nul
)

ho.
ho ========================================
ho   OUPION LNUP OPL
ho ========================================
ho.
ho 📊 LNUP SUY:
ho    • Suiy violions: Fix
ho    • i ifs: ov
ho    • onfiuion: Su
ho    • o fils: Po
ho    • Bup loion: OUPIONLNUPBUP\
ho.
ho 🚀 You L.I.F.. Plfo is now ln n su!
ho    y fo pouion ployn.
ho.

 Opionl: un plfo vliion
hoi / YN / "un plfo vliion s"
if olvl 2 oo :n
if olvl 1 oo :vli

:vli
ho unnin plfo vliion...
pyhon - "
y:
    ipo zuonfi
    fo vnuissys ipo VnuisSys
    pin('✅ Plfo vliion: PSS')
    pin('✅ ll iil syss opionl')
xp xpion s :
    pin(f'⚠️  Vliion wnin: {}')
    pin('💡 Plfo y sill b funionl')
"

:n
ho.
ho Pss ny y o oninu...
pus >nul