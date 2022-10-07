impacts = {
    "acd": ("EF v3.0", "acidification", "accumulated exceedance (ae)"),
    "ozd": ("EF v3.0", "ozone depletion", "ozone depletion potential (ODP) "),
    "cch": ("EF v3.0", "climate change", "global warming potential (GWP100)"),    
    "fwe": (
        "EF v3.0",
        "eutrophication: freshwater",
        "fraction of nutrients reaching freshwater end compartment (P)",
    ),
    "swe": (
        "EF v3.0",
        "eutrophication: marine",
        "fraction of nutrients reaching marine end compartment (N)",
    ),
    "tre": ("EF v3.0", "eutrophication: terrestrial", "accumulated exceedance (AE) "),
    "pco": (
        "EF v3.0",
        "photochemical ozone formation: human health",
        "tropospheric ozone concentration increase",
    ),
    "pma": ("EF v3.0", "particulate matter formation", "impact on human health"),
    "ior": (
        "EF v3.0",
        "ionising radiation: human health",
        "human exposure efficiency relative to u235",
    ),
    "fru": (
        "EF v3.0",
        "energy resources: non-renewable",
        "abiotic depletion potential (ADP): fossil fuels",
    ),
    "mru": (
        "EF v3.0",
        "material resources: metals/minerals",
        "abiotic depletion potential (ADP): elements (ultimate reserves)",
    ),
    "ldu": ("EF v3.0", "land use", "soil quality index"),
    "wtu": (
        "EF v3.0",
        "water use",
        "user deprivation potential (deprivation-weighted water consumption)",
    ),
    "etf": (
        "EF v3.0",
        "ecotoxicity: freshwater",
        "comparative toxic unit for ecosystems (CTUe) ",
    ),
    "htc": (
        "EF v3.0",
        "human toxicity: carcinogenic",
        "comparative toxic unit for human (CTUh) ",
    ),
    "htn": (
        "EF v3.0",
        "human toxicity: non-carcinogenic",
        "comparative toxic unit for human (CTUh) ",
    ),
}

"""Correspondance between the impact name we chose in our export (the trigrams) and the name in the Agribalyse_synthese.

The key is the Agribalyse_synthese name, the value is a tuple (trigram, multiplier),
with `multiplier` the unit (eg E-06) in the Agribalyse_synthese name.

"""
impacts_to_synthese = {
    # TODO: find/add the equivalent in `impacts`
    # "Score unique EF (mPt/kg de produit)": "",
    "Changement climatique (kg CO2 eq/kg de produit)": ("cch", 1),
    "Appauvrissement de la couche d'ozone (E-06 kg CVC11 eq/kg de produit)": (
        "ozd",
        0.000001,
    ),
    "Rayonnements ionisants (kBq U-235 eq/kg de produit)": ("ior", 1),
    "Formation photochimique d'ozone (E-03 kg NMVOC eq/kg de produit)": ("pco", 0.001),
    "Particules (E-06 disease inc./kg de produit)": ("pma", 0.000001),
    "Acidification terrestre et eaux douces (mol H+ eq/kg de produit)": ("acd", 1),
    "Eutrophisation terreste (mol N eq/kg de produit)": ("tre", 1),
    "Eutrophisation eaux douces (E-03 kg P eq/kg de produit)": ("fwe", 0.001),
    "Eutrophisation marine (E-03 kg N eq/kg de produit)": ("swe", 0.001),
    "Utilisation du sol (Pt/kg de produit)": ("ldu", 1),
    "Écotoxicité pour écosystèmes aquatiques d'eau douce (CTUe/kg de produit)": (
        "etf",
        1,
    ),
    "Épuisement des ressources eau (m3 depriv./kg de produit)": ("wtu", 1),
    "Épuisement des ressources énergétiques (MJ/kg de produit)": ("fru", 1),
    "Épuisement des ressources minéraux (E-06 kg Sb eq/kg de produit)": (
        "mru",
        0.000001,
    ),
}

