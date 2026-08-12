from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from px00.dependency_provenance import validate_dependency_provenance


ROOT = Path(__file__).resolve().parents[1]
REQ = ROOT / "requirements-validator.txt"
SBOM = ROOT / "security" / "sbom" / "PX00-validator.cdx.json"


class DependencyProvenanceTests(unittest.TestCase):
    def test_current_repository_dependency_provenance(self) -> None:
        self.assertEqual(validate_dependency_provenance(REQ, SBOM), [])

    def test_requirement_drift_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            req = root / "requirements.txt"
            sbom = root / "bom.json"
            req.write_text("PyYAML==6.0.2\n", encoding="utf-8")
            sbom.write_text(SBOM.read_text(encoding="utf-8"), encoding="utf-8")
            issues = validate_dependency_provenance(req, sbom)
            self.assertTrue(any("requirements/SBOM mismatch" in issue for issue in issues))

    def test_unpinned_requirement_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            req = root / "requirements.txt"
            sbom = root / "bom.json"
            req.write_text("PyYAML>=6\n", encoding="utf-8")
            sbom.write_text(SBOM.read_text(encoding="utf-8"), encoding="utf-8")
            issues = validate_dependency_provenance(req, sbom)
            self.assertTrue(any("not an exact name==version pin" in issue for issue in issues))

    def test_missing_root_dependency_graph_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            req = root / "requirements.txt"
            sbom = root / "bom.json"
            req.write_text(REQ.read_text(encoding="utf-8"), encoding="utf-8")
            value = json.loads(SBOM.read_text(encoding="utf-8"))
            value["dependencies"] = []
            sbom.write_text(json.dumps(value), encoding="utf-8")
            issues = validate_dependency_provenance(req, sbom)
            self.assertTrue(any("root component" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
