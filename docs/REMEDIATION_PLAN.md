# Remediation Plan

Status: **DRAFT — for review. No code changes and no remote pushes until approved.**

This document specifies, in execution order, every correction required to make the
repository's scientific claims match its code and data. Each item lists the exact
files/lines affected, the defect, and the prescribed fix. It changes no code by
itself.

---

## 1. Authorship and metadata

### 1.1 Sole authorship — VERIFIED, no change required

Audit result: **Dino Hatibović is already the only author in every project file.**

| File | Evidence |
| --- | --- |
| `CITATION.cff` (lines 3–6) | single `authors` entry, ORCID 0009-0009-5351-6901 |
| `.zenodo.json` (lines 4–9) | single `creators` entry, same ORCID |
| `README.md` (line 23) | citation "Hatibović, D. (2026)" |
| `latex/main.tex` (line 13) | `\author{Dino Hatibovi\'{c}}` |
| `latex/statistical_appendix.tex` (line 9) | `\author{Dino Hatibović}` |
| `latex/ibm-experiments-paper/main.tex` (line 8) | `\author[1]{Dino Hatibović}` |

No co-authors, contributors, or foreign names appear anywhere. Action: none
(re-verify after any future edit to these files).

### 1.2 Version synchronization to v1.1.1

Current state is inconsistent:

| File | Version stated | Fix |
| --- | --- | --- |
| `CITATION.cff` line 8 | 1.1.1 | keep |
| `.zenodo.json` line 29 | 1.1.1 | keep |
| `README.md` line 24 | **1.1.0** | change to 1.1.1 |
| `CHANGELOG.md` | **no `[1.1.1]` section** | add `## [1.1.1] - 2026-07-18` (metadata patch: CITATION/zenodo sync) between `[Unreleased]` and `[1.1.0]` |
| `release/zenodo_deposit.json` | **1.1.0** | regenerate for 1.1.1 or clearly mark as the v1.1.0 deposit snapshot |
| `release/v1.1.1/RELEASE_NOTES.md` line 7 | calls 21427293 "the v1.1.0 Zenodo DOI" | reword (see 1.3) |

### 1.3 DOI decision (required before editing version strings)

DOI `10.5281/zenodo.21427293` is currently claimed by **both** v1.1.0
(`README.md`, `release/v1.1.1/RELEASE_NOTES.md`) and v1.1.1 (`CITATION.cff`,
`.zenodo.json`). A Zenodo version DOI identifies exactly one deposited version.
Choose one:

- **Option A (recommended, no new deposit):** v1.1.1 is a GitHub-only metadata
  patch. Then 21427293 remains the **v1.1.0** DOI; `CITATION.cff` and
  `.zenodo.json` keep `version: 1.1.1` but the README citation should cite the
  concept DOI `10.5281/zenodo.21427292` (all versions) or explicitly say
  "v1.1.1, archived as Zenodo v1.1.0 deposit 21427293".
- **Option B:** publish a new Zenodo version for v1.1.1 → new DOI; update
  `CITATION.cff`, `.zenodo.json`, README badge + citation to the new DOI.

Additionally (independent of A/B): the manuscripts still cite the **v1.0.0** DOI
`10.5281/zenodo.20749395` — update `latex/main.tex` line 211 (Data Availability),
`latex/statistical_appendix.tex` line 16, `latex/ibm-experiments-paper/bibliography.bib`,
and `notebooks/README.md` line 4 to the chosen current DOI.

Also fix the two broken CI badges in `README.md` lines 3–4: the image URL is the
repo URL, not a badge URL — should be
`https://github.com/dinohatibovic/IBM-Quantum-Experiments/actions/workflows/ci.yml/badge.svg`
(and `docs.yml/badge.svg`).

---

## 2. Mathematical and code corrections in `parse_ibm_json.py`

### 2.1 Remove the P(11) fidelity override (lines 361–363) — CRITICAL

```python
# DELETE these lines:
# If fidelity < 50%, it's probably a |11⟩-optimised circuit
if c.get("11", 0) / n > 0.80:
    f = c.get("11", 0) / n  # target is just |11⟩
```

