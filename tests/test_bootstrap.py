from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Dict, Optional

REPO = Path(__file__).resolve().parents[1]
INSTALLER = REPO / "install.sh"


class BootstrapTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_install(self, vault: Path, *args: str, env: Optional[Dict[str, str]] = None) -> subprocess.CompletedProcess[str]:
        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)
        return subprocess.run(
            ["bash", str(INSTALLER), "--vault", str(vault), "--year", "2031", *args],
            cwd=REPO,
            env=merged_env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

    def make_fake_qmd(self, scenario: str, expected_vault: Path) -> dict[str, str]:
        fakebin = self.root / f"fakebin-{scenario}"
        fakebin.mkdir()
        qmd = fakebin / "qmd"
        qmd.write_text(
            """#!/bin/sh
set -u
printf '%s\\n' \"$*\" >> \"$QMD_LOG\"
command_name=\"${1-} ${2-}\"
case \"$command_name\" in
  'collection show')
    case \"$QMD_SCENARIO\" in
      same-path) printf 'Collection: %s\\n  Path:     %s\\n' \"$3\" \"$EXPECTED_VAULT\"; exit 0 ;;
      collision) printf 'Collection: %s\\n  Path:     /different/private/vault\\n' \"$3\"; exit 0 ;;
      show-error) echo 'database unavailable'; exit 2 ;;
      *) echo \"Collection not found: $3\"; exit 1 ;;
    esac ;;
  'collection add')
    [ \"$QMD_SCENARIO\" = 'add-failure' ] && { echo 'simulated add failure'; exit 9; }
    exit 0 ;;
  'search My SecondBrain Agent Rules') printf 'qmd://my-secondbrain/90_System/Agent Rules.md\\n'; exit 0 ;;
  'search Tag Registry')
    [ \"$QMD_SCENARIO\" = 'search-empty' ] && { echo 'No results found.'; exit 0; }
    printf 'qmd://my-secondbrain/90_System/Ontology/Tag Registry.md\\n'; exit 0 ;;
  *) exit 0 ;;
esac
""",
            encoding="utf-8",
        )
        qmd.chmod(0o755)
        return {
            "PATH": f"{fakebin}{os.pathsep}{os.environ.get('PATH', '')}",
            "QMD_SCENARIO": scenario,
            "EXPECTED_VAULT": str(expected_vault.resolve()),
            "QMD_LOG": str(self.root / f"qmd-{scenario}.log"),
        }

    def test_check_only_does_not_create_vault(self) -> None:
        vault = self.root / "check-vault"
        result = self.run_install(vault, "--check")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("CHECK_ONLY=true", result.stdout)
        self.assertFalse(vault.exists())

    def test_github_bundle_mirrors_canonical_files(self) -> None:
        bundle = REPO / "skills/personal-secondbrain-llm-wiki"
        self.assertEqual((REPO / "SKILL.md").read_bytes(), (bundle / "SKILL.md").read_bytes())
        self.assertEqual(
            (REPO / "scripts/bootstrap_personal_secondbrain.py").read_bytes(),
            (bundle / "scripts/bootstrap_personal_secondbrain.py").read_bytes(),
        )

    def test_fresh_install_and_idempotent_rerun(self) -> None:
        vault = self.root / "vault with spaces"
        first = self.run_install(vault)
        second = self.run_install(vault)
        self.assertEqual(first.returncode, 0, first.stdout)
        self.assertEqual(second.returncode, 0, second.stdout)
        self.assertIn("FILES_WRITTEN=21", first.stdout)
        self.assertIn("FILES_WRITTEN=0", second.stdout)
        self.assertIn("FILES_EXISTING_SKIPPED=21", second.stdout)
        self.assertTrue((vault / "90_System/.personal-secondbrain-starter.json").is_file())
        marker = json.loads((vault / "90_System/.personal-secondbrain-starter.json").read_text())
        self.assertEqual(marker["starter_version"], "1.1.0")
        self.assertEqual(len(list(vault.rglob("People Hub.md"))), 1)
        home = (vault / "10_Dashboard/Home.md").read_text()
        self.assertIn("[[30_Knowledge/People/People Hub|People Hub]]", home)

    def test_nonempty_unmarked_target_is_rejected_without_mutation(self) -> None:
        vault = self.root / "existing"
        vault.mkdir()
        original = vault / "existing.md"
        original.write_text("KEEP_ME\n")
        result = self.run_install(vault)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("Vault is not empty", result.stdout)
        self.assertEqual(original.read_text(), "KEEP_ME\n")
        self.assertEqual(list(vault.iterdir()), [original])

    def test_allow_nonempty_is_explicit(self) -> None:
        vault = self.root / "existing-allowed"
        vault.mkdir()
        (vault / "existing.md").write_text("KEEP_ME\n")
        result = self.run_install(vault, "--allow-nonempty")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual((vault / "existing.md").read_text(), "KEEP_ME\n")
        self.assertTrue((vault / "90_System/Agent Rules.md").is_file())

    def test_overwrite_creates_backup(self) -> None:
        vault = self.root / "overwrite"
        self.assertEqual(self.run_install(vault).returncode, 0)
        rules = vault / "90_System/Agent Rules.md"
        rules.write_text("CUSTOM RULES\n")
        result = self.run_install(vault, "--overwrite")
        self.assertEqual(result.returncode, 0, result.stdout)
        backup_line = next(line for line in result.stdout.splitlines() if line.startswith("BACKUP_DIR="))
        backup = Path(backup_line.split("=", 1)[1])
        self.assertEqual((backup / "90_System/Agent Rules.md").read_text(), "CUSTOM RULES\n")
        self.assertNotEqual(rules.read_text(), "CUSTOM RULES\n")

    def test_v1_0_duplicate_people_hub_is_backed_up_and_removed(self) -> None:
        vault = self.root / "legacy"
        legacy = vault / "10_Dashboard/People Hub.md"
        legacy.parent.mkdir(parents=True)
        legacy.write_text("LEGACY CUSTOM PEOPLE\n")
        result = self.run_install(vault, "--allow-nonempty", "--overwrite")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("LEGACY_FILES_REMOVED=1", result.stdout)
        backup_line = next(line for line in result.stdout.splitlines() if line.startswith("BACKUP_DIR="))
        backup = Path(backup_line.split("=", 1)[1])
        self.assertEqual((backup / "10_Dashboard/People Hub.md").read_text(), "LEGACY CUSTOM PEOPLE\n")
        self.assertFalse(legacy.exists())
        self.assertTrue((vault / "30_Knowledge/People/People Hub.md").is_file())

    def test_managed_symlink_is_rejected_before_write(self) -> None:
        vault = self.root / "symlink-vault"
        outside = self.root / "outside"
        vault.mkdir()
        outside.mkdir()
        (vault / "90_System").symlink_to(outside, target_is_directory=True)
        result = self.run_install(vault, "--allow-nonempty", "--overwrite")
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("symbolic link", result.stdout)
        self.assertEqual(list(outside.iterdir()), [])

    def test_qmd_new_collection_and_searches_succeed(self) -> None:
        vault = self.root / "qmd-success"
        env = self.make_fake_qmd("success", vault)
        result = self.run_install(vault, "--setup-qmd", env=env)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("QMD_SETUP_SUCCESS=true", result.stdout)
        calls = Path(env["QMD_LOG"]).read_text()
        self.assertIn("collection add", calls)
        self.assertIn("search My SecondBrain Agent Rules", calls)
        self.assertIn("search Tag Registry", calls)

    def test_qmd_existing_collection_same_path_is_idempotent(self) -> None:
        vault = self.root / "qmd-same"
        env = self.make_fake_qmd("same-path", vault)
        result = self.run_install(vault, "--setup-qmd", env=env)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("QMD_COLLECTION_PATH_VERIFIED=", result.stdout)
        self.assertNotIn("collection add", Path(env["QMD_LOG"]).read_text())

    def test_qmd_collection_collision_fails_closed(self) -> None:
        vault = self.root / "qmd-collision"
        env = self.make_fake_qmd("collision", vault)
        result = self.run_install(vault, "--setup-qmd", env=env)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("QMD_SETUP_SUCCESS=false", result.stdout)
        self.assertIn("points to /different/private/vault", result.stdout)

    def test_qmd_collection_add_failure_is_not_reported_as_success(self) -> None:
        vault = self.root / "qmd-add-failure"
        env = self.make_fake_qmd("add-failure", vault)
        result = self.run_install(vault, "--setup-qmd", env=env)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("QMD_SETUP_SUCCESS=false", result.stdout)
        self.assertIn("collection registration failed", result.stdout)

    def test_qmd_ambiguous_collection_inspection_failure_fails_closed(self) -> None:
        vault = self.root / "qmd-show-error"
        env = self.make_fake_qmd("show-error", vault)
        result = self.run_install(vault, "--setup-qmd", env=env)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("QMD_SETUP_SUCCESS=false", result.stdout)
        self.assertIn("collection inspection failed", result.stdout)
        self.assertNotIn("collection add", Path(env["QMD_LOG"]).read_text())

    def test_qmd_empty_verification_search_fails(self) -> None:
        vault = self.root / "qmd-search-empty"
        env = self.make_fake_qmd("search-empty", vault)
        result = self.run_install(vault, "--setup-qmd", env=env)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("QMD_SETUP_SUCCESS=false", result.stdout)
        self.assertIn("verification search failed for: Tag Registry", result.stdout)


if __name__ == "__main__":
    unittest.main()
