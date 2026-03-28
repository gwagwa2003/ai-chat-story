import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from server import config


class ConfigTests(unittest.TestCase):
    def test_load_dotenv_sets_missing_values_only(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            env_path = Path(tmpdir) / ".env"
            env_path.write_text(
                "OPENAI_API_KEY=from_file\nANTHROPIC_API_KEY='anthropic_file'\n",
                encoding="utf-8",
            )

            with patch.dict(os.environ, {"OPENAI_API_KEY": "existing"}, clear=True):
                config.load_dotenv(env_path)
                self.assertEqual(os.environ["OPENAI_API_KEY"], "existing")
                self.assertEqual(os.environ["ANTHROPIC_API_KEY"], "anthropic_file")

    def test_require_env_raises_for_missing_value(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(RuntimeError):
                config.require_env("OPENAI_API_KEY")

    def test_resolve_project_path_handles_relative_path(self):
        resolved = Path(config.resolve_project_path("server/Voice/ly_refaudio.wav"))
        self.assertEqual(
            resolved,
            (config.PROJECT_ROOT / "server/Voice/ly_refaudio.wav").resolve(),
        )


if __name__ == "__main__":
    unittest.main()
