# Lubricant Equivalents - Data QA Report

Source: `Stem Fuels_Lubricant equivalents.xlsx` (last modified 2024-11-06T12:32:56Z)  
Generated: 2026-07-28

The lookup tool ships the table **as it stands**. Nothing below has been 
silently changed except the spelling fixes in section 1. Sections 2-4 are 
for Stem Fuels to rule on - correcting them would mean inventing or moving 
a product name, which is not something a tool should do on its own.


## 1. Corrections applied (unambiguous spelling only)

Each original spelling remains searchable, so old paperwork still resolves.

| Cell | Was | Now | Why |
|---|---|---|---|
| `F28` | Ranzo HDZ 68 | Rando HDZ 68 | Chevron's product is Rando HDZ; every other row in this block reads 'Rando HDZ'. |
| `K28` | Bartan HV 68 | Bartran HV 68 | BP's product is Bartran HV; every other row in this block reads 'Bartran HV'. |
| `H56` | Lubrax CompsorRF 68 | Lubrax Compsor RF 68 | Missing space; rows 54-55 read 'Lubrax Compsor RF'. |
| `M69` | Renoilt CXI 2 | Renolit CXI 2 | Transposed letters; M66 spells the same product 'Renolit CXI 2'. |
| `F80` | Celtus DE 100 | Cetus DE 100 | Chevron's product is Cetus; rows 75-76 read 'Cetus PAO'. |
| `C92` | Aircrol SW 22 | Aircol SW 22 | Castrol's product is Aircol; rows 59-63 read 'Aircol PD'. |
| `C93` | Aircrol SW 32 | Aircol SW 32 | Castrol's product is Aircol; rows 59-63 read 'Aircol PD'. |
| `C94` | Aircrol SW 46 | Aircol SW 46 | Castrol's product is Aircol; rows 59-63 read 'Aircol PD'. |
| `C95` | Aircrol SW 68 | Aircol SW 68 | Castrol's product is Aircol; rows 59-63 read 'Aircol PD'. |
| `C96` | Aircrol SW 100 | Aircol SW 100 | Castrol's product is Aircol; rows 59-63 read 'Aircol PD'. |
| `C97` | Aircrol SW150 | Aircol SW 150 | Castrol's product is Aircol, plus a missing space before the grade. |
| `C98` | Aircrol SW 220 | Aircol SW 220 | Castrol's product is Aircol; rows 59-63 read 'Aircol PD'. |
| `E116` | Crter Bio 150 | Carter Bio 150 | Dropped letter; rows 114/115/117 read 'Carter Bio'. |
| `A105` | EAL Stem Tube Oils | EAL Stern Tube Oils | The marine term is 'stern tube'. Category label only - affects no product name. |


## 2. Brand column with no column of its own

**41 cells hold Fuchs products.** The logo above that 
column is not Fuchs, and Fuchs has no column of its own.

This is the single largest issue in the table and it affects every 
quote drawn from that column. The tool shows these entries with a 
warning rather than hiding or moving them.

