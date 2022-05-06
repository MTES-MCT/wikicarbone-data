impacts = {
    "acd": ("EF 3.0 Method (adapted)", "Acidification"),
    "ozd": ("EF 3.0 Method (adapted)", "Ozone depletion"),
    "cch": ("EF 3.0 Method (adapted)", "Climate change"),
    "ccb": ("EF 3.0 Method (adapted)", "Climate change - Biogenic"),
    "ccf": ("EF 3.0 Method (adapted)", "Climate change - Fossil"),
    "ccl": ("EF 3.0 Method (adapted)", "Climate change - Land use and LU change"),
    "fwe": ("EF 3.0 Method (adapted)", "Eutrophication, freshwater"),
    "swe": ("EF 3.0 Method (adapted)", "Eutrophication, marine"),
    "tre": ("EF 3.0 Method (adapted)", "Eutrophication, terrestrial"),
    "pco": ("EF 3.0 Method (adapted)", "Photochemical ozone formation"),
    "pma": ("EF 3.0 Method (adapted)", "Particulate matter"),
    "ior": ("EF 3.0 Method (adapted)", "Ionising radiation"),
    "fru": ("EF 3.0 Method (adapted)", "Resource use, fossils"),
    "mru": ("EF 3.0 Method (adapted)", "Resource use, minerals and metals"),
    "ldu": ("EF 3.0 Method (adapted)", "Land use"),
    "wtu": ("EF 3.0 Method (adapted)", "Water use"),
    "etf": ("EF 3.0 Method (adapted)", "Ecotoxicity, freshwater - inorganics"),
    "htc": ("EF 3.0 Method (adapted)", "Human toxicity, cancer"),
    "htn": ("EF 3.0 Method (adapted)", "Human toxicity, non-cancer"),
}

# EF 3.0 adapted methods:
# ('EF 3.0 Method (adapted)', 'Climate change')
# ('EF 3.0 Method (adapted)', 'Ozone depletion')
# ('EF 3.0 Method (adapted)', 'Ionising radiation')
# ('EF 3.0 Method (adapted)', 'Photochemical ozone formation')
# ('EF 3.0 Method (adapted)', 'Particulate matter')
# ('EF 3.0 Method (adapted)', 'Human toxicity, non-cancer')
# ('EF 3.0 Method (adapted)', 'Human toxicity, cancer')
# ('EF 3.0 Method (adapted)', 'Acidification')
# ('EF 3.0 Method (adapted)', 'Eutrophication, freshwater')
# ('EF 3.0 Method (adapted)', 'Eutrophication, marine')
# ('EF 3.0 Method (adapted)', 'Eutrophication, terrestrial')
# ('EF 3.0 Method (adapted)', 'Ecotoxicity, freshwater')
# ('EF 3.0 Method (adapted)', 'Land use')
# ('EF 3.0 Method (adapted)', 'Water use')
# ('EF 3.0 Method (adapted)', 'Resource use, fossils')
# ('EF 3.0 Method (adapted)', 'Resource use, minerals and metals')
# ('EF 3.0 Method (adapted)', 'Climate change - Fossil')
# ('EF 3.0 Method (adapted)', 'Climate change - Biogenic')
# ('EF 3.0 Method (adapted)', 'Climate change - Land use and LU change')
# ('EF 3.0 Method (adapted)', 'Human toxicity, non-cancer - organics')
# ('EF 3.0 Method (adapted)', 'Human toxicity, non-cancer - inorganics')
# ('EF 3.0 Method (adapted)', 'Human toxicity, non-cancer - metals')
# ('EF 3.0 Method (adapted)', 'Human toxicity, cancer - organics')
# ('EF 3.0 Method (adapted)', 'Human toxicity, cancer - inorganics')
# ('EF 3.0 Method (adapted)', 'Human toxicity, cancer - metals')
# ('EF 3.0 Method (adapted)', 'Ecotoxicity, freshwater - organics')
# ('EF 3.0 Method (adapted)', 'Ecotoxicity, freshwater - inorganics')
# ('EF 3.0 Method (adapted)', 'Ecotoxicity, freshwater - metals')
# ('EF 3.0 Method (adapted)', 'EF 3.0 normalization and weighting set')

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
