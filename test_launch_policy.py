"""Standalone policy checks, no API calls or Streamlit required."""
import ast
import copy
import unittest
from pathlib import Path
from types import SimpleNamespace

SOURCE = Path(__file__).with_name('hydra_dashboard_policy.py')
tree = ast.parse(SOURCE.read_text())
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'apply_launch_policy')
module = ast.Module(body=[fn], type_ignores=[])
namespace = {
    'GATE_DEFINITIONS': [
        {'id': i, 'gate': label} for i, label in [
            ('phi_security', 'PHI remediation and independent verification'),
            ('answer_accuracy', 'Approved answer accuracy ≥95%'),
            ('clinical_escalation', 'Critical escalation =100%'),
            ('latency', 'p95 latency <3 seconds'),
            ('audit_retention', 'Audit retention sign-off'),
        ]
    ],
    'UPDATE_PREFIX': 'csb-update-',
}
exec(compile(module, str(SOURCE), 'exec'), namespace)
policy = namespace['apply_launch_policy']

def chunks(include_updates=True):
    files = ['04_eval_report.md', '05_performance.md', '07_security_policy.md',
             '08_action_tracker.md', '02_architecture.md']
    if include_updates:
        files.append('csb-update-2026-10-12-demo.md')
    return [SimpleNamespace(source_title=f, chunk_content='Synthetic test evidence') for f in files]

def model_report(status):
    return {'gates': [{'gate': g['gate'], 'status': status,
                       'observed': 'model text', 'missing_evidence': '', 'sources': []}
                      for g in namespace['GATE_DEFINITIONS']],
            'recommendation': 'GO', 'summary': 'Model says GO'}

class LaunchPolicyTests(unittest.TestCase):
    def test_never_approves_from_model_claim(self):
        result = policy(model_report('PASS'), chunks())
        self.assertEqual([g['status'] for g in result['gates']],
                         ['PENDING_VERIFICATION','FAIL','FAIL','FAIL','PENDING_VERIFICATION'])
        self.assertIn('NO-GO', result['recommendation'])

    def test_missing_source_fails_closed(self):
        with self.assertRaisesRegex(ValueError, 'requires source evidence'):
            policy(model_report('PASS'), chunks()[:-2])

    def test_missing_update_does_not_claim_deployment(self):
        result = policy(model_report('UNKNOWN'), chunks(False))
        self.assertNotIn('deployed to staging', result['gates'][0]['observed'])

if __name__ == '__main__':
    unittest.main()
