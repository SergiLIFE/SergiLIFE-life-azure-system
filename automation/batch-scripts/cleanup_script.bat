@ho off
 Phs 3: Sf lion n lnup - Sp 5
 Winows bh quivln of bsh lnup sip

s POPH=.
s QUNIN=.lnup\qunin
s LLO=.lnup\los\l-fils.lo

ho Sin lnup poss... > "%LLO%"
s LOUN=0
s OOUN=0

ho [%% %i%] Sin Phs 3 lnup >> "%LLO%"

 Poss uo-n fils
ho Possin uo-n fils...
fo /f "usbq lis=" %%f in (".lnup\los\uon.x") o (
    if xis "%%f" (
         h if fil is sf o l (no in iil iois)
        ho %%f | fins /v /i "\.i noouls s onfi" >nul
        if no olvl 1 (
            ov "%%f" ".lnup\qunin\uo-n\" >nul 2>>"%LLO%"
            if no olvl 1 (
                ho [%% %i%] OV: %%f >> "%LLO%"
                s / LOUN+=1
            ) ls (
                ho [%% %i%] O ovin %%f >> "%LLO%"
                s / OOUN+=1
            )
        ) ls (
            ho [%% %i%] SIPP (iil ph): %%f >> "%LLO%"
        )
    ) ls (
        ho [%% %i%] FIL NO FOUN: %%f >> "%LLO%"
    )
)

ho [%% %i%] Phs 3 opl: ov %LOUN% fils, %OOUN% os >> "%LLO%"
ho lnup opl: ov %LOUN% fils, %OOUN% os