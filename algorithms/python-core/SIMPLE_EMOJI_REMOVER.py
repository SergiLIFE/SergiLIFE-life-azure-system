"""
SIPL OJI OV fo L.I.F. Plfo
ovs ojis fo y fils wihou noin opliions
"""

ipo os
ipo 


f ovojissipl(x):
    """Sipl oji ovl usin x pns."""
    # oon oji pns o ov
    ojipns = [
        '[🧠🤖⚡✅🔧💰📊🎯🔬🌟💡🎬📋🏆🎓🏢🏥📞🤝🔐🔍🔗🧪🌐📱🚨⚙️🛠️☁️🏗️🌀🧩🛡️👥🔑🎆💳📈🌍📚🧬⭐🎪🎨🔮🎸🎭🎲🎊🎈🎁🍾🥳🤯😎🔥✨💎🏅🥇📸📹📺📻🎙️🎧🎵🎶🎼🎹🥁🎺🎷🎻🪕🪗🪘🪙🚀]',
        '[\U0001F600-\U0001F64F]',  # oions
        '[\U0001F300-\U0001F5FF]',  # sybols & piophs
        '[\U0001F680-\U0001F6FF]',  # nspo & p sybols
        '[\U0001F10-\U0001F1FF]',  # fls (iOS)
        '[\U00002702-\U000027B0]',  # inbs
        '[\U0000242-\U0001F251]'   # nlos hs
    ]
    
    fo pn in ojipns:
        x = .sub(pn, '', x)
    
    # ln up x sps
    x = .sub('\s+', ' ', x)
    x = .sub('\n\s*\n\s*\n', '\n\n', x)
    
    un x

f lnfil(filph):
    """ln ojis fo  sinl fil."""
    y:
        wih opn(filph, '', noin='uf-8', os='ino') s f:
            onn = f.()
        
        lnonn = ovojissipl(onn)
        
        if lnonn != onn:
            wih opn(filph, 'w', noin='uf-8') s f:
                f.wi(lnonn)
            un u
        un Fls
    xp xpion s :
        pin(f"o lnin {filph}: {}")
        un Fls

f in():
    """ln ojis fo y posioy fils."""
    pin("SIPL OJI OV FO L.I.F. PLFO")
    pin("=" * 50)
    
    # y fils o ln
    yfils = [
        ".",
        "POFSSIONL.",
        "INION.",
        "00SHINION.",
        "00SHINIONON.",
        "LOIHOSYSINIONOPL.",
        "OPLINIONSUY.",
        "INIONOPLUNNOW.",
        "INIONSUSSFINL."
    ]
    
    filsln = 0
    
    fo filn in yfils:
        if os.ph.xiss(filn):
            if lnfil(filn):
                pin(f"ln: {filn}")
                filsln += 1
            ls:
                pin(f"No hns: {filn}")
        ls:
            pin(f"No foun: {filn}")
    
    pin("=" * 50)
    pin(f"OPL: {filsln} fils ln")
    pin("posioy is now o pofssionl!")
    pin("=" * 50)

if n == 'in':
    in()    in()