# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `MUNICIPALITY` added to `Precision` enum

### Changed

- `observation.id_atlas_code` returns the ornitho id prefixed with `3_`

## [0.2.0] - 2020-11-24

### Added

- `notime` as parameter to observation creation
- `accuracy_of_location` to observation model
- `right` model (aka permission)
- `rights` to observer model

### Changed

- Example forms/create_and_delete: add `notime`; change `precision`
- Example observations/create_and_delete: add `notime`, `resting_habitat` and `observation_detail`

### Fixed

- Setter `visit_number` of the observation model
- Setter `sequence_number` of the observation model
- Setter `notime` of the observation model
- Raw data of `resting_habitat` when generating body for updating observations
- Raw data of `observation_detail` when generating body for when updating observations


## [0.1.0] - 2020-11-10

### Added

- Added taxonomic groups
- Added families
- Added species
- Added territorial units
- Added local admin units
- Added places
- Added observers
- Added entities
- Added protocol
- Added observations
- Added fields
- Added media
- Some basic examples

[unreleased]: https://github.com/dda-dev/ornitho-client-python/compare/v0.2.0...master
[0.2.0]: https://github.com/dda-dev/ornitho-client-python/releases/tag/v0.2.0
[0.1.0]: https://github.com/dda-dev/ornitho-client-python/releases/tag/v0.1.0