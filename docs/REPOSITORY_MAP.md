# Repository Map

```text
.
├── .github
│   ├── ISSUE_TEMPLATE
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows
│       ├── ci.yml
│       ├── docs.yml
│       └── release.yml
├── .gitignore
├── .markdownlint.jsonc
├── .zenodo.json
├── CHANGELOG.md
├── CITATION.cff
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── Dockerfile
├── LICENSE
├── README.md
├── analysis
│   └── .gitkeep            (reserved — no scripts yet, see docs/NATURE_READINESS.md)
├── data
│   ├── calibration
│   │   └── .gitkeep        (reserved — no calibration exports yet)
│   ├── checksums
│   │   └── release_sha256.txt
│   ├── circuits
│   │   └── .gitkeep        (reserved — no QASM/circuit files yet)
│   ├── quantum_results_verified.csv
│   ├── raw_bitarrays
│   │   └── .gitkeep        (reserved — no raw BitArray dumps yet)
│   └── results
│       └── .gitkeep        (reserved — no raw job JSON exports yet)
├── docs
│   ├── ARXIV_PREP.md
│   ├── CHECKSUMS.md
│   ├── DATA_AVAILABILITY.md
│   ├── IBM_QUANTUM_EXPERIMENTS_AUDIT.md
│   ├── JOB_IDS.md
│   ├── NATURE_READINESS.md
│   ├── PARSER_FUNCTION_MAP.md
│   ├── REPOSITORY_MAP.md
│   └── RUNTIME_SAFETY.md
├── environment.yml
├── figures
│   ├── fig1_bell_state_comparison.png
│   ├── fig2_reproducibility.png
│   ├── fig3_bb84_d5sd7.png
│   ├── fig4_bb84_control_group.png
│   ├── fig5_qrng_8bit.png
│   ├── fig6_vqc_4qubit.png
│   ├── fig7_entanglement_metrics.png
│   └── fig8_timeline_summary.png
├── latex
│   └── .gitkeep             (reserved — no manuscript draft yet)
├── notebooks
│   └── .gitkeep             (reserved — no notebooks yet)
├── parse_ibm_json.py
├── release
│   ├── v1.1.0
│   │   ├── MANIFEST.md
│   │   └── RELEASE_NOTES.md
│   └── zenodo_deposit.json
├── requirements.txt
├── scripts
│   ├── smoke_test.sh
│   └── verify_checksums.sh
├── stats_report.pdf
└── tests
    └── .gitkeep             (reserved — no test suite yet)

18 directories, 52 files
```

Generated from `find . -path './.git' -prune -o -type f -print | sort` at v1.1.0.
See `release/v1.1.0/MANIFEST.md` for the flat file list and
`docs/DATA_AVAILABILITY.md` for what is and isn't included.
