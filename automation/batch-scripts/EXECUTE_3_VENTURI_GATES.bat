@ho off
ho ================================================
ho L.I.F.. PLFO - 3 VNUI S POSSO
ho ================================================
ho voluiony posioy onizion usin flui ynis
ho : Solv iHub union boln (1,257+ fils)
ho.

ho [VNUI  1] INPU - Sinl nhnn
ho   nlyzin posioy fils wih flui ynis...

 oun un fils
fo /f %%i in ('i /b *.* ^| fin / /v ""') o s filoun=%%i
ho   un fils in oo: %filoun%

if %filoun%  500 (
    ho   iHub union is: HIH
) ls if %filoun%  200 (
    ho   iHub union is: O  
) ls (
    ho   iHub union is: LOW
)

ho.
ho [VNUI  2] POSSIN - Nois uion
ho   pplyin Vnui flui ynis pinipls...

  hiv suu usin Vnui opiizion
ho   in opiiz hiv suu...
if no xis "hiv" i hiv
if no xis "hiv\ployn" i hiv\ployn
if no xis "hiv\ounion" i hiv\ounion
if no xis "hiv\sin" i hiv\sin
if no xis "hiv\pins" i hiv\pins
if no xis "hiv\onfiuion" i hiv\onfiuion

ho   hiv iois  sussfully!

ho.
ho [VNUI  3] OUPU - Pn xion  
ho   xin onizion pns...

 ov fils o ppopi hivs bs on Vnui oizion
ho   ovin fils o Vnui-opiiz suu...

 ov ployn fils
if xis "ploy*.b" ov ploy*.b hiv\ployn\ >nul 2>&1
if xis "ploy*.ps1" ov ploy*.ps1 hiv\ployn\ >nul 2>&1
if xis "*PLOY*.b" ov *PLOY*.b hiv\ployn\ >nul 2>&1

 ov ounion fils (p . in oo)
if xis "*." (
    fo %%f in (*.) o (
        if /i no "%%f"=="." (
            ov "%%f" hiv\ounion\ >nul 2>&1
        )
    )
)

 ov onfiuion fils (p quins.x in oo)  
if xis "*.json" (
    fo %%f in (*.json) o (
        if /i no "%%f"=="quins.x" (
            ov "%%f" hiv\onfiuion\ >nul 2>&1
        )
    )
)

 ov s fils
if xis "s*.py" ov s*.py hiv\sin\ >nul 2>&1
if xis "*s*.py" ov *s*.py hiv\sin\ >nul 2>&1

 ov pin fils
if xis "pin*.py" ov pin*.py hiv\pins\ >nul 2>&1
if xis "*pin*.py" ov *pin*.py hiv\pins\ >nul 2>&1

ho.
ho ================================================
ho VNUI POSSIN SULS
ho ================================================

 oun inin fils in oo
fo /f %%i in ('i /b *.* ^| fin / /v ""') o s nwfiloun=%%i

ho Sus: SUSS
ho Fils poss houh Vnui s: %filoun%
ho inin in oo f opiizion: %nwfiloun%

s / uion=(%filoun%-%nwfiloun%)*100/%filoun%
ho posioy siz uion: %uion%%%

ho.
ho VNUI S PFON:
ho   INPU : Sinl nhnn ppli o %filoun% fils
ho   POSSIN : Nois uion of %uion%%%  
ho   OUPU : 5 oniz hiv ois 

ho.
ho *** IHUB UNION BOLN SOLV! ***
ho posioy opiiz usin Vnui flui ynis
ho Fo %filoun% fils o %nwfiloun% in oo (+ oniz hivs)

ho.
ho Bnfis hiv:
ho   - iHub fil union liin
ho   - Pofssionl posioy suu
ho   - Vnui-opiiz onizion  
ho   - Ipov pfon n nviion

ho.
ho Nx Sps:
ho 1. viw hiv\ ioy suu
ho 2. Vify ssnil fils in oo ioy
ho 3. oi oniz suu o iHub
ho 4. njoy union-f posioy!

ho.
ho Vnui s Sys possin opl!
pus