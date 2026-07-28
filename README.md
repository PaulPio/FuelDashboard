# Lubricant Equivalents Lookup — Stem Fuels

A search tool for the lubricant equivalents table. Type any product name from any
brand and every equivalent appears together, ready to paste into a quote.

**The tool is one file: `dist/index.html`.** Everything is inside it — the data, the
brand logos, the search. Double-click it and it works. No internet, no install, no
setup. Email it, put it on a shared drive, or copy it onto a laptop going to sea.

---

## Using it

Type into the search box. It searches **every brand at once**, so it does not matter
whose product the customer names.

- **Exact name** — jumps straight to the row: `Mobilgard 300`
- **Not quite right** — offers a list to pick from. It will never choose for you.
  `Mobilgard 30` will not silently become `Mobilgard 300`, because a wrong grade is a
  wrong quote.
- **Category** — type `gear oil` to see the whole section
- **Old spelling** — the typos that were in the spreadsheet still find their product,
  so a customer's own paperwork still works

Grade numbers are picked out in amber. That is deliberate: `Alexia 40` and
`Alexia 100` differ by nothing else, and the highlight lets you check at a glance that
every brand on the row agrees on the grade.

**Copy all equivalents** puts the row on the clipboard as two columns, so it pastes
into Excel or an email cleanly. **Copy as one line** writes it as a sentence for a
quote.

### What the greyed-out entries mean

These are different facts, and the tool keeps them apart:

| Shown | Means |
|---|---|
| *No equivalent* | The cell holds `-`. Someone checked; that brand has nothing matching. |
| *Not listed* | The cell is blank. Nobody has filled it in yet. |

### Warnings

An amber tag means the entry is doubtful — most often **Listed as a Fuchs product**.
See `data/QA-REPORT.md` for why, and read that report before relying on the last
column.

---

## Updating it when the spreadsheet changes

Edit `Stem Fuels_Lubricant equivalents.xlsx` as normal, then:

```
pip install openpyxl        # once
python tools/build.py
```

That rewrites `dist/index.html`, `data/equivalents.json` and `data/QA-REPORT.md`.
Send out the new `dist/index.html` and re-deploy if you host it.

The build **stops with an error** rather than producing something subtly wrong if the
spreadsheet has moved underneath it — for example if a row a correction points at now
holds different text. The message names the cell.

### Publishing it

`dist/index.html` is a plain static page, so any host works:

```
npm i -g vercel
cd dist && vercel deploy --prod
```

The hosted page and the emailed file are the same artifact, so they cannot drift.

---

## What's in here

| Path | |
|---|---|
| `Stem Fuels_Lubricant equivalents.xlsx` | The source of truth. Never written to. |
| `dist/index.html` | **The tool.** The only file anyone else needs. |
| `data/QA-REPORT.md` | Suspected errors in the table, for Stem Fuels to rule on. |
| `data/equivalents.json` | The extracted data, readable, for checking a change. |
| `tools/build.py` | Rebuilds everything from the spreadsheet. |
| `tools/parse.py` | Reads the spreadsheet's quirks — see below. |
| `tools/corrections.py` | The spelling fixes, one line each, with reasons. |
| `tools/qa.py` | Finds suspect entries. Reports only; never edits. |
| `app/index.template.html` | The page itself, before the data is baked in. |

### Why parsing this spreadsheet is not trivial

The rules in `tools/parse.py` each come from a real string in the file:

- **Category names come from the cell borders**, not the labels. The label sits on the
  visual middle row of its block, so it cannot mark where a block starts or ends.
- **`Visga 15/Equivis ZS 15` is two products; `Navigo TPEO 30/40` is one.** A slash
  splits only when both sides contain letters, otherwise `30/40` would enter the index
  as a product called "40".
- **Only a trailing bracket is a note.** `Alexia S4 (SAE 40 TBN 60)` carries a spec;
  `4524 (32) Synthetic Ref. Oil` is just the product's name.
- **Unclosed brackets are tolerated** — `Taro special HT 55 (SAE TBN 55` is in the file.
- **One product can sit on several rows**, and the tool shows all of them rather than
  guessing which was meant.

---

Equivalents are guidance for quoting. Confirm against the maker's specification
before supply.
