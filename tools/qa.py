"""Detect suspected data problems. Reports only - never edits, never auto-fixes.

Two detectors:

1. Column bleed - a product name whose family belongs to a different brand's column.
   Catches copy/paste slips like Castrol's 'Tlx Plus 204' sitting in BP's column.

2. Vertical repeats - the same product name on consecutive rows of one column, which
   usually means a grade was pasted down and never edited.

Both feed the QA report AND a per-cell warning in the app, so a salesperson sees the
doubt at the moment they would otherwise quote it.
"""

import re
from collections import defaultdict

# Well-known product families per brand. Used only for flagging; never rewrites data.
# Keys are brand ids from parse.BRANDS.
BRAND_FAMILIES = {
    "shell":      ["melina", "alexia", "argina", "gadinia", "tellus", "sirius", "rimula",
                   "turbo t", "omala", "clavus", "corena", "gadus", "donax", "naturelle",
                   "refr oil"],
    "castrol":    ["cdx", "cyltech", "tlx", "mhp", "hyspin", "tection", "perfecto",
                   "alpha sp", "alphasyn", "icematic", "aircol", "spheerol", "biostat",
                   "biopar", "biotac", "biotrans", "agri trans", "tqd"],
    "exxonmobil": ["mobil", "gargoyle", "rarus", "zerice", "eal artic", "shc aware",
                   "delvac", "atf 220", "multipurpose atf"],
    "total":      ["atlanta", "talusia", "aurelia", "disola", "visga", "equivis", "azolla",
                   "turbine t", "preslia", "epona", "carter", "lunaria", "dacnis", "ceran",
                   "multis", "elfmatic", "planetelf", "biohydran", "bioneptan", "barelf",
                   "seriola", "rubia", "biomultis", "bio adhesive"],
    "chevron":    ["veritas", "taro", "rando", "ursa", "regal", "meropa", "capella",
                   "multifak", "texamatic", "texatherm", "texclad", "clarity", "cetus",
                   "molytex", "delo", "pinnacle", "compressor p"],
    "sinopec":    ["system oil", "cylinder oil", "medium speed", "l-hv", "l-cdk", "tsa ",
                   "dba ", "mco ", "ch-4", "mos2", "ep lithium", "4502", "4523", "4524"],
    "petrobras":  ["marbrax", "lubrax"],
    "enoc":       ["strata", "axis", "reduct", "spiro", "cryogen", "vortex", "lamina",
                   "verron"],
    "gulf":       ["superbear", "cylcare", "power", "hydraulic hvi", "harmony", "turbine oil",
                   "gear oil", "fidelity", "compressor oil", "hyperbar", "cooloil",
                   "synth comp", "synth gear", "de compressor", "bd ", "ht oil", "atf dx"],
    "bp":         ["energol", "bartran", "vanellus", "energrease", "enersyn"],
    "eni":        ["eni "],
    "lukoil":     ["navigo", "navisyn"],
}

# Families that appear in the table but belong to a brand with NO column of its own.
# Flagged so they are never silently attributed to whichever logo sits above them.
ORPHAN_FAMILIES = {
    "Fuchs": ["renolin", "reniso", "renolit", "renoil", "titan"],
}

_FAMILY_LOOKUP = []
for _bid, _prefixes in BRAND_FAMILIES.items():
    for _p in _prefixes:
        _FAMILY_LOOKUP.append((_p, _bid))
for _owner, _prefixes in ORPHAN_FAMILIES.items():
    for _p in _prefixes:
        _FAMILY_LOOKUP.append((_p, f"~{_owner}"))
# Longest prefix wins, so 'gear oil' beats 'gear' and 'turbine oil' beats 'turbine'.
_FAMILY_LOOKUP.sort(key=lambda kv: -len(kv[0]))


def owner_of(product_name):
    """Which brand does this product name's family belong to? None if unrecognised."""
    key = re.sub(r"\s+", " ", product_name.lower()).strip()
    for prefix, owner in _FAMILY_LOOKUP:
        if key.startswith(prefix):
            return owner
    return None


def find_bleeds(rows, brands):
    """Cells whose product family belongs to another brand's column."""
    findings = []
    brand_names = {b["id"]: b["name"] for b in brands}
    for row in rows:
        for brand in brands:
            cell = row["cells"].get(brand["id"], {})
            if cell.get("state") != "products":
                continue
            for product in cell["products"]:
                owner = owner_of(product["name"])
                if owner is None or owner == brand["id"]:
                    continue
                if owner.startswith("~"):
                    owner_label = owner[1:]
                    kind = "orphan-brand"
                    detail = (f"'{product['name']}' is a {owner_label} product, but this "
                              f"column's logo is {brand_names[brand['id']]}. "
                              f"{owner_label} has no column of its own in this table.")
                else:
                    owner_label = brand_names.get(owner, owner)
                    kind = "column-bleed"
                    detail = (f"'{product['name']}' is a {owner_label} product but sits in "
                              f"the {brand_names[brand['id']]} column.")
                findings.append({
                    "kind": kind,
                    "cell": f"{brand['col']}{row['id']}",
                    "row": row["id"],
                    "brand": brand["id"],
                    "product": product["name"],
                    "expected_owner": owner_label,
                    "detail": detail,
                })
    return findings


def find_repeats(rows, brands):
    """Same product name on consecutive rows of one column - usually a paste-down."""
    findings = []
    brand_names = {b["id"]: b["name"] for b in brands}
    by_brand = defaultdict(list)
    for row in rows:
        for brand in brands:
            cell = row["cells"].get(brand["id"], {})
            if cell.get("state") != "products":
                continue
            for product in cell["products"]:
                by_brand[brand["id"]].append((row["id"], product["name"]))

    for brand_id, entries in by_brand.items():
        seen = {}
        for row_id, name in entries:
            key = re.sub(r"\s+", " ", name.lower()).strip()
            if key in seen:
                prev = seen[key]
                findings.append({
                    "kind": "repeated-value",
                    "cell": f"{brand_id}:{row_id}",
                    "row": row_id,
                    "brand": brand_id,
                    "product": name,
                    "detail": (f"{brand_names[brand_id]} lists '{name}' on both row {prev} "
                               f"and row {row_id}. Different grades usually mean different "
                               f"products - check whether one was pasted down."),
                })
            seen[key] = row_id
    return findings


def run(rows, brands):
    """All findings, grouped, plus a {cell_key: [warning strings]} map for the app."""
    bleeds = find_bleeds(rows, brands)
    repeats = find_repeats(rows, brands)

    warnings = defaultdict(list)
    for f in bleeds:
        warnings[f"{f['brand']}:{f['row']}"].append(
            f"Listed as a {f['expected_owner']} product"
        )
    for f in repeats:
        warnings[f"{f['brand']}:{f['row']}"].append("Also listed on another row")

    return {"bleeds": bleeds, "repeats": repeats, "warnings": dict(warnings)}
