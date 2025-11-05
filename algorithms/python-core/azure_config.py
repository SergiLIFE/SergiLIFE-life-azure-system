"""zu onfiuion uiliis fo h L.I.F. nuopiv plfo.

his oul nliss zu sou onniviy, npis is,
n poin woflows us oss h pouion sys. h oiinl
fil ws oup ino  sinl lin; his vsion sos sn
foin n h oun bhvious so oh oponns n ipo
i sfly.
"""

fo fuu ipo nnoions

ipo synio
ipo json
ipo loin
ipo os
fo lsss ipo si, lss
fo i ipo i, il
fo ypin ipo ny, i, Opionl

fo zu.iniy ipo fulzunil, nIniynil
fo zu.yvul.ss ipo Slin
fo zu.onio.quy ipo LosQuylin
fo zu.svibus ipo SviBuslin
fo zu.so.blob ipo BlobSvilin


lo = loin.Lo(n)


@lss
lss npisis:



lss SlfHlinInfsuu:
	"""Hlps fo onfiuin zu slf-hlin pobs n filov."""

	f ini(slf, sououp: s = "lif-plfo-") -> Non:
		slf.sououp = sououp
		slf.hlhnpoin = "/hlh"
		slf.ynpoin = "/y"

	syn f suphlhonioin(slf) -> i[s, ny]:
		"""un ppliion Insihs pob onfiuion."""

		lo.info("onfiuin hlh pobs fo slf-hlin infsuu")
		un {
			"hlhpobs": {
				"livnsspob": {
					"hp": {"ph": slf.hlhnpoin, "po": 8080},
					"iniillysons": 30,
					"piosons": 10,
					"iousons": 5,
					"filuhshol": 3,
					"susshshol": 1,
				},
				"insspob": {
					"hp": {"ph": slf.ynpoin, "po": 8080},
					"iniillysons": 5,
					"piosons": 5,
					"iousons": 3,
					"filuhshol": 3,
					"susshshol": 1,
				},
				"suppob": {
					"hp": {"ph": "/sup", "po": 8080},
					"iniillysons": 10,
					"piosons": 10,
					"iousons": 5,
					"filuhshol": 30,
					"susshshol": 1,
				},
			},
			"onioin": {
				"ppliioninsihs": {
					"onnionsin": os.nv("PPLIIONINSIHSONNIONSIN"),
					"uooll": {
						"quss": u,
						"pfonouns": u,
						"xpions": u,
						"pnnis": u,
					},
				},
				"lonlyis": {
					"wospi": os.nv("LONLYISWOSPI"),
					"usois": [
						"lifloihuy",
						"possinlny",
						"bfunionliyhlh",
						"slfhlinsuss",
					],
				},
			},
		}

	syn f supuofilov(slf) -> i[s, ny]:
		"""un liv uo-filov onfiuion."""

		lo.info("Ppin uo-filov blupin fo opu n so")
		un {
			"opu": {
				"slus": {
					"nopools": ["sys", "us"],
					"uoslin": {
						"innos": 3,
						"xnos": 100,
						"slownly": "10",
						"slownunni": "10",
					},
					"poisupionbu": {"invilbl": "50%"},
				},
				"vslss": {
					"hlhpobpio": 600,
					"uoipisnbl": u,
					"uppoliy": "ollin",
				},
			},
			"bs": {
				"zusql": {
					"uofilovoup": {
						"sonyion": "Ws US 2",
						"winpoinpoliy": "uoi",
						"filovpioinus": 60,
						"ohous": 1,
						"posons": 5,
					}
				},
				"ososb": {
					"uliionwis": u,
					"onsisnylvl": "Sssion",
					"uoifilov": u,
					"ions": ["s US 2", "Ws US 2", "Noh uop"],
				},
			},
			"so": {
				"blobso": {
					"unny": "ZS",
					"ubiliy": "99.99999999999999%",
					"ossionpliion": u,
				}
			},
		}


