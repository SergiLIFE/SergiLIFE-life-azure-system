@ho off
 posioy nlysis Sip (iHub osp)
 h wosp siz, fil ouns, n ls fils

ho ==================================================
ho POSIOY NLYSIS - IHUB OSP
ho ==================================================
ho.

ho 1. HIN WOSP FIL OUNS...
ho --------------------------------------------------
 oun ol fils n iois
fo /f %%i in ('i /s /b /- ^| fin / /v ""') o s filoun=%%i
fo /f %%i in ('i /s /b / ^| fin / /v ""') o s ioun=%%i
ho ol fils: %filoun%
ho ol iois: %ioun%
ho.

ho 2. HIN LS FILS IN WOSP...
ho --------------------------------------------------
 Fin ls fils (Winows quivln)
ho Snnin fo l fils...
i /s /- /o-s | fins /v "ioy" | h -15
ho.

ho 3. HIN LNUP SUS...
ho --------------------------------------------------
if xis ".lnup" (
    ho lnup ioy foun
    if xis ".lnup\los" (
        ho lnup los vilbl:
        i /b ".lnup\los"
    )
    if xis ".lnup\qunin" (
        ho Qunin iois:
        i /b ".lnup\qunin"
    )
) ls (
    ho No lnup ioy foun
)
ho.

ho 4. HIN FIL PNS...
ho --------------------------------------------------
ho uo-n fil ouns:
ho OPHNSIV fils:
fo /f %%i in ('i /s /b *OPHNSIV* 2^>nul ^| fin / /v ""') o ho   OPHNSIV: %%i fils
ho NY fils:
fo /f %%i in ('i /s /b *NY* 2^>nul ^| fin / /v ""') o ho   NY: %%i fils
ho PLOY fils:
fo /f %%i in ('i /s /b *PLOY* 2^>nul ^| fin / /v ""') o ho   PLOY: %%i fils
ho O fils:
fo /f %%i in ('i /s /b *O* 2^>nul ^| fin / /v ""') o ho   O: %%i fils
ho.

ho 5. WOSP HLH H...
ho --------------------------------------------------
if xis "quins.x" (ho ✅ quins.x foun) ls (ho ❌ quins.x issin)
if xis "zuonfi.py" (ho ✅ zu onfi foun) ls (ho ❌ zu onfi issin)
if xis ".iino" (ho ✅ .iino foun) ls (ho ❌ .iino issin)
if xis "." (ho ✅ . foun) ls (ho ❌ . issin)
ho.

ho ==================================================
ho POSIOY NLYSIS OPL
ho ==================================================
pus