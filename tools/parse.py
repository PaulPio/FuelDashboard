"""Parse the Stem Fuels lubricant equivalents workbook into structured data.

Every rule in here is driven by a real string in the source file - see docstrings.
The workbook is never modified; this module only reads.
"""

import re

# Columns B..M hold the twelve brands. The brand names appear NOWHERE as text in the
# sheet - they are logo images anchored above each column. These names were read off
# the logos themselves (xl/media/image*.png, mapped via the drawing anchors).
BRANDS = [
    {"id": "shell",      "name": "Shell",      "col": "B", "col_idx": 2,  "image": 11},
    {"id": "castrol",    "name": "Castrol",    "col": "C", "col_idx": 3,  "image": 12},
    {"id": "exxonmobil", "name": "ExxonMobil", "col": "D", "col_idx": 4,  "image": 2},
    {"id": "total",      "name": "Total",      "col": "E", "col_idx": 5,  "image": 3},
    {"id": "chevron",    "name": "Chevron",    "col": "F", "col_idx": 6,  "image": 4},
    {"id": "sinopec",    "name": "Sinopec",    "col": "G", "col_idx": 7,  "image": 5},
    {"id": "petrobras",  "name": "Petrobras",  "col": "H", "col_idx": 8,  "image": 6},
    {"id": "enoc",       "name": "ENOC",       "col": "I", "col_idx": 9,  "image": 7},
    {"id": "gulf",       "name": "Gulf Marine","col": "J", "col_idx": 10, "image": 8},
    {"id": "bp",         "name": "BP",         "col": "K", "col_idx": 11, "image": 10},
    {"id": "eni",        "name": "Eni",        "col": "L", "col_idx": 12, "image": 13},
    {"id": "lukoil",     "name": "LUKOIL",     "col": "M", "col_idx": 13, "image": 9},
]

FIRST_ROW, LAST_ROW = 8, 117

# Cell states. These four are genuinely different facts and must not be conflated.
PRODUCTS = "products"   # one or more real products
NONE     = "none"       # "-"   -> checked, no equivalent exists
UNKNOWN  = "unknown"    # empty -> not researched


def normalize(s):
    """Search key: lowercase, punctuation stripped, whitespace collapsed.

    'Hydraulic HVI Plus  22' and 'hydraulic hvi plus 22' must collide.
    """
    s = s.lower()
    s = re.sub(r"[^\w\s]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def split_products(text):
    """Split a cell on '/' only when BOTH sides contain letters.

    'Visga 15/Equivis ZS 15'  -> two products.
    'Navigo TPEO 30/40'       -> ONE product; the 40 is a grade suffix, not a name.
    Without this rule the index fills with junk entries like '40' and '4524'.
    """
    if "/" not in text:
        return [text.strip()]
    parts = [p.strip() for p in text.split("/")]
    if all(re.search(r"[A-Za-z]", p) for p in parts if p):
        return [p for p in parts if p]
    return [text.strip()]


def extract_annotation(name):
    """Pull a TRAILING parenthetical off a product name and classify it.

    Only trailing parens are annotations:
      'Alexia S4 (SAE 40 TBN 60)'   -> annotation
      '4524 (32) Synthetic Ref. Oil' -> NOT an annotation, parens are mid-name

    Tolerates unclosed parens - 'Taro special HT 55 (SAE TBN 55' really is in the file.

    Returns (clean_name, specs, obsolete, approximate).
    """
    name = re.sub(r"\s+", " ", name).strip()
    m = re.search(r"\(([^()]*)\)?\s*$", name)
    if not m or m.start() == 0:
        return name, [], False, False

    inner = m.group(1).strip()
    clean = name[: m.start()].strip()
    if not clean:
        return name, [], False, False

    obsolete = "obsolete" in inner.lower()
    approximate = "closest" in inner.lower()

    specs = []
    for spec_m in re.finditer(r"\b(SAE|TBN)\b\s*([\w.\-]+)?", inner, re.I):
        label = spec_m.group(1).upper()
        value = (spec_m.group(2) or "").strip()
        specs.append(f"{label} {value}".strip())
    # 'Taro special HT 55 (SAE TBN 55' -> SAE has no value, TBN does. Drop the empty one
    # only when a richer sibling exists, so we never silently lose information.
    if len(specs) > 1:
        specs = [s for s in specs if re.search(r"\d", s)] or specs

    if not obsolete and not approximate and not specs:
        # An unrecognised trailing parenthetical is part of the name, not an annotation.
        return name, [], False, False

    return clean, specs, obsolete, approximate


def parse_cell(raw):
    """Turn one worksheet cell into a state + product list."""
    if raw is None:
        return {"state": UNKNOWN}
    text = re.sub(r"\s+", " ", str(raw)).strip()
    if not text:
        return {"state": UNKNOWN}
    if text == "-":
        return {"state": NONE}

    products = []
    for piece in split_products(text):
        clean, specs, obsolete, approximate = extract_annotation(piece)
        if not clean:
            continue
        products.append({
            "name": clean,
            "specs": specs,
            "obsolete": obsolete,
            "approximate": approximate,
        })
    if not products:
        return {"state": UNKNOWN}
    return {"state": PRODUCTS, "products": products}


def _has_bottom_border(cell):
    b = cell.border
    return bool(b and b.bottom and b.bottom.style)


def category_blocks(ws, label_fixes=None):
    """Recover category blocks from cell BORDERS, not from label position.

    The category label in column A is written once on the visual middle row of its
    block, so label position cannot delimit anything. The drawn box around each block
    can: a bottom border in column A or B closes a block.

    Returns [{'name', 'start', 'end'}] for blocks that contain data. Blank
    page-break spacers (rows 44-46 and 89-91) fall out naturally - they close as
    blocks but hold no products, so they are dropped.
    """
    label_fixes = label_fixes or {}
    blocks = []
    start = FIRST_ROW
    for row in range(FIRST_ROW, LAST_ROW + 1):
        closes = _has_bottom_border(ws.cell(row=row, column=1)) or \
                 _has_bottom_border(ws.cell(row=row, column=2))
        if closes or row == LAST_ROW:
            blocks.append((start, row))
            start = row + 1

    out = []
    for start, end in blocks:
        has_data = any(
            parse_cell(ws.cell(row=r, column=b["col_idx"]).value)["state"] == PRODUCTS
            for r in range(start, end + 1)
            for b in BRANDS
        )
        if not has_data:
            continue
        parts = []
        for r in range(start, end + 1):
            raw = ws.cell(row=r, column=1).value
            if not raw:
                continue
            # Column A carries category labels, so corrections apply here too.
            parts.append(label_fixes.get(f"A{r}", str(raw).strip()))
        label = re.sub(r"\s+", " ", " ".join(parts)).strip()
        out.append({"name": label or "Uncategorised", "start": start, "end": end})
    return out
