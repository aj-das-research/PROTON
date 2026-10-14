#!/usr/bin/env python3
"""Audit provenance and reading-depth bookkeeping; does not certify paper quality."""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import date, datetime
import json
from pathlib import Path
import re
import sys


CUTOFF = date(2026, 9, 17)
LEVELS = {'metadata_only', 'abstract_narrative_review', 'targeted_narrative_structure_review'}
ARXIV_ID = re.compile(r'2[3-6](0[1-9]|1[0-2])\.[0-9]{4,5}')


def text_field(record: dict, field: str, where: str, required: bool = False) -> None:
    if field not in record and not required:
        return
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{where}.{field}: expected a nonempty string')


def bool_field(record: dict, field: str, where: str, required: bool = False) -> None:
    if field in record or required:
        if type(record.get(field)) is not bool:
            raise ValueError(f'{where}.{field}: expected a JSON boolean (true or false)')


def scope_field(record: dict, field: str, where: str, required: bool = False) -> None:
    if field not in record and not required:
        return
    value = record.get(field)
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f'{where}.{field}: expected an array of nonempty strings')
    if len(value) != len(set(value)):
        raise ValueError(f'{where}.{field}: duplicate scope entries')


def date_field(record: dict, field: str, where: str, issues: list[str], required: bool = False) -> None:
    if field not in record and not required:
        return
    text_field(record, field, where, required=True)
    value = record[field]
    try:
        if field == 'version_date_observed':
            observed = datetime.strptime(value, '%d %b %Y').date()
        else:
            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
                raise ValueError
            observed = date.fromisoformat(value)
    except ValueError:
        expected = 'DD Mon YYYY' if field == 'version_date_observed' else 'YYYY-MM-DD'
        raise ValueError(f'{where}.{field}: expected a valid date in {expected} format') from None
    if observed > CUTOFF:
        issues.append(f'{where}.{field}: date after {CUTOFF} cutoff')


def records(value: object, where: str) -> list[dict]:
    if not isinstance(value, list):
        raise ValueError(f'{where}: expected an array of objects')
    for position, record in enumerate(value, 1):
        if not isinstance(record, dict):
            raise ValueError(f'{where}[{position}]: expected an object')
    return value


def read_records(path: Path) -> list[dict]:
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except ValueError as exc:
        raise ValueError(f'{path}: invalid JSON: {exc}') from None
    return records(value, str(path))


def arxiv_field(record: dict, where: str, issues: list[str], required: bool = False) -> None:
    if 'arxiv_id' not in record and not required:
        return
    text_field(record, 'arxiv_id', where, required=True)
    identifier = record['arxiv_id']
    if not ARXIV_ID.fullmatch(identifier):
        issues.append(f'{where}.arxiv_id: expected a canonical identifier in the 2023–2026 range')
    elif identifier.startswith('26') and identifier[2:4] > '09':
        issues.append(f'{where}.arxiv_id: identifier falls after September 2026 cutoff')


def normalized_scope(record: dict) -> set[str]:
    return {'abstract' if item == 'author_abstract' else item for item in record.get('review_scope', [])}


def canonical_id(record: dict) -> str:
    return 'arxiv:' + record['arxiv_id'] if 'arxiv_id' in record else record['paper_id']


