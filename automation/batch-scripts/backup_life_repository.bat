@ho off
 ========================================
 L.I.F.. posioy Poion Sys
 uo Bup & oupion Pvnion
 ========================================

s POPH=:\Uss\Sio Py Boull\.zu\SiLIF-lif-zu-sys\.i\hoos\SiLIF-lif-zu-sys
s SOPBUP=:\Uss\%USN%\sop\LIFposioyBups
s ISP=%:~10,4%%:~4,2%%:~7,2%%i:~0,2%%i:~3,2%
s ISP=%ISP: =0%

ho ===== L.I.F.. posioy Poion Sys =====
ho Sin bup poss  %% %i%

  bup ioy suu
ho in bup iois...
if no xis "%SOPBUP%" i "%SOPBUP%"
if no xis "%SOPBUP%\ily" i "%SOPBUP%\ily"
if no xis "%SOPBUP%\wly" i "%SOPBUP%\wly"
if no xis "%SOPBUP%\ibunls" i "%SOPBUP%\ibunls"
if no xis "%SOPBUP%\hlhpos" i "%SOPBUP%\hlhpos"

 / "%POPH%"

 Hlh h bfo bup
ho unnin p-bup hlh h...
i fs --full > "%SOPBUP%\hlhpos\hlh%ISP%.x" 2>&1
s "FSO=%OLVL%"
if no "%FSO%"=="0" (
    ho WNIN: posioy hlh issus !
    ho h %SOPBUP%\hlhpos\hlh%ISP%.x
)

  i bunl (opl posioy bup)
ho in i bunl bup...
i bunl  "%SOPBUP%\ibunls\lifpo%ISP%.bunl" --ll
s "BUNLO=%OLVL%"
if "%BUNLO%"=="0" (
    ho ✅ i bunl  sussfully
) ls (
    ho ❌ i bunl ion fil
)

  fil sys bup (xluin l/p fils)
ho in fil sys bup...
oboopy "%POPH%" "%SOPBUP%\ily\lifpo%ISP%" /I /X ".i\objs\p" "pyh" ".ypyh" ".vnv" "noouls" /XF "*.p" "*.lo" "hubh*" /:3 /W:5 /NFL /NL /NP

 p only ls 7 ily bups n 4 wly bups
ho lnin ol bups...
fofils /p "%SOPBUP%\ily" / lifpo* / -7 / " / i /s /q @ph" 2>nul
fofils /p "%SOPBUP%\ibunls" / *.bunl / -28 / " / l /q @ph" 2>nul

  bup suy
ho in bup suy...
ho Bup opl  %% %i% > "%SOPBUP%\lsbup.x"
ho posioy ph: %POPH% >> "%SOPBUP%\lsbup.x"
ho Bunl loion: %SOPBUP%\ibunls\lifpo%ISP%.bunl >> "%SOPBUP%\lsbup.x"
ho Fils loion: %SOPBUP%\ily\lifpo%ISP% >> "%SOPBUP%\lsbup.x"

ho.
ho ===== Bup opl =====
ho sop bup loion: %SOPBUP%
ho Ls bunl: lifpo%ISP%.bunl
ho.
ho o so fo bunl: i lon [bunlph] [nwfol]
ho o vify bup: un vifybups.b