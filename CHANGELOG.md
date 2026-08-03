# Changelog

## 1.1.0

- Bundle the Python bootstrap during Hermes URL installs through an explicit support-file link.
- Add read-only `--check` validation and reject unmarked non-empty targets by default.
- Add `--allow-nonempty` for deliberate existing-directory setup.
- Back up managed files automatically before `--overwrite`.
- Add a starter marker for safe idempotent reruns and future upgrades.
- Remove the duplicate dashboard `People Hub.md` and use an explicit Obsidian path link.
- Back up and remove the obsolete v1.0 dashboard `People Hub.md` during explicit overwrite migration.
- Refuse symbolic links along managed paths so writes cannot escape the selected vault.
- Validate qmd collection names and verify existing collection paths.
- Fail qmd setup on collection/context/update/embed/status/list/search errors.
- Verify qmd retrieval for Agent Rules and Tag Registry before reporting success.

## 1.0.0

- Initial public starter with an empty vault skeleton, ontology, templates, Agent Rules, Tag Registry, and optional qmd setup.