Defect: when a job's counts are dominated by |11⟩, "fidelity" is silently
redefined as P(11). This manufactures the headline 96.3 % (job `d5sd9mveglic…`,
Shannon entropy 0.278 ⇒ ~96 % of shots in the single state |11⟩ — consistent
with a **separable** product state, i.e. concurrence ≈ 0, not 0.926). The
comment is also wrong (it says "fidelity < 50%" while the condition tests
P(11) > 0.80).

Consequences to propagate after removal:

- `data/quantum_results_verified.csv` row `d5sd9mv…` must be regenerated from
  raw data or **excluded/flagged as anomalous**; its C=0.926 / T=0.857 values
  are invalid.
- Headline numbers change everywhere: README line 16, `latex/main.tex`
  (abstract line 29, results), `latex/ibm-experiments-paper/sections/results.tex`
  lines 5–8, notebooks 01/04 markdown. The honest best Bell result in the
  dataset is **94.4 %** (`d5sd2io…`, 4000 shots).
- The "R2 exceeds R1 by +8.3 pp under the same circuit" claim should be restated
  from the like-for-like 4000-shot jobs: 0.940/0.944 (ibm_fez) vs 0.859
  (ibm_torino) ⇒ **8.1–8.5 pp**.

### 2.2 Correct Bell-fidelity estimator

Current: `bell_fidelity` (lines ~183–192) computes P(00)+P(11) from Z-basis
counts only. That is the ZZ-correlation, an **upper bound**, not
F = ⟨Φ⁺|ρ|Φ⁺⟩ — a distribution concentrated on |11⟩ alone also scores high.

Prescribed estimator (three measurement settings):

F = (1 + ⟨XX⟩ − ⟨YY⟩ + ⟨ZZ⟩) / 4,  where ⟨AB⟩ = P(outcomes equal) − P(outcomes differ)

Implementation plan:

1. New QPU runs per Bell job: three circuits — (i) bare Bell (ZZ), (ii) Bell +
   H on both qubits (XX), (iii) Bell + S†·H on both qubits (YY). Same backend,
   same qubit pair, ≥4000 shots each.
2. New parser function `bell_fidelity_xyz(counts_zz, counts_xx, counts_yy)`
   implementing the formula above; keep the existing Z-only quantity but rename
   it `zz_correlation` and label it as an upper bound in the CSV and docs.
3. Alternative (heavier): full 2-qubit state tomography
   (`qiskit_experiments.library.StateTomography`), reconstruct ρ, then
   F = ⟨Φ⁺|ρ|Φ⁺⟩ directly. Choose tomography only if Wootters concurrence
   (2.3) is wanted from the same data.
4. Uncertainty: propagate multinomial errors on the three correlators
   (bootstrap over shots, B ≥ 1000) instead of a single Wilson CI; Wilson CI
   remains valid only for the Z-only proportion.

### 2.3 Concurrence and tangle (lines 195–205)

`concurrence()` returns `max(0, 2F−1)`. As a **lower bound** on concurrence this
is legitimate *only* when F is a true fidelity to a maximally entangled state —
not when F is the Z-only proxy, and not under the (removed) P(11) override.
Fix, in order of preference:

- With tomography (2.2 option 3): compute Wootters concurrence
  C = max(0, λ₁−λ₂−λ₃−λ₄) from ρ(σy⊗σy)ρ*(σy⊗σy) — this is what
  `latex/statistical_appendix.tex` line 79 already (falsely) claims is done.
- Without tomography: keep `max(0, 2F−1)` but (a) feed it the XYZ fidelity from
  2.2, (b) rename the CSV column to `concurrence_lower_bound`, and (c) rewrite
  the appendix to describe the bound, not Wootters' formula.

### 2.4 χ² reproducibility test (lines 241–250)

`stats.chisquare(obs1, f_exp=obs2)` treats a noisy run as exact expected values
(statistically invalid) and **raises** whenever the two runs have unequal total
shots. Fix: use a 2×k contingency test —

```python
from scipy.stats import chi2_contingency
chi2, p, dof, _ = chi2_contingency([obs1, obs2])
```

which pools the runs for the expected counts and handles unequal totals. Update
`latex/statistical_appendix.tex` (line 49) to describe exactly this.

### 2.5 QBER (lines 208–215) and BB84 processing