impacts_ecobalyse = {
    "acd": {
        "source": {"label": "Base Impacts", "url": "https://base-impacts.ademe.fr/"},
        "label_en": "Acidification",
        "label_fr": "Acidification",
        "unit_fr": "mol éq. H+",
        "unit_en": "mol H+ eq",
        "short_unit": "molH+e",
        "description_en": "Indicator of the **potential acidification of soils and water** due to the release of gases such as nitrogen oxides and sulphur oxides.",
        "description_fr": "Indicateur de l'**acidification potentielle des sols et des eaux** due à la libération de gaz tels que les oxydes d'azote et les oxydes de soufre.\n\nCet indicateur se mesure en mol (quantité de matière) d'équivalent d'ions hydrogène (`H+`).",
        "primary": True,
        "quality": 2,
        "pef": {"color": "#ff1493", "normalization": 5.55695e1, "weighting": 0.062},
        "scopes": ["textile", "food"],
    },
    "ozd": {
        "source": {"label": "Base Impacts", "url": "https://base-impacts.ademe.fr/"},
        "label_en": "Ozone depletion",
        "label_fr": "Appauvrissement de la couche d'ozone",
        "unit_fr": "kg éq. CFC 11",
        "unit_en": "kg CVC11 eq",
        "short_unit": "kgCVC11e",
        "description_en": "Indicator of **emissions to air** that cause the **destruction of the stratospheric ozone layer**.",
        "description_fr": "La couche d'ozone est située en haute altitude dans l'atmosphère, elle protège des rayons ultra-violets solaires. Son appauvrissement augmente l'**exposition de l'ensemble des êtres vivants à ces radiations négatives** (cancérigènes en particulier).\n\nCet indicateur se mesure en kg d'équivalent `CFC 11`, le CFC 11 (trichlorofluorométhane) étant l'un des gaz responsable de l'appauvrissement de la couche d'ozone.",
        "primary": True,
        "quality": 1,
        "pef": {"color": "#800080", "normalization": 5.3648e-2, "weighting": 0.0631},
        "scopes": ["textile", "food"],
    },
    "cch": {
        "source": {"label": "Base Impacts", "url": "https://base-impacts.ademe.fr/"},
        "label_en": "Climate change",
        "label_fr": "Changement climatique",
        "unit_fr": "kg éq. CO₂",
        "unit_en": "kg CO₂ eq",
        "short_unit": "kgCO₂e",
        "description_en": "Indicator of **potential global warming** due to **emissions of greenhouse gases to air**. Divided into 3 subcategories based on the emission source: (1) fossil resources, (2) bio-based resources and (3) land use change.",
        "description_fr": "Indicateur le plus connu, correspond à la **modification du climat**, affectant l'écosystème global.\n\nCet indicateur se mesure en kg équivalent `CO₂`, le principal gaz à effet de serre.",
        "primary": True,
        "quality": 1,
        "pef": {"color": "#800000", "normalization": 8.09553e3, "weighting": 0.2106},
        "scopes": ["textile", "food"],
    },
    "fwe": {
        "source": {"label": "Base Impacts", "url": "https://base-impacts.ademe.fr/"},
        "label_en": "Freshwater Eutrophication",
        "label_fr": "Eutrophisation eaux douces",
        "unit_fr": "kg éq. P",
        "unit_en": "kg P eq",
        "description_en": "Indicator of the **enrichment of the fresh water ecosystem** with nutritional elements, due to the emission of nitrogen or phosphor containing compounds.",
        "description_fr": "Indicateur correspondant à un **enrichissement excessif des milieux naturels en nutriments**, ce qui conduit à une prolifération et une asphyxie (zone morte). C'est ce phénomène qui est à l'origine des algues vertes. On peut le retrouver en rivière et en lac également.\n\nCet indicateur se mesure en kg d'équivalent Phosphore (`P`), le phosphore étant l'un des éléments responsables de l'eutrophisation des eaux douces.",
        "short_unit": "kgPe",
        "primary": True,
        "quality": 2,
        "pef": {"color": "#1f7dca", "normalization": 1.60685, "weighting": 0.028},
        "scopes": ["textile", "food"],
    },
    "swe": {
        "source": {"label": "Base Impacts", "url": "https://base-impacts.ademe.fr/"},
        "label_en": "Marine eutrophication",
        "label_fr": "Eutrophisation marine",
        "unit_fr": "kg éq. N",
        "unit_en": "kg N eq",
        "description_en": "Indicator of the **enrichment of the marine ecosystem** with nutritional elements, due to the emission of nitrogen containing compounds.",
        "description_fr": "Indicateur correspondant à un **enrichissement excessif des milieux naturels en nutriments**, ce qui conduit à une prolifération et une asphyxie (zone morte). C'est ce phénomène qui est à l'origine des algues vertes.\n\nCet indicateur se mesure en kg d'équivalent azote (`N`), l'azote étant l'un des éléments responsables de l'eutrophisation des eaux marines.",
        "short_unit": "kgNe",
        "primary": True,
        "quality": 2,
        "pef": {"color": "#000080", "normalization": 1.95e1, "weighting": 0.0296},
        "scopes": ["textile", "food"],
    },
    "tre": {
        "source": {"label": "Base Impacts", "url": "https://base-impacts.ademe.fr/"},
        "label_en": "Terrestrial eutrophication",
        "label_fr": "Eutrophisation terrestre",
        "unit_fr": "mol éq. N",
        "unit_en": "mol N eq",
        "description_en": "Indicator of the **enrichment of the terrestrial ecosystem** with nutritional elements, due to the emission of nitrogen containing compounds.",
        "description_fr": "Comme dans l'eau, l'eutrophisation terrestre correspond à un **enrichissement excessif du milieu**, en azote en particulier, conduisant a un déséquilibre et un appauvrissement de l'écosystème. Ceci concerne principalement les sols agricoles.\n\nCet indicateur se mesure en mol d'équivalent azote (`N`).",
        "short_unit": "molNe",
        "primary": True,
        "quality": 2,
        "pef": {"color": "#20b2aa", "normalization": 1.76755e2, "weighting": 0.0371},
        "scopes": ["textile", "food"],
    },
    "pco": {
        "source": {"label": "Base Impacts", "url": "https://base-impacts.ademe.fr/"},
        "label_en": "Photochemical ozone formation",
        "label_fr": "Formation d'ozone photochimique",
        "unit_fr": "kg éq. COVNM",
        "unit_en": "kg NMVOC eq",
        "description_en": "Indicator of **emissions of gases** that affect the creation of photochemical ozone in the lower atmosphere (smog) catalysed by sunlight.",
        "description_fr": "Indicateur correspondant à la **dégradation de la qualité de l'air**, principalement via la formation de brouillard de basse altitude nommé *smog*. Il a des conséquences néfastes sur la santé.\n\nCet indicateur se mesure en kg d'équivalent Composés Organiques Volatiles Non Méthaniques (`COVNM`), un ensemble de composés organiques (alcools, aromatiques,...) contribuant à la formation d'ozone photochimique.",
        "short_unit": "kgNMVOCe",
        "primary": True,
        "quality": 1,
        "pef": {"color": "#da70d6", "normalization": 4.06014e1, "weighting": 0.0478},
        "scopes": ["textile", "food"],
    },
    "pma": {
        "source": {"label": "Base Impacts", "url": "https://base-impacts.ademe.fr/"},
        "label_en": "Particulate matter",
        "label_fr": "Particules",
        "unit_fr": "incidence de maladie",
        "unit_en": "disease inc.",
        "description_en": "Indicator of the potential **incidence of disease** due to particulate matter emissions.",
        "description_fr": "Indicateur correspondant aux **effets négatifs sur la santé humaine** causés par les émissions de particules (`PM`) et de leurs précurseurs (`NOx`, `SOx`, `NH3`).\n\nCet indicateur se mesure en incidence de maladie supplémentaire due aux particules",
        "short_unit": "dis.inc.",
        "primary": True,
        "quality": 2,
        "pef": {"color": "#696969", "normalization": 5.95387e-4, "weighting": 0.0896},
        "scopes": ["textile", "food"],
    },
    "ior": {
        "source": {"label": "Base Impacts", "url": "https://base-impacts.ademe.fr/"},
        "label_en": "Ionising radiation",
        "label_fr": "Radiations ionisantes",
        "unit_fr": "éq. kBq U235",
        "unit_en": "kBq U-235 eq",
        "description_en": "Damage to **human health and ecosystems** linked to the emissions of radionuclides.",
        "description_fr": "Indicateur correspondant aux dommages pour la **santé humaine et les écosystèmes** liés aux émissions de radionucléides.\n\nIl se mesure en kilobecquerel d'equivalent `Uranium 235`.",
        "short_unit": "kBqU235e",
        "primary": True,
        "quality": 2,
        "pef": {"color": "#ffd700", "normalization": 4.22016e3, "weighting": 0.0501},
        "scopes": ["textile", "food"],
    },
    "fru": {
        "source": {"label": "Base Impacts", "url": "https://base-impacts.ademe.fr/"},
        "label_en": "Fossile resource use",
        "label_fr": "Utilisation de ressources fossiles",
        "unit_fr": "MJ",
        "unit_en": "MJ",
        "description_en": "Indicator of the **depletion of natural fossil** fuel resources (e.g. natural gas, coal, oil).",
        "description_fr": "Indicateur de l'**épuisement des ressources naturelles en combustibles fossiles** (gaz, charbon, pétrole).\n\nIl se mesure en mégajoules (`MJ`), la quantité d'énergie fossile utilisée.",
        "short_unit": "MJ",
        "primary": True,
        "quality": 3,
        "pef": {"color": "#000000", "normalization": 6.50043e4, "weighting": 0.0832},
        "scopes": ["textile", "food"],
    },
    "mru": {
        "source": {"label": "Base Impacts", "url": "https://base-impacts.ademe.fr/"},
        "label_en": "Minerals and metal resource use",
        "label_fr": "Utilisation de ressources minérales et métalliques",
        "unit_fr": "kg éq. Sb",
        "unit_en": "kg Sb eq",
        "description_en": "Indicator of the **depletion of natural non-fossil resources**.",
        "description_fr": "Indicateur de l'**épuisement des ressources naturelles non fossiles**.\n\nIl se mesure en kg d'équivalent d'antimoine (`Sb`) (élément métallique).",
        "short_unit": "kgSbe",
        "primary": True,
        "quality": 3,
        "pef": {"color": "#a9a9a9", "normalization": 6.36403e-2, "weighting": 0.0755},
        "scopes": ["textile", "food"],
    },
    "ldu": {
        "source": {"label": "Base Impacts", "url": "https://base-impacts.ademe.fr/"},
        "label_en": "Land use",
        "label_fr": "Utilisation des sols",
        "unit_fr": "sans dimension (Pt)",
        "unit_en": "Pt",
        "description_en": "Measure of the changes in **soil quality** (Biotic production, Erosion resistance, Mechanical filtration).",
        "description_fr": "Mesure de l'évolution de la **qualité des sols** (production biotique, résistance à l'érosion, filtration mécanique).\n\nCet indicateur n'a pas de dimension, il se mesure en Points (`Pt`).",
        "short_unit": "Pt",
        "primary": True,
        "quality": 3,
        "pef": {"color": "#006400", "normalization": 8.19498e5, "weighting": 0.0794},
        "scopes": ["textile", "food"],
    },
    "pef": {
        "source": {"label": "Base Impacts", "url": "https://base-impacts.ademe.fr/"},
        "label_en": "PEF Score",
        "label_fr": "Score PEF",
        "unit_fr": "mPt PEF",
        "unit_en": "mPt PEF",
        "description_en": "Aggregated impact : sum of the weighted and normalized impact of all environmental impact categories according to the PEF methodology.",
        "description_fr": "Impact *agrégé* : somme des impacts **normalisés** et **pondérés** de chaque catégorie d'impact selon la méthode *single score* du PEF. 12 impacts différents pris en compte à ce stade. 4 encore à ajouter.\n\nCet indicateur n'a **pas de dimension**, il se mesure en **Points (`Pt`)** ou en **milliPoints (`mPt`)** avec `1 Pt = 1000 mPt`. `1 Pt` correspond à l'impact total d'un européen sur une année.",
        "short_unit": "mPt PEF",
        "primary": True,
        "quality": None,
        "pef": None,
        "scopes": ["textile", "food"],
    },
    "wtu": {
        "source": {
            "label": "Kering",
            "url": "https://kering-group.opendatasoft.com/explore/dataset/raw-material-intensities-2020/information/",
        },
        "label_en": "Water use",
        "label_fr": "Utilisation de ressources en eau",
        "unit_fr": "m³",
        "unit_en": "m³",
        "description_en": "Indicator of water consumption contributing to the depletion of available water. The impact is expressed in **cubic meters (`m³`)** of water use",
        "description_fr": "Indicateur de la consommation d'eau et son épuisement dans certaines régions. **À ce stade, elle n'est prise en compte que pour l'étape “Matière & Filature”.**\n\nCet indicateur se mesure en **mètre cube (`m³`)** d'eau consommé.",
        "short_unit": "m³",
        "primary": True,
        "quality": 0,
        "pef": {"color": "#00ffff", "normalization": 1.14687e4, "weighting": 0.0851},
        "scopes": ["textile", "food"],
    },
    "etf": {
        "source": {"label": "Agribalyse", "url": "https://agribalyse.ademe.fr/"},
        "label_en": "Ecotoxicity: freshwater",
        "label_fr": "Écotoxicité de l'eau douce",
        "unit_fr": "CTUe",
        "unit_en": "CTUe",
        "description_en": "Indicator of freshwater ecotoxicity. The unit of measurement is Comparative Toxic Unit for ecosystems (CTUe)",
        "description_fr": "Indicateur d'écotoxicité pour écosystèmes aquatiques d'eau douce. Cet indicateur se mesure en Comparative Toxic Unit for ecosystems (CTUe)",
        "short_unit": "CTUe",
        "primary": True,
        "quality": 0,
        "pef": {"color": "#03A764", "normalization": 4.27e4, "weighting": 0.0192},
        "scopes": ["food"],
    },
    "htc": {
        "source": {"label": "Agribalyse", "url": "https://agribalyse.ademe.fr/"},
        "label_en": "Human toxicity: carcinogenic",
        "label_fr": "Toxicité humaine - cancer",
        "unit_fr": "CTUh",
        "unit_en": "CTUh",
        "description_en": "Indicator of carcinogenic toxicity for humans. The unit of measurement is Comparative toxic unit for humans (CTUh)",
        "description_fr": "Indicateur de toxicité cancérigène pour l'homme. Cet indicateur se mesure en Comparative Toxic Unit for humans (CTUh)",
        "short_unit": "CTUh",
        "primary": True,
        "quality": 0,
        "pef": {"color": "#A77C2B", "normalization": 1.69e-5, "weighting": 0.0213},
        "scopes": ["food"],
    },
    "htn": {
        "source": {"label": "Agribalyse", "url": "https://agribalyse.ademe.fr/"},
        "label_en": "Human toxicity: non-carcinogenic",
        "label_fr": "Toxicité humaine - non-cancer",
        "unit_fr": "CTUh",
        "unit_en": "CTUh",
        "description_en": "Indicator of non-carcinogenic toxicity for humans. The unit of measurement is Comparative toxic unit for humans (CTUh)",
        "description_fr": "Indicateur de toxicité non cancérigène pour l'homme. Cet indicateur se mesure en Comparative Toxic Unit for humans (CTUh)",
        "short_unit": "CTUh",
        "primary": True,
        "quality": 0,
        "pef": {"color": "#FFA907", "normalization": 1.2874e-4, "weighting": 0.0184},
        "scopes": ["food"],
    },
}
