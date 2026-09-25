# TensorFleet_LLM

## Literature evidence registry

The `feat/define_system` branch includes a small, dependency-free validator for the R-01 related-work matrix. It makes the issue's acceptance criteria executable without treating unsupported novelty or performance claims as facts.

Each JSONL record must include comparable evidence for:

- Citation, title, year, and source URL
- Hardware, model, quantization, adapter placement, and rank
- Training budget and seeds
- Memory methodology and evaluation metrics
- Released artifacts, findings, and limitations

Validate a completed 12–15 record matrix with:

```bash
PYTHONPATH=src python -m tensorfleet_literature.validate path/to/matrix.jsonl
```

For incremental work, override the bounds temporarily:

```bash
PYTHONPATH=src python -m tensorfleet_literature.validate path/to/matrix.jsonl --minimum 1 --maximum 15
```

Run tests with:

```bash
PYTHONPATH=src python -m pytest -q
```

The validator checks completeness, URL format, year range, record count, and duplicate citations. It does not infer scientific validity; findings and limitations still require human review.
