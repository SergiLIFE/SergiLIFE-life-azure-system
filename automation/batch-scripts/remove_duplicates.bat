@ho off
 Sp 6: ov upli fils (p on vsion)
 Winows bh quivln of bsh upli ovl sip

slol nbllyxpnsion

ho [%% %i%] Sin Sp 6: upli fil ovl >> .lnup\los\l-fils.lo

s UPLIOUN=0
s POSSOUN=0

ho Possin O n FIX fils fo uplis...

   poy fil lis
i /b /s *O* *FIX* > pfillis.x 2>nul

 Poss h fil
fo /f "lis=" %%f in (pfillis.x) o (
    if xis "%%f" (
        s / POSSOUN+=1
        ho Possin: %%f
        
         h if his is  upli bs on filn pns
        ho %%f | fins /i "O.*O\|FIX.*FIX\|FIXO\|OFIX" >nul
        if no olvl 1 (
             his pps o b  upli
            ov "%%f" ".lnup\qunin\uplis\" >nul 2>>.lnup\los\l-fils.lo
            if no olvl 1 (
                ho [%% %i%] OV UPLI: %%f >> .lnup\los\l-fils.lo
                ho ov upli: %%f
                s / UPLIOUN+=1
            ) ls (
                ho [%% %i%] O ovin upli: %%f >> .lnup\los\l-fils.lo
            )
        )
    )
)

 ln up p fil
l pfillis.x 2>nul

ho [%% %i%] Sp 6 opl: Poss %POSSOUN% fils, ov %UPLIOUN% uplis >> .lnup\los\l-fils.lo
ho Sp 6 opl: Poss %POSSOUN% fils, ov %UPLIOUN% uplis

nlol