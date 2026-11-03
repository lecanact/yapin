import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
CORE = ("Bot", "Cog", "command", "listener", "button", "YapperError", "row", "btn", "link_button")


def run(code, cwd, extra_env=None):
    """Run Python in a fresh process (the .env is read at import time) with no YAP* token variables set."""
    env = {k: v for k, v in os.environ.items() if not k.startswith(("YAPPER_", "YAPIN_"))}
    env["PYTHONPATH"] = str(SRC)
    env.update(extra_env or {})
    return subprocess.run([sys.executable, "-c", code], cwd=cwd, env=env, capture_output=True, text=True, timeout=60)


class ApiSurfaceTests(unittest.TestCase):
    def test_package_exposes_the_yapper_api(self):
        import yapin

        for name in CORE:
            self.assertTrue(hasattr(yapin, name), name)

    def test_package_is_yapper_not_a_copy(self):
        import yapin
        import yapper.main

        self.assertIs(yapin.Bot, yapper.main.Bot)
        self.assertIs(yapin.Cog, yapper.main.Cog)
        self.assertEqual(yapin.__version__, yapper.main.__version__)

    def test_package_exports_everything_yapper_lists(self):
        import yapin
        from yapper import main

        for name in main.__all__:
            self.assertTrue(hasattr(yapin, name), name)
            self.assertIn(name, yapin.__all__)

    def test_old_yapin_error_name_still_works(self):
        import yapin

        self.assertIs(yapin.YapinError, yapin.YapperError)
        with self.assertRaises(yapin.YapinError):
            raise yapin.YapperError("boom", 500)


class TokenTests(unittest.TestCase):
    CODE = "import yapin; print(yapin.Bot(log=False).token)"

    def test_yapin_bot_token_variable_is_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            r = run(self.CODE, d, {"YAPIN_BOT_TOKEN": "yb_from_yapin_var"})
            self.assertEqual(r.stdout.strip(), "yb_from_yapin_var", r.stderr)

    def test_yapper_bot_token_wins_over_yapin_bot_token(self):
        with tempfile.TemporaryDirectory() as d:
            r = run(self.CODE, d, {"YAPIN_BOT_TOKEN": "yb_a", "YAPPER_BOT_TOKEN": "yb_b"})
            self.assertEqual(r.stdout.strip(), "yb_b", r.stderr)

    def test_env_file_is_loaded(self):
        with tempfile.TemporaryDirectory() as d:
            (pathlib.Path(d) / ".env").write_text("YAPIN_BOT_TOKEN=yb_from_dotenv\n")
            r = run(self.CODE, d)
            self.assertEqual(r.stdout.strip(), "yb_from_dotenv", r.stderr)

    def test_real_environment_beats_env_file(self):
        with tempfile.TemporaryDirectory() as d:
            (pathlib.Path(d) / ".env").write_text("YAPIN_BOT_TOKEN=yb_from_file\n")
            r = run(self.CODE, d, {"YAPIN_BOT_TOKEN": "yb_from_env"})
            self.assertEqual(r.stdout.strip(), "yb_from_env", r.stderr)


if __name__ == "__main__":
    unittest.main()
