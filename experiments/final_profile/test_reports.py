"""T18/T19/T20/T27 negative contracts; synthetic rows are never empirical results."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from instrument import generate, SOURCES
from reports import read_events, complete, load_bundle, build, early_stop, core_cost, match, cost_associations


def event(kind, seq=1, **fields):
    return {'schema': 'vflhcds.final_profile', 'version': 1, 'seq': seq, 'event': kind,
            'elapsed_ns': 12, 'phases_ns': {'count': 10}, 'boundary_residual_ns': 2,
            'work': {}, **fields}


class Contracts(unittest.TestCase):
    def test_T18_partial_and_malformed_stream(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'events'
            path.write_text(json.dumps(event('phase_begin', phase='max_flow')) + '\n{"unfinished":')
            events = read_events(path)
            self.assertEqual(len(events), 1)
            self.assertFalse(complete(events))
            self.assertEqual(events[-1]['phase'], 'max_flow')
            path.write_text(json.dumps(event('finish', complete=True, boundary_residual_ns=0)) + '\n')
            with self.assertRaises(ValueError): read_events(path)
            path.write_text(json.dumps(event('finish', seq=2, complete=True)) + '\n')
            with self.assertRaises(ValueError): read_events(path)

    def test_T20_reversible_generation_and_anchor_rejection(self):
        root = Path(__file__).resolve().parents[2]
        for source in SOURCES:
            original = (root / source).read_bytes()
            a, edits = generate(source, original)
            b, _ = generate(source, original)
            self.assertEqual(a, b)
            self.assertGreater(edits, 0)
        with self.assertRaises(ValueError): generate('src/solver/solver.cpp', b'no matching anchor')

    def bundle(self):
        return {'schema': 1, 'scope': 'development', 'host': 'test-host',
                'schedule': ['a', 'missing'], 'pins': {'VF': {'source_sha256': 'source', 'control': 'binary'}},
                'rows': [{'run_id': 'a', 'scope': 'development', 'host': 'test-host', 'algorithm': 'VF',
                          'source_sha256': 'source', 'binary_sha256': 'binary', 'role': 'control',
                          'status': 'timeout', 'suite': 'unit', 'graph_sha256': 'g', 'h': 3,
                          'k': 1, 'core': 'off', 'work_mode': 'global', 'repeat': 0}]}

    def test_T27_pins_duplicates_scope_missing_and_censored(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bundle.json'
            bundle = self.bundle()
            path.write_text(json.dumps(bundle))
            loaded = load_bundle(path)
            self.assertEqual(loaded['missing_run_ids'], ['missing'])
            report = build(loaded)
            self.assertEqual(report['outcomes']['timeout'], 1)
            self.assertEqual(report['vf_ippv'][0]['coverage'], 'unavailable_pair')
            self.assertEqual(report['early_stop'][0]['coverage'], 'unavailable_suffix')
            self.assertEqual(json.dumps(report, sort_keys=True), json.dumps(build(load_bundle(path)), sort_keys=True))
            with self.assertRaises(ValueError): load_bundle(path, formal=True)
            for field, value in [('source_sha256', 'other-source'), ('binary_sha256', 'other-binary'),
                                 ('scope', 'formal-m8'), ('status', 'success-ish'), ('host', 'other-host')]:
                bad = copy.deepcopy(bundle); bad['rows'][0][field] = value
                path.write_text(json.dumps(bad))
                with self.assertRaises(ValueError): load_bundle(path)
            bad = copy.deepcopy(bundle); bad['rows'] *= 2
            path.write_text(json.dumps(bad))
            with self.assertRaises(ValueError): load_bundle(path)

    def test_T27_suffix_is_after_rank_not_after_query(self):
        rows = []
        for role in ('control', 'diagnostic'):
            for k in (1, 'all'):
                row = dict(self.bundle()['rows'][0], run_id=f'{role}-{k}', role=role, k=k, status='completed',
                           wall_seconds=1 if k == 1 else 2, peak_rss_bytes=100, output_data=[{'vertices': [0]}])
                if k == 'all': row['output_data'].append({'vertices': [1]})
                row['events_data'] = [event('index', work={'cliques_appended': 3}),
                    event('rank_ready', rank=1, pending_intervals=1,
                          work={'cliques_appended': 3, 'count_clique_visits': 6, 'accepted_components': 2}),
                    event('solve_end', work={'cliques_appended': 3, 'count_clique_visits': 9, 'accepted_components': 2}),
                    event('finish', complete=True, work={'cliques_appended': 3, 'count_clique_visits': 6 if k == 1 else 9,
                                                        'accepted_components': 2})]
                rows.append(row)
        report = early_stop({'rows': rows})[0]
        self.assertEqual(report['suffix_work']['count_clique_visits'], 3)
        self.assertEqual(report['suffix_work']['accepted_components'], 0)
        self.assertEqual(report['unavoidable_initial_work'], {'cliques_appended': 3})
        rows[0]['output_data'] = [{'vertices': [2]}]
        with self.assertRaises(ValueError): early_stop({'rows': rows})

    def test_T27_core_disagreement_rejected(self):
        rows = []
        for role in ('control', 'diagnostic'):
            for core in ('off', 'safe'):
                row = dict(self.bundle()['rows'][0], run_id=role+core, role=role, core=core, status='completed',
                           wall_seconds=1, peak_rss_bytes=100, output_data=[{'vertices': [0 if core == 'off' else 1]}],
                           events_data=[event('finish', complete=True)])
                rows.append(row)
        with self.assertRaises(ValueError): core_cost({'rows': rows})

    def test_T27_identical_graphs_in_distinct_fixtures_do_not_cross_join(self):
        rows = []
        for fixture in ('split_nonoutput', 'peeling_tail_1'):
            for role in ('control', 'diagnostic'):
                rows.append(dict(self.bundle()['rows'][0], run_id=fixture+role, suite='development:'+fixture, role=role))
        self.assertEqual(match(rows, rows[0], role='diagnostic')['run_id'], 'split_nonoutputdiagnostic')
        for row in rows: row['suite'] = 'ambiguous'
        with self.assertRaises(ValueError): match(rows, rows[0], role='diagnostic')

    def test_T27_vf_ippv_positive_join_preserves_unavailable_internal_phases(self):
        vf = dict(self.bundle()['rows'][0], status='completed', wall_seconds=2, peak_rss_bytes=3)
        ippv = dict(vf, run_id='ippv', algorithm='IPPV', wall_seconds=4, peak_rss_bytes=5)
        report = cost_associations({'rows': [vf, ippv]})[0]
        self.assertEqual(report['coverage'], 'paired')
        self.assertEqual(report['ippv_wall_seconds'], 4)
        self.assertIsNone(report['ippv_internal_phases'])


if __name__ == '__main__':
    unittest.main()
