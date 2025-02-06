#!/usr/bin/env python3

import argparse
import copy
import functools
import os
from os.path import join

import bw2data

from common import brightway_patch as brightway_patch
from common.import_ import (
    DB_FILES_DIR,
    import_simapro_block_csv,
    link_technosphere_by_activity_hash_ref_product,
    setup_project,
)

CURRENT_FILE_DIR = os.path.dirname(os.path.realpath(__file__))

PROJECT = "ecobalyse"
# AGRIBALYSE31 = "AGB3.1.1.20230306.CSV.zip"  # Agribalyse 3.1
AGRIBALYSE31 = "AGB3.1.1.20230306.CSV"  # Agribalyse 3.1
AGRIBALYSE32 = "AGB32beta_08082024.CSV"  # Agribalyse 3.2
GINKO = "CSV_369p_et_298chapeaux_final.csv"  # additional organic processes
# PASTOECO = "pastoeco.CSV.zip"
PASTOECO = "pastoeco.CSV"
CTCPA = "Export emballages_PACK AGB_CTCPA.CSV"
WFLDB = "WFLDB.CSV"
BIOSPHERE = "biosphere3"


ACTIVITIES = "food/activities.json"
#
ACTIVITIES_TO_CREATE = "food/activities_to_create.json"

# excluded strategies and migrations
EXCLUDED = [
    "normalize_biosphere_names",
    "fix_localized_water_flows",  # both agb and ef31 adapted have localized wf
    "simapro-water",
]

GINKO_MIGRATIONS = [
    {
        "name": "diesel-fix",
        "description": "Fix Diesel process name",
        "data": {
            "fields": ("name",),
            "data": [
                (
                    (
                        "Diesel {GLO}| market group for | Cut-off, S - Copied from ecoinvent",
                    ),
                    {
                        "name": "Diesel {GLO}| market group for | Cut-off, S - Copied from Ecoinvent U"
                    },
                )
            ],
        },
    }
]
# migrations necessary to link some remaining unlinked technosphere activities
AGRIBALYSE_MIGRATIONS = [
    {
        "name": "agb-technosphere-fixes",
        "description": "Specific technosphere fixes for Agribalyse 3",
        "data": {
            "fields": ["name", "unit"],
            "data": [
                (
                    (
                        "Wastewater, average {Europe without Switzerland}| market for wastewater, average | Cut-off, S - Copied from Ecoinvent U",
                        "l",
                    ),
                    {"unit": "m3", "multiplier": 1e-3},
                ),
                (
                    (
                        "Wastewater, from residence {RoW}| market for wastewater, from residence | Cut-off, S - Copied from Ecoinvent U",
                        "l",
                    ),
                    {"unit": "m3", "multiplier": 1e-3},
                ),
                (
                    (
                        "Heat, central or small-scale, natural gas {Europe without Switzerland}| market for heat, central or small-scale, natural gas | Cut-off, S - Copied from Ecoinvent U",
                        "kWh",
                    ),
                    {"unit": "MJ", "multiplier": 3.6},
                ),
                (
                    (
                        "Heat, district or industrial, natural gas {Europe without Switzerland}| heat production, natural gas, at industrial furnace >100kW | Cut-off, S - Copied from Ecoinvent U",
                        "kWh",
                    ),
                    {"unit": "MJ", "multiplier": 3.6},
                ),
                (
                    (
                        "Heat, district or industrial, natural gas {RER}| market group for | Cut-off, S - Copied from Ecoinvent U",
                        "kWh",
                    ),
                    {"unit": "MJ", "multiplier": 3.6},
                ),
                (
                    (
                        "Heat, district or industrial, natural gas {RoW}| market for heat, district or industrial, natural gas | Cut-off, S - Copied from Ecoinvent U",
                        "kWh",
                    ),
                    {"unit": "MJ", "multiplier": 3.6},
                ),
                (
                    (
                        "Land use change, perennial crop {BR}| market group for land use change, perennial crop | Cut-off, S - Copied from Ecoinvent U",
                        "m2",
                    ),
                    {"unit": "ha", "multiplier": 1e-4},
                ),
            ]
            + sum(
                [
                    [
                        [
                            (f"Water, river, {country}", "l"),
                            {"unit": "cubic meter", "multiplier": 0.001},
                        ],
                        [
                            (f"Water, well, {country}", "l"),
                            {"unit": "cubic meter", "multiplier": 0.001},
                        ],
                    ]
                    # only ES for AGB, all for Ginko
                    for country in ["ES", "ID", "CO", "CR", "EC", "IN", "BR", "US"]
                ],
                [],
            ),
        },
    }
]

