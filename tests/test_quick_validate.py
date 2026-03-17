import importlib.util
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPO_ROOT / "skills" / "mint" / "scripts" / "quick_validate.py"


def load_validate_skill():
    spec = importlib.util.spec_from_file_location("quick_validate", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.validate_skill


def write_skill(root: Path, frontmatter: str, body: str = "# Title\n") -> Path:
    skill_dir = root / "fixture"
    skill_dir.mkdir()
    frontmatter = textwrap.dedent(frontmatter).strip()
    content = f"---\n{frontmatter}\n---\n\n{body}"
    (skill_dir / "SKILL.md").write_text(content)
    return skill_dir


class QuickValidateTests(unittest.TestCase):
    def test_accepts_skill_without_protocol_interface_fields(self):
        validate_skill = load_validate_skill()
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = write_skill(
                Path(tmpdir),
                """
                name: mint
                description: Validate a regular skill.
                metadata:
                  version: "1.0.0"
                """,
            )

            valid, message = validate_skill(skill_dir)

        self.assertTrue(valid, message)

    def test_accepts_protocol_with_required_interface_fields(self):
        validate_skill = load_validate_skill()
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = write_skill(
                Path(tmpdir),
                """
                name: begin
                description: Start a work session.
                requires: []
                accepts: []
                produces: []
                may_produce: []
                trigger:
                  on_signal: session-start
                """,
            )

            valid, message = validate_skill(skill_dir)

        self.assertTrue(valid, message)

    def test_rejects_protocol_missing_required_interface_field(self):
        validate_skill = load_validate_skill()
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = write_skill(
                Path(tmpdir),
                """
                name: begin
                description: Start a work session.
                requires: []
                accepts: []
                produces: []
                trigger:
                  on_signal: session-start
                """,
            )

            valid, message = validate_skill(skill_dir)

        self.assertFalse(valid)
        self.assertIn("may_produce", message)

    def test_rejects_file_missing_name(self):
        validate_skill = load_validate_skill()
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = write_skill(
                Path(tmpdir),
                """
                description: Missing the required name.
                """,
            )

            valid, message = validate_skill(skill_dir)

        self.assertFalse(valid)
        self.assertIn("Missing 'name'", message)


if __name__ == "__main__":
    unittest.main()
