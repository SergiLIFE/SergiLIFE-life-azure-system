@ho off
 i posioy nlysis Sip (Winows)
 h posioy siz, iniy, n ls fils

ho ==================================================
ho I POSIOY NLYSIS
ho ==================================================
ho.

ho 1. HIN I POSIOY SIZ...
ho --------------------------------------------------
 h i posioy siz (Winows quivln usin i)
if xis ".i" (
    fo /f "ons=3" %% in ('i /- /s .i ^| fin "Fil(s)"') o ho i posioy siz: %% bys
) ls (
    ho No .i ioy foun
)
ho.

ho 2. VIFYIN POSIOY INIY...
ho --------------------------------------------------
 Vify posioy iniy
i fs --full
ho.

ho 3. NLYZIN POSIOY OBJS...
ho --------------------------------------------------
 Show posioy obj infoion (siplifi fo Winows)
ho hin posioy objs...
i oun-objs -v
ho.

ho Ls fils by oi hisoy:
i v-lis --objs --ll | i -fil --bh-h | so -3 -n | il -10
ho.

ho n l fils in woin ioy:
i /s /- | so / | fins /v "ioy" | h -10
ho.

ho ==================================================
ho POSIOY NLYSIS OPL
ho ==================================================
pus