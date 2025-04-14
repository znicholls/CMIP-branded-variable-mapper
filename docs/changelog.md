# Changelog

Versions follow [Semantic Versioning](https://semver.org/) (`<major>.<minor>.<patch>`).

Backward incompatible (breaking) changes will only be introduced in major versions
with advance notice in the **Deprecations** section of releases.

<!--
You should *NOT* be adding new changelog entries to this file,
this file is managed by towncrier.
See `changelog/README.md`.

You *may* edit previous changelogs to fix problems like typo corrections or such.
To add a new changelog entry, please see
`changelog/README.md`
and https://pip.pypa.io/en/latest/development/contributing/#news-entries,
noting that we use the `changelog` directory instead of news,
markdown instead of restructured text and use slightly different categories
from the examples given in that link.
-->

<!-- towncrier release notes start -->

## CMIP Branded Variable Mapper v0.3.0 (2025-03-18)

### :warning: Breaking Changes

- - Renamed `cmip_branded_variable_mapper` to `map_to_cmip_branded_variable`
  - Changed the `dimensions` argument to be `tuple[str, ...]` rather than `str` (to remove handling of whitespace and string searching)

  ([#9](https://github.com/znicholls/CMIP-branded-variables-mapper/pull/9))

### :tada: Improvements

- Updated the mapping to be able to reproduce the expected translation for the old variable names ([#8](https://github.com/znicholls/CMIP-branded-variables-mapper/pull/8))

### :books: Improved Documentation

- Added documentation that shows how to use the API ([#10](https://github.com/znicholls/CMIP-branded-variables-mapper/pull/10))


## CMIP Branded Variable Mapper v0.2.0 (2025-03-10)

### 🆕 Features

- Added basic functionality. Mapping for almost all varaibles is now supported. The failing cases are ones with basin in their dimensions. ([#6](https://github.com/znicholls/CMIP-branded-variables-mapper/pull/6))

### 🔧 Trivial/Internal Changes

- [#3](https://github.com/znicholls/CMIP-branded-variables-mapper/pull/3)


## CMIP Branded Variable Mapper v0.1.1 (2025-03-03)

### 🔧 Trivial/Internal Changes

- [#2](https://github.com/znicholls/CMIP-branded-variables-scratch/pull/2)


## CMIP Branded Variable Mapper v0.1.0 (2025-03-03)

### 🔧 Trivial/Internal Changes

- [#1](https://github.com/znicholls/CMIP-branded-variables-scratch/pull/1)
