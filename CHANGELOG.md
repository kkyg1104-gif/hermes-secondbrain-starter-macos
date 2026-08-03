# Changelog

## 1.1.1

- Validate starter marker type, JSON shape, schema, version, and managed paths before trusting it.
- Reject malformed, foreign, directory, and symbolic-link markers even with `--allow-nonempty`.
- Write generated files and the starter marker atomically with `os.replace()`.
- Remove the stale duplicate Dashboard People Hub requirement from the manual bootstrap instructions.
- Add regression coverage for marker, symlink, path-boundary, and qmd inspection edge cases.

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