PASTOECO_MIGRATIONS = [
    {
        "name": "pastoeco-technosphere-fixes",
        "description": "Fixes to ease linking to agb",
        "data": {
            "fields": ("name",),
            "data": [
                (
                    ("Diesel {Europe without Switzerland}| market for | Cut-off, S",),
                    {
                        "name": "Diesel {Europe without Switzerland}| market for | Cut-off, S - Copied from Ecoinvent U"
                    },
                ),
                (
                    ("Petrol, two-stroke blend {GLO}| market for | Cut-off, S",),
                    {
                        "name": "Petrol, two-stroke blend {GLO}| market for | Cut-off, S - Copied from Ecoinvent U"
                    },
                ),
                (
                    (
                        "Tap water {Europe without Switzerland}| market for | Cut-off, S",
                    ),
                    {
                        "name": "Tap water {Europe without Switzerland}| market for | Cut-off, S - Copied from Ecoinvent U"
                    },
                ),
                (
                    ("Electricity, low voltage {FR}| market for | Cut-off, S",),
                    {
                        "name": "Electricity, low voltage {FR}| market for | Cut-off, S - Copied from Ecoinvent U"
                    },
                ),
                (
                    (
                        "Newborn dairy calf, Conventional, Alsace, at farm gate, FR - MEANS#16615 U",
                    ),
                    {
                        "name": "Newborn dairy calf, Conventional, Alsace, at farm gate - MEANS#16615, FR"
                    },
                ),
            ],
        },
    }
]


def remove_azadirachtine(db):
    """Remove all exchanges with azadirachtine, except for apples"""
    new_db = []
    for ds in db:
        new_ds = copy.deepcopy(ds)
        new_ds["exchanges"] = [
            exc
            for exc in ds.get("exchanges", [])
            if (
                "azadirachtin" not in exc.get("name", "").lower()
                or ds.get("name", "").lower().startswith("apple")
            )
        ]
        new_db.append(new_ds)
    return new_db


def remove_negative_land_use_on_tomato(db):
    """Remove transformation flows from urban on greenhouses
    that cause negative land-use on tomatoes"""
    new_db = []
    for ds in db:
        new_ds = copy.deepcopy(ds)
        if ds.get("name", "").lower().startswith("plastic tunnel"):
            new_ds["exchanges"] = [
                exc
                for exc in ds.get("exchanges", [])
                if not exc.get("name", "")
                .lower()
                .startswith("transformation, from urban")
            ]
        else:
            pass
        new_db.append(new_ds)
    return new_db


def remove_some_processes(db):
    """Some processes make the whole import fail
    due to inability to parse the Input and Calculated parameters"""
    new_db = []
    for ds in db:
        new_ds = copy.deepcopy(ds)
        if ds.get("simapro metadata", {}).get("Process identifier") not in (
            "EI3CQUNI000025017103662",
        ):
            new_db.append(new_ds)
    return new_db


GINKO_STRATEGIES = [
    remove_negative_land_use_on_tomato,
    remove_azadirachtine,
    functools.partial(
        link_technosphere_by_activity_hash_ref_product,
        external_db_name="Agribalyse 3.1.1",
        fields=("name", "unit"),
    ),
]
AGB_STRATEGIES = [remove_negative_land_use_on_tomato]

