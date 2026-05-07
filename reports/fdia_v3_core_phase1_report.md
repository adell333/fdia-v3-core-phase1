# FDIA v3 Core Phase 1 Validation  
## Detecting Misleading Structured Data in Controlled Conditions

---

## Abstract

This report presents the Phase 1 validation of FDIA v3 Core on the *misleading_v1* dataset, a controlled synthetic benchmark designed to simulate misleading structured data conditions.

The dataset consists of 30 samples across three categories: header spoofing, truncated/artificial structure, and mixed entropy artifacts. FDIA v3 Core achieved 30/30 alignment with expected benchmark labels.

A key improvement over FDIA v2 is the correction of false usability classifications in truncated structures.

FDIA v3 Core demonstrates, on a controlled synthetic benchmark, that validating structure against entropy, integrity, and contradiction signals can reduce false forensic usability claims compared with trusting structure alone.

---

## Methodology

The evaluation was conducted using the *misleading_v1* dataset, consisting of:

- M1 — Header spoof samples (valid header, invalid structure)  
- M2 — Truncated/artificial structure samples (partial integrity)  
- M3 — Mixed entropy samples (structured header with high entropy regions)

Each sample was processed through FDIA v3 Core, which evaluates:

- entropy  
- entropy variance  
- structure confidence  
- integrity score  
- contradiction index  

Classification outputs were compared against predefined expected benchmark labels.

---

## Dataset Description

The *misleading_v1* dataset is a controlled synthetic benchmark designed to simulate scenarios where structured data appears valid but is misleading or partially invalid.

Distribution:

- M1: 10 samples  
- M2: 10 samples  
- M3: 10 samples  

Total: 30 samples

---

## FDIA v3 Core Signal Framework

FDIA v3 Core evaluates data reliability through a multi-signal framework:

- Entropy: measures randomness and potential encryption  
- Entropy Variance: identifies irregular distribution patterns  
- Structure Confidence: evaluates structural validity beyond headers  
- Integrity Score: detects inconsistencies and missing segments  
- Contradiction Index: identifies conflicts between signals  

This approach enables validation of structure rather than blind acceptance.

---

## Results

| Category | Expected Label | FDIA v3 Output | Alignment |
|----------|--------------|----------------|-----------|
| M1 | Misleading | Misleading | 10/10 |
| M2 | Partial | Partial | 10/10 |
| M3 | Misleading | Misleading | 10/10 |

Overall result:

- 30/30 alignment with expected benchmark labels

---

## v2 vs v3 Comparison

FDIA v2 limitation:

- classified truncated/artificial structures (M2) as **Usable**

This resulted in false forensic usability claims.

FDIA v3 correction:

- reclassifies M2 as **Partial**
- improves reliability assessment in incomplete structures

---

## Baseline Comparison

Single-signal baselines were evaluated conceptually:

- Entropy-only approaches  
- Structure-only approaches  

Limitations:

- Entropy-only fails to detect misleading structure  
- Structure-only cannot distinguish invalid structure from encrypted or unknown data  

FDIA v3 improves by combining multiple signals and detecting contradictions.

---

## Limitations

- Evaluation is based on a controlled synthetic benchmark  
- Real-world acquisition noise is not represented  
- Hardware extraction variability is not included  
- Dataset size is limited to 30 samples  

---

## Research Implications

The results indicate that relying solely on structural indicators can lead to false forensic conclusions.

Validating structure against entropy, integrity, and contradiction signals provides a more reliable assessment of data usability.

This is potentially relevant to encrypted, partial, or degraded mobile forensic workflows.

---

## Next Work

Future work involves:

- applying FDIA v3 Core to real forensic extraction scenarios  
- evaluating performance under hardware-level acquisition conditions  
- expanding datasets beyond controlled synthetic benchmarks