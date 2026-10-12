import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from generate_data import generate
from brain import readiness

class BrainTests(unittest.TestCase):
    def test_generation(self):
        with TemporaryDirectory() as folder:
            self.assertEqual(generate(Path(folder)), 9)
            self.assertIn('PHI', (Path(folder) / '03_support_ticket.md').read_text())
    def test_readiness(self):
        score = readiness()
        self.assertEqual(sum(x['status'] == 'BLOCKED' for x in score), 4)
        self.assertEqual(sum(x['status'] == 'AT RISK' for x in score), 1)

if __name__ == '__main__':
    unittest.main()
