import unittest

from px00.knowledge_snapshots import KnowledgeSnapshotBuilder, SnapshotObjectRef


D1 = "1" * 64
D2 = "2" * 64
COMMIT1 = "a" * 40
COMMIT2 = "b" * 40


class KnowledgeSnapshotBuilderTests(unittest.TestCase):
    def setUp(self):
        self.builder = KnowledgeSnapshotBuilder()
        self.obj1 = SnapshotObjectRef("SEC-SRC-0001", "v1", D1, "KB-SECURITY")
        self.obj2 = SnapshotObjectRef("SEC-REQ-0001", "v3", D2, "KB-SECURITY")

    def build(self, **overrides):
        args = {
            "snapshot_id": "KSNAP-SEC-0001",
            "knowledge_space_id": "KB-SECURITY",
            "canonical_repository": "VictorKVS/KNOWLEDGE_CORE",
            "repository_commit_sha": COMMIT1,
            "route_snapshot_ref": "KROUTE-SECURITY-v1",
            "content_root": "security-knowledge/",
            "objects": (self.obj1, self.obj2),
            "product_ref": "SEC-PROD-0001",
            "domain_ref": "SECURITY",
        }
        args.update(overrides)
        return self.builder.build(**args)

    def test_builds_immutable_sorted_snapshot(self):
        snapshot = self.build(objects=(self.obj2, self.obj1))
        self.assertEqual(snapshot.repository_commit_sha, COMMIT1)
        self.assertEqual(snapshot.object_version_refs, (
            f"SEC-REQ-0001@v3#{D2}",
            f"SEC-SRC-0001@v1#{D1}",
        ))
        self.assertEqual(len(snapshot.snapshot_digest), 64)

    def test_repository_commit_change_changes_snapshot_digest(self):
        first = self.build(repository_commit_sha=COMMIT1)
        second = self.build(repository_commit_sha=COMMIT2)
        self.assertNotEqual(first.snapshot_digest, second.snapshot_digest)

    def test_object_digest_change_changes_snapshot_digest(self):
        first = self.build(objects=(self.obj1,))
        changed = SnapshotObjectRef("SEC-SRC-0001", "v1", D2, "KB-SECURITY")
        second = self.build(objects=(changed,))
        self.assertNotEqual(first.snapshot_digest, second.snapshot_digest)

    def test_branch_name_cannot_replace_commit_sha(self):
        with self.assertRaisesRegex(ValueError, "IMMUTABLE_REPOSITORY_COMMIT_REQUIRED"):
            self.build(repository_commit_sha="main")

    def test_repository_url_is_not_accepted_as_repository_identity(self):
        with self.assertRaisesRegex(ValueError, "INVALID_CANONICAL_REPOSITORY"):
            self.build(canonical_repository="https://github.com/VictorKVS/KNOWLEDGE_CORE")

    def test_parent_traversal_content_root_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "INVALID_KNOWLEDGE_CONTENT_ROOT"):
            self.build(content_root="../security-knowledge/")

    def test_cross_space_object_is_rejected(self):
        wrong = SnapshotObjectRef("OBJ-1", "v1", D1, "KB-OTHER")
        with self.assertRaisesRegex(ValueError, "KNOWLEDGE_SPACE_MISMATCH"):
            self.build(objects=(wrong,))

    def test_duplicate_object_version_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "DUPLICATE_KNOWLEDGE_OBJECT_VERSION"):
            self.build(objects=(self.obj1, self.obj1))

    def test_empty_snapshot_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "KNOWLEDGE_SNAPSHOT_OBJECTS_REQUIRED"):
            self.build(objects=())


if __name__ == "__main__":
    unittest.main()