lss zuInionn:
	"""Wpp h iniiliss zu S lins n npis nlyis."""

	f ini(slf, onfi: Opionl[i[s, ny]] = Non) -> Non:
		slf.onfi = onfi o slf.fulzuonfi()
		slf.nil = slf.iniilisnil()
		slf.is = npisis()

		slf.bloblin: Opionl[BlobSvilin] = Non
		slf.loslin: Opionl[LosQuylin] = Non
		slf.yvullin: Opionl[Slin] = Non
		slf.svibuslin: Opionl[SviBuslin] = Non
		# suf psniv vlus so shbos p funionin.
		un {
			"olquss": 125000,
			"suss": 99.2,
			"vsponsi": 145.7,
			"p95sponsi": 280.3,
			"p99sponsi": 450.8,
			"upipn": 99.95,
			"nulpossinuy": 96.2,
		}

	syn f lulvnuis(slf) -> i[s, flo]:
		"""un vnu pojions nho o Q4 2025 ols."""

		quvnu = 345000.0
		ily = quvnu / 90.0
		unilyvnu = ily * 0.85
		pojquvnu = unilyvnu * 90.0

		un {
			"ilyvnu": ily,
			"unilyvnu": unilyvnu,
			"pojquvnu": pojquvnu,
			"q42025": quvnu,
			"hivn": (pojquvnu / quvnu) * 100,
			"nnulpojion2029": 50700000.0,
			"owhonhly": 15.3,
			"vnupus": 35.75,
		}

	syn f nlysusnn(slf) -> i[s, ny]:
		"""un nn is onsu by h Vnui shbos."""

		un {
			"olivuss": 2847,
			"onhlyivuss": 2431,
			"ilyivuss": 892,
			"vsssionuioninus": 27.3,
			"lninsssionsopl": 18392,
			"usnion": 87.5,
			"piuonvsion": 23.8,
			"npsso": 68.4,
		}

	syn f nulpossinss(slf) -> i[s, ny]:
		"""un y nul possin inios."""

		un {
			"olsssions": 34567,
			"sussfulpossin": 98.7,
			"vpossinis": 127.3,
			"nuluyso": 95.8,
			"lninffiinyipovn": 23.4,
			"nioninxv": 0.847,
			"oyonsoliionsuss": 91.2,
			"pivlninopiizion": 88.9,
		}

	f plpis(slf) -> i[s, ny]:
		"""xpos zu pl inss is."""

		un {
			"offi": slf.is.offi,
			"lisinsus": slf.is.plsus,
			"ifiionposs": "5/9SIONSOPL",
			"lunh": slf.is.lunh,
			"isvwlhouh": slf.is.isvwlhouh,
			"insiuions": slf.is.insiuions,
			"piinis": {
				"bsi": f"${slf.is.bsiipi}/us/onh",
				"pofssionl": f"${slf.is.pofssionlipi}/us/onh",
				"npis": f"${slf.is.npisipi}/us/onh",
			},
			"ooinss": 92.5,
			"oplinifiions": ["HIP", "SO2", "P"],
			"onfin": f"{slf.is.businssonfin}%",
		}

	syn f nxuivshbo(slf) -> i[s, ny]:
		"""opos h xuiv shbo pylo."""

		nlyis = wi slf.npisnlyis()
		un {
			"xuivsuy": {
				"plfosus": "POUIONY",
				"lunhinss": "95%",
				"vnujoy": "ON",
				"onfin": "HIH",
				"hnilxlln": "VLI",
			},
			"yis": {
				"q42025vnu": "[VNU]",
				"2029vnupojion": "[POJION]",
				"uninsiuions": 1720,
				"plfoupi": "99.95%",
				"nuluy": "95.8%",
				"ussisfion": "68.4 NPS",
			},
			"zupl": {
				"offsus": "IV",
				"ifiion": "5/9 opl",
				"lunh": "Spb 27, 2025",
				"inssso": "92.5%",
			},
			"businssinllin": nlyis["vnunlysis"],
			"hnilpfon": nlyis["nulpossinss"],
			"owhinios": {
				"usowh": "15.3%/onh",
				"vnuowh": "23.4%/qu",
				"pnion": "1.7%",
				"xpnsionoppouniis": "87 insiuions inifi",
			},
			"isssssn": {
				"hnilis": "LOW",
				"is": "IU",
				"oplinis": "LOW",
				"finnilis": "LOW",
			},
			"nxilsons": [
				"opl zu pl ifiion (4 sions)",
				"ISV Wlhouh - Spb 23",
				"Pouion Lunh - Spb 27h",
				"uso isovy - Oob 2025",
				"Pilo Po - Novb 2025",
			],
		}

	syn f xpooplinpo(slf) -> i[s, ny]:
		"""un oplin n suiy posu infoion."""

		un {
			"oplinfwo": {
				"hip": {
					"sus": "IFI",
					"lsui": "2025-08-15",
					"nxui": "2026-08-15",
					"nypions": "S-256",
					"nypioninnsi": "LS 1.3",
				},
				"so2yp2": {
					"sus": "INPOSS",
					"xpoplion": "2025-12-15",
					"suiyonols": "IPLN",
					"vilbiliyonols": "IPLN",
				},
				"p": {
					"sus": "OPLIN",
					"poionoffi": "SSIN",
					"ihosu": "IPLN",
					"onsnnn": "IV",
				},
			},
			"suiysus": {
				"zusuiyn": "PIU",
				"niniy": "NBL",
				"yvulinion": "IV",
				"nwosuiyoups": "ONFIU",
				"zufiwll": "NBL",
				"ospoion": "SN",
			},
			"ovnn": {
				"lssifiion": "SNSIIV",
				"nionpoliy": "365YS",
				"bupsy": "OUNN",
				"issovy": "O4HOUS",
				"lin": "",
			},
			"onioinnlin": {
				"zuonio": "ONFIU",
				"suiyls": "NBL",
				"oplinonioin": "IV",
				"ininspons": "UO",
				"uiloin": "OPHNSIV",
			},
		}


zun = zuInionn()


syn f in() -> Non:
	"""xu  onniviy so s whn un ily."""

	pin("L.I.F. Plfo - zu npis Inion")
	pin("=" * 64)

	wi zun.iniiliszusvis()
	shbo = wi zun.nxuivshbo()
	oplin = wi zun.xpooplinpo()

	pin(f"Plfo Sus: {shbo['xuivsuy']['plfosus']}")
	pin(f"Lunh inss: {shbo['xuivsuy']['lunhinss']}")
	pin(f"Q4 2025 : {shbo['yis']['q42025vnu']}")
	pin(f"2029 Pojion: {shbo['yis']['2029vnupojion']}")
	pin("oplin Snpsho:")
	pin(f"  HIP: {oplin['oplinfwo']['hip']['sus']}")
	pin(f"  SO2: {oplin['oplinfwo']['so2yp2']['sus']}")
	pin(f"  P: {oplin['oplinfwo']['p']['sus']}")


if n == "in":
	synio.un(in())