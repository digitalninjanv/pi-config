import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "analyze-sessions" / "scripts"))
import sessions

class SessionTests(unittest.TestCase):
    def test_parse_date_relative_and_iso(self):
        self.assertIsNotNone(sessions.parse_date("7d").tzinfo)
        self.assertEqual(sessions.parse_date("2026-09-17").hour, 0)

    def test_summary_is_one_pass_and_tolerates_bad_json(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "x.jsonl"
            p.write_text(
                '{"type":"session","id":"abc","cwd":"/tmp"}\n'
                '{bad json\n'
                '{"type":"message","message":{"role":"user","content":[{"type":"text","text":"hello"}]}}\n'
                '{"type":"message","message":{"role":"assistant","model":"m","provider":"openai","usage":{"cost":{"total":0.1},"input":2,"output":3}}}\n'
            )
            s = sessions.summarize_session(p)
            self.assertEqual(s.id, "abc")
            self.assertEqual(s.user_count, 1)
            self.assertEqual(s.cost_total, 0.1)
            self.assertEqual(s.tok_input, 2)

if __name__ == "__main__":
    unittest.main()
