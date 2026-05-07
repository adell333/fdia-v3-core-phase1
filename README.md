# FDIA v3 Core — Phase 1 Validation

## Overview

This repository documents the Phase 1 validation of FDIA v3 Core, a forensic data reliability framework.

The evaluation is performed on the *misleading_v1* dataset, a controlled synthetic benchmark designed to simulate misleading structured data conditions.

---

## Problem Context

A risk in digital forensic interpretation is assuming that structured data is inherently usable.

In controlled conditions, data may appear structurally valid while lacking integrity or interpretability.

---

## Dataset

**misleading_v1** (controlled synthetic benchmark)

- M1 — Header spoof (valid header, invalid structure)
- M2 — Truncated/artificial structure (partial integrity)
- M3 — Mixed entropy (structured header + high entropy data)

Total samples: **30**

---

## Results

- **30/30 alignment with expected benchmark labels**

| Category | Result |
|----------|--------|
| M1 | 10/10 → Misleading |
| M2 | 10/10 → Partial |
| M3 | 10/10 → Misleading |

---

## Key Improvement (v2 → v3)

FDIA v2 classified truncated structures (M2) as **Usable**, producing false forensic usability claims.

FDIA v3 corrects this by classifying M2 as **Partial**.

---

## Baseline Comparison

Single-signal baselines:

- entropy-only
- structure-only

Limitations:

- do not reliably detect misleading structure
- cannot distinguish invalid structure from encrypted or unknown data

---

## Core Contribution

**FDIA v3 Core demonstrates, on a controlled synthetic benchmark, that validating structure against entropy, integrity, and contradiction signals can reduce false forensic usability claims compared with trusting structure alone.**

---

## Repository Structure

- `fdia/` — FDIA v3 Core engine  
- `datasets/misleading_v1/` — synthetic benchmark dataset  
- `results/` — classification output  
- `reports/` — research report  
- `run_fdia_v3_core.py` — execution script  

---

## Scope

This validation is based on a controlled synthetic benchmark.

It does not represent full real-world validation.

---

## Research Direction

Future work involves applying FDIA v3 Core to real forensic extraction scenarios to evaluate data reliability under real-world conditions.

---

## How to Run

Clone the repository:

```bash
git clone https://github.com/adell333/fdia-v3-core-phase1.git
cd fdia-v3-core-phase1