| Cell | Product | Column logo |
|---|---|---|
| `M24` | Renolin 15 HVI | LUKOIL |
| `M25` | Renolin 22 HVI | LUKOIL |
| `M26` | Renolin 32 HVI | LUKOIL |
| `M27` | Renolin 46 HVI | LUKOIL |
| `M28` | Renolin 68 HVI | LUKOIL |
| `M29` | Renolin 100 HVI | LUKOIL |
| `M30` | Renolin 150 HVI | LUKOIL |
| `M31` | Titan Truck Plus 15W40 | LUKOIL |
| `M40` | Renolin Eterna 32 | LUKOIL |
| `M41` | Renolin Eterna 46 | LUKOIL |
| `M43` | Renolin Eterna 68 | LUKOIL |
| `M47` | RENOLIN CLP 68 | LUKOIL |
| `M48` | RENOLIN CLP 100 | LUKOIL |
| `M49` | RENOLIN CLP 150 | LUKOIL |
| `M50` | RENOLIN CLP 220 | LUKOIL |
| `M51` | RENOLIN CLP 320 | LUKOIL |
| `M52` | RENOLIN CLP 460 | LUKOIL |
| `M53` | RENOLIN CLP 680 | LUKOIL |
| `M54` | RENISO KM 32 | LUKOIL |
| `M55` | RENISO KM 46 | LUKOIL |
| `M56` | RENISO KM 32 | LUKOIL |
| `M61` | Renolin 503 | LUKOIL |
| `M62` | Renolin 504 | LUKOIL |
| `M63` | Renolin 505 | LUKOIL |
| `M66` | Renolit CXI 2 | LUKOIL |
| `M69` | Renolit CXI 2 | LUKOIL |
| `M74` | Renolin Unisyn OL 32 | LUKOIL |
| `M75` | Renolin Unisyn OL 46 | LUKOIL |
| `M76` | Renolin Unisyn OL 68 | LUKOIL |
| `M82` | Renolin Unisyn CLP 68 | LUKOIL |
| `M84` | Renolin Unisyn CLP 150 | LUKOIL |
| `M85` | Renolin Unisyn CLP 220 | LUKOIL |
| `M86` | Renolin Unisyn CLP 380 | LUKOIL |
| `M87` | Renolin Unisyn CLP 460 | LUKOIL |
| `M88` | Renolin Unisyn CLP 680 | LUKOIL |
| `M92` | Reniso Triton SEZ 22 | LUKOIL |
| `M93` | Reniso Triton SEZ 32 | LUKOIL |
| `M94` | Reniso Triton SEZ 46 | LUKOIL |
| `M95` | Reniso Triton SEZ 68 | LUKOIL |
| `M96` | Reniso Triton SEZ 100 | LUKOIL |
| `M103` | Renoil LPG 185 | LUKOIL |


## 3. Products sitting in the wrong brand's column

| Cell | Product | Looks like | Sits in |
|---|---|---|---|
| `K23` | Tlx Plus 204 | Castrol | BP |
| `G61` | Aircol PD 150 | Castrol | Sinopec |
| `I61` | Lubrax Compsor AC 150 | Petrobras | ENOC |
| `I62` | Lubrax Compsor AC 150 | Petrobras | ENOC |
| `J65` | Verron EP GREASE 2 | ENOC | Gulf Marine |
| `F101` | Refr Oil Low Temp 68 | Shell | Chevron |
| `K107` | Biotac EP 2 | Castrol | BP |


## 4. The same product listed on more than one row

Usually means a value was pasted down a column and the grade never updated. 
Some of these are legitimate (one product genuinely covering two grades), 
which is why none have been changed.

| Brand | Product | Rows |
|---|---|---|
| Castrol | Biotac Ep 2 | 108 |
| Castrol | Cyltech CL 100 ACC | 10 |
| Castrol | Spheerol SX2 | 66 |
| Chevron | Clarity Synthetic EA grease | 108 |
| ENOC | Lubrax Compsor AC 150 | 62 |
| ENOC | Verron EP GREASE 2 | 69 |
| ExxonMobil | Mobilgrease XHP 222 | 69 |
| ExxonMobil | SHC Aware Grease EP 2 | 108 |
| Gulf Marine | BD EP2 Grease | 108 |
| Gulf Marine | Compressor Oil 100 | 62 |
| Gulf Marine | Compressor Oil 68 | 61 |
| Gulf Marine | Fidelity 150 | 63 |
| Gulf Marine | Fidelity 32 | 59 |
| Gulf Marine | Fidelity 46 | 60 |
| LUKOIL | RENISO KM 32 | 56 |
| LUKOIL | Renolit CXI 2 | 69 |
| Petrobras | Lubrax Lith EP 2 | 69 |
| Sinopec | Cylinder Oil 50100 | 11 |
| Sinopec | Medium Speed Engine 3012 | 21 |


## 5. Noted by hand, not auto-detectable

- `G21` repeats `Medium Speed Engine 3012` from row 20; row 21 is the SAE 40 
  line, so `4012` may have been intended. Not changed - that would invent a name.
- `K43` (`Energol THB 68`) and `M43` (`Renolin Eterna 68`) sit on the 100-grade 
  row while `K42`/`M42` are blank or absent, suggesting both slipped down a row.
- `M56` repeats `RENISO KM 32` from row 54; row 56 is the 68 grade.
- `F96` reads `Capella HFC 100` while rows 93/95 read `Capella HCF`. One 
  spelling is wrong but the correct one is not certain from the table alone.
- Eni (column L) is populated in only a handful of rows. The tool shows those 
  cells as *not listed* rather than *no equivalent* - they read as unresearched.