if __name__ == "__main__":
    """Import Agribalyse and additional processes"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--recreate-activities",
        action="store_true",
        help="Delete and re-create the created activities",
    )
    args = parser.parse_args()

    setup_project()

    # # 15m1
    # ### Applying additional transformations...
    # 18603it [00:00, 114568.15it/s]
    # Graph statistics for `Agribalyse 3.1.1 old` importer:
    # 18603 graph nodes:
    # 	process: 18603
    # 5064937 graph edges:
    # 	biosphere: 4908102
    # 	technosphere: 138281
    # 	production: 18554
    # 5064937 edges to the following databases:
    # 	biosphere3: 4908102
    # 	Agribalyse 3.1.1 old: 156835
    # 0 unique unlinked edges (0 total):

    # if (db := "Agribalyse 3.1.1 old") not in bw2data.databases:
    #     import_simapro_csv(
    #         join(DB_FILES_DIR, AGRIBALYSE31),
    #         db,
    #         migrations=AGRIBALYSE_MIGRATIONS,
    #         excluded_strategies=EXCLUDED,
    #         other_strategies=AGB_STRATEGIES,
    #     )
    # else:
    #     print(f"{db} already imported")
    #
    # import sys
    #
    # sys.exit(0)

    # AGRIBALYSE 3.1.1
    # 4m23
    #
    # À la fin :
    # Applying strategy: link_technosphere_by_activity_hash_ref_product
    # Applying strategy: link_technosphere_by_activity_hash_ref_product
    # Graph statistics for `Agribalyse 3.1.1` importer:
    # 19041 graph nodes:
    # 	process: 17067
    # 	readonly_process: 1487
    # 	multifunctional: 487
    # 5076156 graph edges:
    # 	biosphere: 4911196
    # 	technosphere: 124358
    # 	production: 40602
    # 3446623 edges to the following databases:
    # 	biosphere3: 3410867
    # 	Agribalyse 3.1.1: 35756
    # 13276 unique unlinked edges (1629533 total):
    # 	technosphere: 5271
    # 	production: 5406
    # 	biosphere: 2599
    #
    if (db := "Agribalyse 3.1.1") not in bw2data.databases:
        import_simapro_block_csv(
            join(DB_FILES_DIR, AGRIBALYSE31),
            db,
            migrations=AGRIBALYSE_MIGRATIONS,
            excluded_strategies=EXCLUDED,
            other_strategies=AGB_STRATEGIES,
        )
    else:
        print(f"{db} already imported")

    # if (db := "Agribalyse 3.1.1 old") not in bw2data.databases:
    #     import_simapro_csv(
    #         join(DB_FILES_DIR, AGRIBALYSE31),
    #         db,
    #         migrations=AGRIBALYSE_MIGRATIONS,
    #         excluded_strategies=EXCLUDED,
    #         other_strategies=AGB_STRATEGIES,
    #     )
    # else:
    #     print(f"{db} already imported")
    #
    # import sys
    #
    # sys.exit(0)

    # # AGRIBALYSE 3.2
    # if (db := "Agribalyse 3.2 beta 08/08/2024") not in bw2data.databases:
    #     import_simapro_block_csv(
    #         join(DB_FILES_DIR, AGRIBALYSE32),
    #         db,
    #         migrations=AGRIBALYSE_MIGRATIONS,
    #         first_strategies=[remove_some_processes],
    #         excluded_strategies=EXCLUDED,
    #         other_strategies=AGB_STRATEGIES,
    #     )
    # else:
    #     print(f"{db} already imported")

    # PASTO ECO
    if (db := "PastoEco") not in bw2data.databases:
        import_simapro_block_csv(
            join(DB_FILES_DIR, PASTOECO),
            db,
            migrations=PASTOECO_MIGRATIONS,
            excluded_strategies=EXCLUDED,
            other_strategies=[
                functools.partial(
                    link_technosphere_by_activity_hash_ref_product,
                    external_db_name="Agribalyse 3.1.1",
                    fields=("name", "unit"),
                )
            ],
        )
    else:
        print(f"{db} already imported")

    # GINKO
    if (db := "Ginko") not in bw2data.databases:
        import_simapro_block_csv(
            join(DB_FILES_DIR, GINKO),
            db,
            excluded_strategies=EXCLUDED,
            other_strategies=GINKO_STRATEGIES,
            migrations=GINKO_MIGRATIONS + AGRIBALYSE_MIGRATIONS,
        )
    else:
        print(f"{db} already imported")

    # if (db := "Ginko old") not in bw2data.databases:
    #     import_simapro_csv(
    #         join(DB_FILES_DIR, GINKO),
    #         db,
    #         excluded_strategies=EXCLUDED,
    #         other_strategies=GINKO_STRATEGIES,
    #         migrations=GINKO_MIGRATIONS + AGRIBALYSE_MIGRATIONS,
    #     )
    # else:
    #     print(f"{db} already imported")

    # CTCPA
    if (db := "CTCPA") not in bw2data.databases:
        import_simapro_block_csv(
            join(DB_FILES_DIR, CTCPA), db, excluded_strategies=EXCLUDED
        )
    else:
        print(f"{db} already imported")

    # WFLDB
    if (db := "WFLDB") not in bw2data.databases:
        import_simapro_block_csv(
            join(DB_FILES_DIR, WFLDB), db, excluded_strategies=EXCLUDED
        )
    else:
        print(f"{db} already imported")

    if args.recreate_activities:
        if "Ecobalyse" in bw2data.databases:
            del bw2data.databases["Ecobalyse"]
