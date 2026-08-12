from __future__ import annotations

import unittest
from pathlib import Path

from px00.secret_hygiene import scan_repository, scan_text


ROOT = Path(__file__).resolve().parents[1]


class SecretHygieneTests(unittest.TestCase):
    def test_current_repository_has_no_detected_secret_material(self) -> None:
        findings, errors = scan_repository(ROOT)
        self.assertEqual(errors, [])
        self.assertEqual(findings, [])

    def test_github_token_like_value_is_rejected(self) -> None:
        token = "gh" + "p_" + ("A" * 36)
        findings = scan_text(f"token={token}\n", "fixture.txt")
        self.assertTrue(any(item.kind == "github_pat" for item in findings))
        self.assertTrue(all(token not in item.message for item in findings))

    def test_private_key_header_is_rejected_without_echoing_value(self) -> None:
        marker = "-----BEGIN " + "PRIVATE KEY-----"
        findings = scan_text(marker + "\n", "fixture.pem")
        self.assertTrue(any(item.kind == "private_key" for item in findings))
        self.assertTrue(all(marker not in item.message for item in findings))

    def test_generic_secret_assignment_is_rejected(self) -> None:
        key = "client" + "_secret"
        value = "candidate" + "Value123"
        findings = scan_text(f"{key}={value}\n", "fixture.env")
        self.assertTrue(any(item.kind == "generic_secret_assignment" for item in findings))
        self.assertTrue(all(value not in item.message for item in findings))

    def test_placeholder_assignment_is_allowed(self) -> None:
        key_one = "api" + "_key"
        key_two = "pass" + "word"
        fixture = f"{key_one}=replace_me\n{key_two}=not_set\n"
        findings = scan_text(fixture, "fixture.env")
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
