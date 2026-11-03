import pathlib, tomllib, unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class MetadataTests(unittest.TestCase):
    def test_pyproject_has_expected_publish_metadata(self):
        data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        project = data["project"]
        self.assertEqual(project["name"], "yapin")
        self.assertEqual(project["license"], "GPL-3.0-only")
        self.assertIn("python-dotenv>=1.2.4", project["dependencies"])

    def test_package_is_built_on_yapper_py(self):
        data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        deps = data["project"]["dependencies"]
        self.assertTrue(any(d.replace(" ", "").startswith("yapper.py>=") for d in deps), deps)

    def test_readme_exists_and_is_not_empty(self):
        readme = ROOT / "README.md"
        self.assertTrue(readme.exists())
        self.assertGreater(len(readme.read_text(encoding="utf-8").strip()), 0)


if __name__ == "__main__":
    unittest.main()
