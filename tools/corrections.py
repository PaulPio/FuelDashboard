"""Explicit, auditable typo corrections applied to the source data.

Policy agreed with Stem Fuels: fix unambiguous SPELLING slips only. Anything that
would require inventing or relocating a product name is reported in QA-REPORT.md
and left untouched - see qa.py.

Every entry lands in the QA report under "Corrections applied", and every entry
contributes its ORIGINAL spelling as a hidden exact-match alias. This table has
circulated for years, so a customer's own paperwork may literally say "Bartan HV 68";
keeping the old spelling searchable means it still resolves exactly rather than
degrading into a fuzzy guess.

Each correction is keyed by cell so it fails loudly if the workbook changes shape.
"""

CORRECTIONS = [
    {"cell": "F28",  "before": "Ranzo HDZ 68",        "after": "Rando HDZ 68",
     "reason": "Chevron's product is Rando HDZ; every other row in this block reads 'Rando HDZ'."},
    {"cell": "K28",  "before": "Bartan HV 68",        "after": "Bartran HV 68",
     "reason": "BP's product is Bartran HV; every other row in this block reads 'Bartran HV'."},
    {"cell": "H56",  "before": "Lubrax CompsorRF 68", "after": "Lubrax Compsor RF 68",
     "reason": "Missing space; rows 54-55 read 'Lubrax Compsor RF'."},
    {"cell": "M69",  "before": "Renoilt CXI 2",       "after": "Renolit CXI 2",
     "reason": "Transposed letters; M66 spells the same product 'Renolit CXI 2'."},
    {"cell": "F80",  "before": "Celtus DE 100",       "after": "Cetus DE 100",
     "reason": "Chevron's product is Cetus; rows 75-76 read 'Cetus PAO'."},
    {"cell": "C92",  "before": "Aircrol SW 22",       "after": "Aircol SW 22",
     "reason": "Castrol's product is Aircol; rows 59-63 read 'Aircol PD'."},
    {"cell": "C93",  "before": "Aircrol SW 32",       "after": "Aircol SW 32",
     "reason": "Castrol's product is Aircol; rows 59-63 read 'Aircol PD'."},
    {"cell": "C94",  "before": "Aircrol SW 46",       "after": "Aircol SW 46",
     "reason": "Castrol's product is Aircol; rows 59-63 read 'Aircol PD'."},
    {"cell": "C95",  "before": "Aircrol SW 68",       "after": "Aircol SW 68",
     "reason": "Castrol's product is Aircol; rows 59-63 read 'Aircol PD'."},
    {"cell": "C96",  "before": "Aircrol SW 100",      "after": "Aircol SW 100",
     "reason": "Castrol's product is Aircol; rows 59-63 read 'Aircol PD'."},
    {"cell": "C97",  "before": "Aircrol SW150",       "after": "Aircol SW 150",
     "reason": "Castrol's product is Aircol, plus a missing space before the grade."},
    {"cell": "C98",  "before": "Aircrol SW 220",      "after": "Aircol SW 220",
     "reason": "Castrol's product is Aircol; rows 59-63 read 'Aircol PD'."},
    {"cell": "E116", "before": "Crter Bio 150",       "after": "Carter Bio 150",
     "reason": "Dropped letter; rows 114/115/117 read 'Carter Bio'."},
    {"cell": "A105", "before": "EAL Stem Tube Oils",  "after": "EAL Stern Tube Oils",
     "reason": "The marine term is 'stern tube'. Category label only - affects no product name."},
]


def build_index():
    """{cell_ref: correction} for lookup during parsing."""
    return {c["cell"]: c for c in CORRECTIONS}