def audit(corpus: Path, notes: Path, abstract_notes: Path | None = None) -> tuple[dict, list[str]]:
    rows = []
    for line_number, line in enumerate(corpus.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError as exc:
            raise ValueError(f'{corpus}:{line_number}: invalid JSON: {exc}') from None
        if not isinstance(row, dict):
            raise ValueError(f'{corpus}:{line_number}: expected an object')
        rows.append(row)
    reviews = read_records(notes)
    abstracts = read_records(abstract_notes) if abstract_notes else []
    issues = []
    for position, row in enumerate(rows, 1):
        where = f'{corpus}:record[{position}]'
        for field in ('paper_id', 'title', 'source_url', 'screening_level'):
            text_field(row, field, where, required=True)
        where += f' ({row["paper_id"]})'
        for field in ('abstract_read', 'full_text_read', 'visual_reviewed'):
            bool_field(row, field, where, required=True)
        bool_field(row, 'exact_first_publication_date_verified', where)
        scope_field(row, 'review_scope', where)
        scope_field(row, 'additional_sections_inspected', where)
        for field in ('metadata_crosschecked_url', 'version_observed'):
            text_field(row, field, where)
        date_field(row, 'accessed_date', where, issues, required=True)
        date_field(row, 'version_date_observed', where, issues)
        arxiv_field(row, where, issues, required=row['paper_id'].startswith('arxiv:'))
        if 'arxiv_id' in row and row['paper_id'] != canonical_id(row):
            issues.append(f'{where}.paper_id: must equal canonical ID {canonical_id(row)}')
        for field in ('year', 'arxiv_id_year_inferred', 'arxiv_id_month_inferred'):
            if field in row and type(row[field]) is not int:
                raise ValueError(f'{where}.{field}: expected an integer')
        for number, source in enumerate(records(row.get('discovery_sources', []), f'{where}.discovery_sources'), 1):
            source_where = f'{where}.discovery_sources[{number}]'
            text_field(source, 'kind', source_where, required=True)
            text_field(source, 'url', source_where)
            date_field(source, 'accessed_date', source_where, issues)
        if not row['source_url'].startswith('https://'):
            issues.append(f'{where}.source_url: must be an explicit HTTPS provenance link')
        level = row['screening_level']
        if level not in LEVELS:
            issues.append(f'{where}.screening_level: unrecognized reading level {level!r}')
        if level == 'metadata_only' and row['abstract_read']:
            issues.append(f'{where}: metadata-only label conflicts with abstract-read flag')
        if level == 'abstract_narrative_review' and not row['abstract_read']:
            issues.append(f'{where}: abstract review label conflicts with abstract-read flag')
        if level == 'targeted_narrative_structure_review' and not row.get('review_scope'):
            issues.append(f'{where}: targeted review lacks an explicit scope')

    ids = [row['paper_id'] for row in rows]
    for label, values in (('paper IDs', ids), ('canonical paper IDs', [canonical_id(row) for row in rows])):
        duplicates = [key for key, count in Counter(values).items() if count > 1]
        if duplicates:
            issues.append(f'Duplicate {label}: {duplicates}')
    index = {row['paper_id']: row for row in rows}
    for position, review in enumerate(reviews, 1):
        where = f'{notes}[{position}]'
        text_field(review, 'paper_id', where)
        if 'paper_id' not in review and 'arxiv_id' not in review:
            raise ValueError(f'{where}: expected paper_id or arxiv_id')
        arxiv_field(review, where, issues, required=review.get('paper_id', '').startswith('arxiv:'))
        if 'arxiv_id' in review and 'paper_id' in review and review['paper_id'] != canonical_id(review):
            issues.append(f'{where}.paper_id: must equal canonical ID {canonical_id(review)}')
        for field in ('source_url', 'narrative', 'organization', 'transferable_lesson'):
            text_field(review, field, where, required=True)
        scope_field(review, 'review_scope', where, required=True)
        scope_field(review, 'additional_sections_inspected', where)
        text_field(review, 'version_observed', where)
        for field in ('full_text_read', 'visual_reviewed'):
            bool_field(review, field, where)
        date_field(review, 'accessed_date', where, issues, required=True)
        date_field(review, 'version_date_observed', where, issues)
        if not review['review_scope']:
            issues.append(f'{where}: primary review lacks an explicit scope')

    primary_keys = [canonical_id(review) for review in reviews]
    duplicate_primary = [key for key, count in Counter(primary_keys).items() if count > 1]
    if duplicate_primary:
        issues.append(f'Duplicate paper IDs in primary notes: {duplicate_primary}')
    primary_index = dict(zip(primary_keys, reviews))
    for key, review in zip(primary_keys, reviews):
        if key not in index:
            issues.append(f'{key}: primary review absent from corpus')
            continue
        row = index[key]
        if row['screening_level'] != 'targeted_narrative_structure_review':
            issues.append(f'{key}: primary review conflicts with corpus screening_level')
        if normalized_scope(row) != normalized_scope(review):
            issues.append(f'{key}: primary review_scope conflicts with corpus review_scope')
        if 'abstract' in normalized_scope(review) and row['abstract_read'] is not True:
            issues.append(f'{key}: primary abstract scope conflicts with corpus abstract_read flag')
        for field in ('version_date_observed', 'version_observed', 'full_text_read', 'visual_reviewed', 'additional_sections_inspected'):
            if field in row and field in review:
                row_value, review_value = row[field], review[field]
                if field == 'additional_sections_inspected':
                    row_value, review_value = set(row_value), set(review_value)
                if row_value != review_value:
                    issues.append(f'{key}: primary {field} conflicts with corpus')

    for position, record in enumerate(abstracts, 1):
        where = f'{abstract_notes}[{position}]'
        text_field(record, 'paper_id', where, required=True)
        bool_field(record, 'actual_abstract_read', where, required=True)
        date_field(record, 'accessed_date', where, issues, required=True)
        date_field(record, 'version_date_observed', where, issues)
        for field in ('reading_scope', 'writing_observation', 'source_url', 'issue'):
            text_field(record, field, where)
        key = record['paper_id']
        if key not in index:
            issues.append(f'{key}: abstract note absent from corpus')
            continue
        if record['actual_abstract_read']:
            if record.get('reading_scope') != 'author_abstract':
                issues.append(f'{key}: successful abstract note lacks author_abstract scope')
            if not record.get('writing_observation') or not record.get('source_url'):
                issues.append(f'{key}: abstract note lacks original observation or source')
            if index[key]['abstract_read'] is not True:
                issues.append(f'{key}: read note conflicts with index')
        elif not record.get('issue'):
            issues.append(f'{key}: unsuccessful abstract access needs an issue record')
    abstract_ids = [record['paper_id'] for record in abstracts]
    if len(abstract_ids) != len(set(abstract_ids)):
        issues.append('Duplicate paper IDs in abstract-reading notes')
    successful_ids = {record['paper_id'] for record in abstracts if record['actual_abstract_read'] is True}
    primary_abstract_ids = {key for key, review in primary_index.items() if 'abstract' in normalized_scope(review)}
    for row in rows:
        key = row['paper_id']
        if row['abstract_read'] is True and key not in successful_ids | primary_abstract_ids:
            issues.append(f'{key}: abstract-read flag lacks a corresponding reading note with abstract scope')
        if row['screening_level'] == 'targeted_narrative_structure_review' and key not in primary_index:
            issues.append(f'{key}: targeted review lacks a corresponding primary reading note')

    summary = {
        'total_unique': len({canonical_id(row) for row in rows}),
        'hf_unique': len({canonical_id(row) for row in rows if any(source['kind'] == 'hugging_face_monthly' for source in row.get('discovery_sources', []))}),
        'official_icml_metadata_crosschecked': len({canonical_id(row) for row in rows if row.get('metadata_crosschecked_url')}),
        'primary_targeted_reviews': len(primary_index),
        'abstracts_read': sum(row['abstract_read'] is True for row in rows),
        'abstract_only_note_records': len(successful_ids),
        'unavailable_abstract_records': sum(record['actual_abstract_read'] is False for record in abstracts),
        'abstract_source_limitation_records': sum(bool(record.get('issue')) for record in abstracts),
        'full_paper_reviews': sum(row['full_text_read'] is True for row in rows),
        'visual_reviews': sum(row['visual_reviewed'] is True for row in rows),
        'levels': dict(Counter(row['screening_level'] for row in rows)),
        'year_basis': 'Identifier-inferred year for arXiv; proceedings year for PMLR. Not certified first-publication year.',
        'years': dict(Counter(str(row.get('year', row.get('arxiv_id_year_inferred'))) for row in rows)),
    }
    return summary, issues


def main() -> int:
    base = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--corpus', type=Path, default=base / 'references/research/paper-corpus.jsonl')
    parser.add_argument('--notes', type=Path, default=base / 'references/research/primary-paper-notes.json')
    parser.add_argument('--abstract-notes', type=Path, default=base / 'references/research/abstract-reading-notes.json')
    args = parser.parse_args()
    try:
        summary, issues = audit(args.corpus, args.notes, args.abstract_notes)
    except (OSError, ValueError, KeyError) as exc:
        print(f'Corpus audit could not complete: {exc}', file=sys.stderr)
        return 1
    print(json.dumps({'summary': summary, 'issues': issues}, indent=2))
    return int(bool(issues))


if __name__ == '__main__':
    raise SystemExit(main())