`qber()` hardcodes `alice_sends="0"` and defines QBER = P(bob=1) with no basis
sifting — that is not the BB84 QBER. Fix: record Alice's bit and basis registers
in the experiment, sift (keep only matching-basis rounds), then
QBER = mismatches / sifted bits. See §3.2 for the required control run.

### 2.6 Minor numeric hygiene

- `wilson_ci(int(f * n), n)` (line 366): floor-truncation bias — pass the exact
  integer success count (`signal` from the counts) instead of `int(f*n)`.
- `decode_bitarray` (line 72): replace the unconditional `"==="` padding with
  `s + "=" * (-len(s) % 4)`.
- `extract_info` (lines 279–285): shots are read positionally from `pub[2]`;
  add a defensive check / fallback for SamplerV2 pub-shape changes.

### 2.7 Reproducibility gate

The parser cannot run as shipped: `data/results/` is empty, so every entry in
`KNOWN_JOBS` (lines 523–532) hits `FileNotFoundError`, and the CSV is not
regenerable. Either commit the raw `job-*-result.json` exports (preferred; they
are also required to recompute row `d5sd9mv…` after 2.1) or soften every
"fully reproducible" claim (`latex/main.tex`, abstract/conclusion of
`ibm-experiments-paper`, README line 7) to "processed results included; raw
exports available on request".

---

## 3. Other scientific and logic corrections

### 3.1 Notebook `notebooks/03_VQC.ipynb` — entropy vs circuit width

Audit result: the entropy cell (cell 7) **already uses `np.log2`** — the log
base is correct and no ln→log2 change is needed. The actual defect is
dimensional: the ansatz (cell 3) is a **2-qubit** circuit (max entropy 2 bits),
while the notebook header and manuscripts claim **3.885 / 4 bits** — physically
impossible for that circuit. The dataset job `d5se1sk…` (entropy 3.885 ⇒ ≥16
outcomes) and `figures/fig6_vqc_4qubit.png` both indicate the real experiment
was 4-qubit. Fix:

1. Rewrite `vqc_ansatz` as a 4-qubit circuit (e.g. `ry` layer on q0–q3 +
   entangling `cz` chain + `measure_all`), matching the recorded job.
2. Keep `np.log2`; report entropy as x / 4.000 bits, and guard the sum against
   p = 0 terms.
3. Update the Sampler API usage: `result.quasi_dists` is the V1 API; the
   dataset was produced with SamplerV2 (`result[0].data.meas.get_counts()`).
4. The claimed χ² = 300.94 (p ≈ 0) is currently not reproducible from anything
   in the repo — either recompute it in the notebook from the raw counts (needs
   2.7) or remove it from `results.tex` / `main.tex`.

### 3.2 BB84 — clean baseline QBER (no Eve)

Current data has **no eavesdropper-free run**: both BB84 jobs (`d5sd7vb…`,
`d5sd8vg…`) contain an `eve` register and show QBER ≈ 49 %. The 0.60 % baseline
and the derived "82×" degradation (README line 17, `results.tex` lines 19–21,
`main.tex` lines 33/148–151, `fig4_bb84_control_group.png`) exist nowhere in the
dataset. Required control-run conditions:

1. Circuit: Alice prepares BB84 states, **no intercept-resend stage** (no `eve`
   register in the circuit), Bob measures — same backend (`ibm_fez`), same
   physical qubits, same transpilation level and shot count (12000) as the Eve
   runs, executed in the same calibration window.
2. Basis sifting: keep only rounds where Alice's and Bob's bases match;
   QBER_baseline = mismatched sifted bits / sifted bits (expected ~0.5–2 % from
   hardware error alone).
3. Report degradation as QBER_eve / QBER_baseline with a two-proportion test
   (as `statistical_appendix.tex` line 87 already promises) and CIs on both.
4. Until this run exists: remove "82×" and "0.60 %" from README and all
   manuscripts, and drop or clearly mark `fig4` as illustrative.

### 3.3 `analysis/noise_model_extended.py` — 2- vs 5-parameter AIC/BIC comparison

Audit results and fixes:

