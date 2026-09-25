from dataclasses import replace

from tensorfleet_literature.models import EvidenceRecord, LiteratureMatrix


def record(citation="Author 2025"):
    return EvidenceRecord(
        citation=citation,
        title="A reproducible study",
        year=2025,
        url="https://example.org/paper",
        hardware="Apple M4, 16 GB",
        model="Example 1B",
        quantization="4-bit",
        adapter_placement="last 8 attention layers",
        adapter_rank="8",
        training_budget="200k supervised tokens",
        seeds="3",
        memory_methodology="peak allocator and process RSS, reported separately",
        evaluation_metrics="macro-F1; exact match",
        released_artifacts="code and configs",
        findings="coverage and rank trade off under matched budgets",
        limitations="single device and two tasks",
    )


def test_complete_record_is_valid():
    assert record().validate() == []


def test_invalid_record_reports_missing_and_bad_url():
    item = replace(record(), title="", url="not-a-url")
    errors = item.validate()
    assert "title is required" in errors
    assert "url must be an absolute http(s) URL" in errors


def test_matrix_requires_twelve_to_fifteen_unique_records():
    matrix = LiteratureMatrix.from_records(record(f"Author {year}") for year in range(2014, 2026))
    assert matrix.validate() == []

    duplicate = LiteratureMatrix.from_records([record("Same 2025")] * 12)
    errors = duplicate.validate()
    assert any("duplicate citation" in error for error in errors)


def test_matrix_can_use_custom_bounds_for_incremental_work():
    matrix = LiteratureMatrix.from_records([record()])
    assert matrix.validate(minimum=1, maximum=1) == []
