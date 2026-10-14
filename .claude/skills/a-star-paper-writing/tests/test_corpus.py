"""Regression tests for corpus bookkeeping, using synthetic custom input files."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(os.environ.get('PAPER_SKILL_DIR', Path(__file__).resolve().parents[1]))
AUDIT = SKILL / 'scripts' / 'audit_corpus.py'


class CorpusAuditTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.corpus = self.root / 'custom-corpus.jsonl'
        self.notes_path = self.root / 'custom-primary.json'
        self.abstracts_path = self.root / 'custom-abstracts.json'
        self.rows = [{
            'paper_id': 'arxiv:2401.00001', 'arxiv_id': '2401.00001',
            'title': 'Synthetic primary paper', 'source_url': 'https://example.org/primary',
            'accessed_date': '2026-09-17', 'version_date_observed': '01 Jan 2024',
            'version_observed': '2401.00001v1',
            'screening_level': 'targeted_narrative_structure_review',
            'abstract_read': True, 'full_text_read': False, 'visual_reviewed': False,
            'review_scope': ['abstract', 'main_section_outline'],
            'arxiv_id_year_inferred': 2024, 'arxiv_id_month_inferred': 1,
            'discovery_sources': [{'kind': 'hugging_face_monthly', 'url': 'https://example.org/month', 'accessed_date': '2026-09-17'}],
        }, {
            'paper_id': 'pmlr:synthetic', 'title': 'Synthetic proceedings paper',
            'source_url': 'https://example.org/proceedings', 'accessed_date': '2026-09-17',
            'screening_level': 'abstract_narrative_review', 'review_scope': ['author_abstract'],
            'abstract_read': True, 'full_text_read': False, 'visual_reviewed': False, 'year': 2023,
        }]
        self.notes = [{
            'arxiv_id': '2401.00001', 'source_url': 'https://example.org/primary',
            'accessed_date': '2026-09-17', 'version_date_observed': '01 Jan 2024',
            'version_observed': '2401.00001v1', 'review_scope': ['abstract', 'main_section_outline'],
            'narrative': 'Synthetic narrative observation.', 'organization': 'Synthetic organization observation.',
            'transferable_lesson': 'Synthetic writing lesson.', 'full_text_read': False, 'visual_reviewed': False,
        }]
        self.abstracts = [{
            'paper_id': 'pmlr:synthetic', 'actual_abstract_read': True,
            'accessed_date': '2026-09-17', 'source_url': 'https://example.org/proceedings',
            'reading_scope': 'author_abstract', 'writing_observation': 'Synthetic abstract observation.',
        }]

    def save(self):
        self.corpus.write_text(''.join(json.dumps(row) + '\n' for row in self.rows), encoding='utf-8')
        self.notes_path.write_text(json.dumps(self.notes), encoding='utf-8')
        self.abstracts_path.write_text(json.dumps(self.abstracts), encoding='utf-8')

    def run_audit(self, save=True):
        if save:
            self.save()
        result = subprocess.run([
            sys.executable, str(AUDIT), '--corpus', str(self.corpus), '--notes', str(self.notes_path),
            '--abstract-notes', str(self.abstracts_path),
        ], capture_output=True, text=True)
        self.assertNotIn('Traceback', result.stderr)
        return result, json.loads(result.stdout) if result.stdout else None

    def assert_issue(self, report, fragment):
        self.assertTrue(any(fragment in issue for issue in report['issues']), report)

    def test_custom_inputs_and_proceedings_without_arxiv_id_pass(self):
        result, report = self.run_audit()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report['issues'], [])
        self.assertEqual(report['summary']['total_unique'], 2)
        self.assertEqual(report['summary']['abstracts_read'], 2)
        self.assertEqual(report['summary']['full_paper_reviews'], 0)
        self.assertEqual(report['summary']['visual_reviews'], 0)

    def test_minimal_metadata_only_proceedings_record_passes(self):
        self.rows = [{'paper_id': 'pmlr:custom', 'title': 'Synthetic metadata',
                      'source_url': 'https://example.org/metadata', 'accessed_date': '2026-09-17',
                      'screening_level': 'metadata_only', 'abstract_read': False,
                      'full_text_read': False, 'visual_reviewed': False}]
        self.notes = []
        self.abstracts = []
        result, report = self.run_audit()
        self.assertEqual(result.returncode, 0, result.stderr or report)
        self.assertEqual(report['summary']['total_unique'], 1)
        self.assertEqual(report['summary']['abstracts_read'], 0)
        self.assertEqual(report['summary']['primary_targeted_reviews'], 0)

    def test_minimal_custom_primary_note_does_not_need_shipped_metadata(self):
        self.rows = self.rows[:1]
        self.abstracts = []
        for field in ('version_date_observed', 'version_observed', 'discovery_sources',
                      'arxiv_id_year_inferred', 'arxiv_id_month_inferred'):
            self.rows[0].pop(field)
        for field in ('version_date_observed', 'version_observed', 'full_text_read', 'visual_reviewed'):
            self.notes[0].pop(field)
        result, report = self.run_audit()
        self.assertEqual(result.returncode, 0, result.stderr or report)
        self.assertEqual(report['summary']['primary_targeted_reviews'], 1)

    def test_primary_note_can_link_a_proceedings_paper_without_arxiv_id(self):
        self.rows[1]['screening_level'] = 'targeted_narrative_structure_review'
        self.rows[1]['review_scope'] = ['author_abstract', 'introduction_excerpt']
        note = {key: self.notes[0][key] for key in
                ('accessed_date', 'narrative', 'organization', 'transferable_lesson')}
        note.update(paper_id='pmlr:synthetic', source_url='https://example.org/proceedings',
                    review_scope=['abstract', 'introduction_excerpt'])
        self.notes.append(note)
        self.abstracts = []
        result, report = self.run_audit()
        self.assertEqual(result.returncode, 0, result.stderr or report)
        self.assertEqual(report['summary']['primary_targeted_reviews'], 2)
        self.assertEqual(report['summary']['abstracts_read'], 2)

    def test_primary_paper_id_must_match_supplied_arxiv_id(self):
        self.notes[0]['paper_id'] = 'arxiv:2401.00001v2'
        result, report = self.run_audit()
        self.assertEqual(result.returncode, 1)
        self.assert_issue(report, '.paper_id: must equal canonical ID arxiv:2401.00001')

    def test_additional_section_order_does_not_create_false_conflict(self):
        self.rows[0]['additional_sections_inspected'] = ['evaluation excerpt', 'appendix excerpt']
        self.notes[0]['additional_sections_inspected'] = ['appendix excerpt', 'evaluation excerpt']
        result, report = self.run_audit()
        self.assertEqual(result.returncode, 0, result.stderr or report)

    def test_shipped_corpus_counts_unchanged(self):
        result = subprocess.run([sys.executable, str(AUDIT)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['issues'], [])
        expected = {'total_unique': 622, 'hf_unique': 557, 'official_icml_metadata_crosschecked': 50,
                    'primary_targeted_reviews': 20, 'abstracts_read': 622, 'abstract_only_note_records': 602,
                    'unavailable_abstract_records': 0, 'abstract_source_limitation_records': 1,
                    'full_paper_reviews': 0, 'visual_reviews': 0}
        for key, value in expected.items():
            self.assertEqual(report['summary'][key], value, key)

    def test_duplicate_primary_note_is_rejected_and_not_counted_twice(self):
        self.notes.append(copy.deepcopy(self.notes[0]))
        result, report = self.run_audit()
        self.assertEqual(result.returncode, 1)
        self.assert_issue(report, 'Duplicate paper IDs in primary notes')
        self.assertEqual(report['summary']['primary_targeted_reviews'], 1)

    def test_canonical_arxiv_version_duplicate_is_rejected_and_not_counted_twice(self):
        duplicate = copy.deepcopy(self.rows[0])
        duplicate.update(paper_id='arxiv:2401.00001v2', screening_level='metadata_only', abstract_read=False, review_scope=[])
        self.rows.append(duplicate)
        result, report = self.run_audit()
        self.assertEqual(result.returncode, 1)
        self.assert_issue(report, 'must equal canonical ID')
        self.assert_issue(report, 'Duplicate canonical paper IDs')
        self.assertEqual(report['summary']['total_unique'], 2)
        self.assertEqual(report['summary']['hf_unique'], 1)

    def test_targeted_row_needs_matching_primary_note(self):
        self.rows[1]['screening_level'] = 'targeted_narrative_structure_review'
        self.rows[1]['review_scope'] = ['author_abstract', 'introduction_excerpt']
        result, report = self.run_audit()
        self.assertEqual(result.returncode, 1)
        self.assert_issue(report, 'targeted review lacks a corresponding primary reading note')

    def test_primary_abstract_scope_and_index_flag_must_agree(self):
        self.rows[0]['abstract_read'] = False
        result, report = self.run_audit()
        self.assertEqual(result.returncode, 1)
        self.assert_issue(report, 'primary abstract scope conflicts with corpus abstract_read flag')

    def test_primary_and_index_scopes_must_agree(self):
        self.notes[0]['review_scope'].append('appendix_outline')
        result, report = self.run_audit()
        self.assertEqual(result.returncode, 1)
        self.assert_issue(report, 'primary review_scope conflicts')

    def test_scope_order_and_abstract_alias_do_not_create_false_conflict(self):
        self.notes[0]['review_scope'] = ['main_section_outline', 'author_abstract']
        result, report = self.run_audit()
        self.assertEqual(result.returncode, 0, result.stderr or report)

    def test_primary_without_abstract_scope_cannot_support_abstract_flag(self):
        self.rows[0]['review_scope'] = ['main_section_outline']
        self.notes[0]['review_scope'] = ['main_section_outline']
        result, report = self.run_audit()
        self.assertEqual(result.returncode, 1)
        self.assert_issue(report, 'abstract-read flag lacks a corresponding reading note with abstract scope')

    def test_separate_abstract_note_can_support_primary_without_abstract_scope(self):
        self.rows[0]['review_scope'] = ['main_section_outline']
        self.notes[0]['review_scope'] = ['main_section_outline']
        record = copy.deepcopy(self.abstracts[0])
        record['paper_id'] = self.rows[0]['paper_id']
        self.abstracts.append(record)
        result, report = self.run_audit()
        self.assertEqual(result.returncode, 0, result.stderr or report)

    def test_non_boolean_read_flags_are_rejected_with_field_diagnostic(self):
        cases = [(self.rows[0], 'abstract_read'), (self.rows[0], 'full_text_read'),
                 (self.rows[0], 'visual_reviewed'), (self.notes[0], 'full_text_read'),
                 (self.abstracts[0], 'actual_abstract_read')]
        for record, field in cases:
            original = record[field]
            for invalid in ('false', 0, 1, None, []):
                with self.subTest(field=field, invalid=invalid):
                    record[field] = invalid
                    result, report = self.run_audit()
                    self.assertEqual(result.returncode, 1)
                    self.assertIsNone(report)
                    self.assertIn(field + ': expected a JSON boolean', result.stderr)
            record[field] = original

    def test_only_true_flags_increase_full_and_visual_counts(self):
        self.rows[0]['full_text_read'] = self.notes[0]['full_text_read'] = True
        self.rows[0]['visual_reviewed'] = self.notes[0]['visual_reviewed'] = True
        result, report = self.run_audit()
        self.assertEqual(result.returncode, 0, result.stderr or report)
        self.assertEqual(report['summary']['full_paper_reviews'], 1)
        self.assertEqual(report['summary']['visual_reviews'], 1)

    def test_future_dates_are_checked_in_corpus_primary_abstract_and_discovery(self):
        cases = [(self.rows[0], 'accessed_date', '2026-09-18'),
                 (self.rows[0], 'version_date_observed', '18 Sep 2026'),
                 (self.notes[0], 'version_date_observed', '18 Sep 2026'),
                 (self.notes[0], 'accessed_date', '2026-09-18'),
                 (self.abstracts[0], 'accessed_date', '2026-09-18'),
                 (self.rows[0]['discovery_sources'][0], 'accessed_date', '2026-09-18')]
        for record, field, value in cases:
            with self.subTest(field=field, value=value):
                original = record[field]
                record[field] = value
                result, report = self.run_audit()
                self.assertEqual(result.returncode, 1)
                self.assert_issue(report, field + ': date after 2026-09-17 cutoff')
                record[field] = original

    def test_conflicting_reviewed_versions_are_rejected(self):
        self.notes[0]['version_date_observed'] = '02 Jan 2024'
        self.notes[0]['version_observed'] = '2401.00001v2'
        result, report = self.run_audit()
        self.assertEqual(result.returncode, 1)
        self.assert_issue(report, 'primary version_date_observed conflicts')
        self.assert_issue(report, 'primary version_observed conflicts')

    def test_malformed_fields_have_location_and_no_traceback(self):
        cases = [(self.rows[0], 'arxiv_id', None, 'custom-corpus.jsonl'),
                 (self.rows[0], 'paper_id', [], 'custom-corpus.jsonl'),
                 (self.rows[0], 'discovery_sources', [None], 'custom-corpus.jsonl'),
                 (self.rows[0], 'review_scope', 'abstract', 'custom-corpus.jsonl'),
                 (self.notes[0], 'arxiv_id', None, 'custom-primary.json'),
                 (self.notes[0], 'version_date_observed', '31 Feb 2026', 'custom-primary.json'),
                 (self.abstracts[0], 'paper_id', {}, 'custom-abstracts.json'),
                 (self.abstracts[0], 'accessed_date', '2026-9-17', 'custom-abstracts.json')]
        for record, field, invalid, filename in cases:
            with self.subTest(field=field, invalid=invalid):
                original = record[field]
                record[field] = invalid
                result, report = self.run_audit()
                self.assertEqual(result.returncode, 1)
                self.assertIsNone(report)
                self.assertIn(filename, result.stderr)
                self.assertIn(field, result.stderr)
                record[field] = original

    def test_malformed_roots_and_record_shapes_have_no_tracebacks(self):
        self.save()
        for path in (self.notes_path, self.abstracts_path, self.corpus):
            original = path.read_text()
            for invalid in ('null', '{}', '[null]', '"record"', '{invalid'):
                if path == self.corpus and invalid == '{}':
                    continue
                with self.subTest(path=path.name, invalid=invalid):
                    path.write_text(invalid)
                    result, report = self.run_audit(save=False)
                    self.assertEqual(result.returncode, 1)
                    self.assertIsNone(report)
                    self.assertIn(path.name, result.stderr)
            path.write_text(original)


if __name__ == '__main__':
    unittest.main()