1. **Non-identifiability:** `readout_fidelity_asym` (lines 26–33) collapses
   r0, r1 into `(r0+r1)/2` — only their sum affects the model, so the
   "5-parameter" model has 4 effective parameters and the `n_params=5` in
   `compare_models` (line 167) is wrong. Fix: either implement genuinely
   asymmetric readout response (state-dependent: apply r0 to qubits ideally
   reading 0 and r1 to qubits ideally reading 1, per target outcome) or reduce
   to a single readout parameter `r` and count parameters honestly.
2. **Missing simple model:** the promised 2-parameter model
   (p_gate, r_readout) is never implemented; `compare_models` takes
   `simple_sse` from outside, and notebook 06 feeds it a **placeholder**
   (`simple_sse = sse_ext * 1.5`). Fix: implement
   `fit_simple_model(bell_df)` — F̂ = (1−p_gate)^(n_1q+n_2q) · (1−r)^n_qubits,
   same L-BFGS-B least-squares — and pass its real SSE.
3. **Missing data columns:** the model requires `n_1q, n_2q, n_pairs, n_qubits,
   t1, t2, duration_s`, none of which exist in
   `data/quantum_results_verified.csv`. Fix: add a circuit-metadata table
   (e.g. `data/circuits/circuit_metadata.csv`, one row per job: gate counts
   from the transpiled circuit, qubit pair, duration; T1/T2 from
   `backend.properties()` — the CSV's calibration columns are all "MISSING")
   and join it in the notebook instead of hand-written synthetic rows.
4. **Underdetermination:** only 3 valid Bell rows exist (after excluding the
   anomalous `d5sd9mv…`, §2.1). Fitting 4–5 parameters to 3 points is
   underdetermined and AIC/BIC at n_points=3 is not meaningful. Fix: state
   n ≥ 8–10 Bell circuits of varying depth as a prerequisite for the 5-param
   fit; with the current 3 points fit at most the 2-parameter model, and
   present the extended model as illustrative only.
5. **Numerical guards:** `aic_bic_from_sse` (lines 150–158) returns −inf when
   SSE = 0 — clamp `sigma2 = max(sse/n, eps)`; bootstrap `n_boot` in notebook
   06 (200) should be ≥1000 to match the appendix's B claim, or the appendix
   text (B=10,000) must be corrected to what is actually run.

### 3.4 Documentation refresh (stale statements found during audit)

- `README.md` lines 45–49, 73: `analysis/`, `notebooks/`, `tests/` described as
  "currently empty" — all are populated; rewrite the structure section.
- `docs/REPOSITORY_MAP.md`, `docs/NATURE_READINESS.md`, `docs/ARXIV_PREP.md`,
  `docs/ROADMAP.md`: regenerate/update — they still describe the pre-notebook,
  pre-manuscript state.
- `docs/PARSER_FUNCTION_MAP.md` line 21: stale default output path
  (`quantum_results.csv` vs actual `data/quantum_results_verified.csv`).
- `latex/ibm-experiments-paper/sections/abstract.tex` line 2: date range
  "January 27 – March 15, 2026" is unsupported — every CSV row is dated
  2026-01-27; correct to the actual date.
- Add CI coverage: run `pytest`, execute the parser against committed raw data
  (once 2.7 lands), and assert the recomputed CSV matches — the current smoke
  test only checks compile + CSV shape.

---

## 4. Execution order and guardrails

1. §1.3 DOI decision (blocks §1.2 edits) → §1.2 version sync → badge fix.
2. §2.1 override removal + §2.6 hygiene (pure code, no data needed).
3. §2.7 raw-data commit → regenerate CSV → propagate corrected numbers to
   README + manuscripts (this supersedes the 96.3 % headline).
4. §2.2/§2.3 new QPU runs (XYZ bases) and §3.2 BB84 control run — the only
   items requiring hardware time.
5. §2.4, §3.1, §3.3 code/notebook fixes; §3.4 docs refresh.
6. Only after all numbers are re-verified: release v1.1.2/v1.2.0, new Zenodo
   deposit, arXiv submission.

**Guardrails:** no `git push` and no remote/GitHub changes until this plan is
approved; no code edits are performed by this document; every numeric claim in
README/manuscripts must trace to a value computable from committed data by
committed code.
