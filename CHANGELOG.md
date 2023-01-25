# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `access` model added
- `access` property added to `site`
- `access` property added to `protocol`

### Changed

- override default repr

### Fixed

- if a `protocol` has no sites, an exception is no longer thrown when trying to access them

## [0.3.0] - 2022-03-10

### Added

- `MUNICIPALITY` added to `Precision` enum
- `requests-cache` added as optional dependency
- `excel_str_german` property added to `Detail`
- `guid` added as property to `Observation` and as argument with default generator (uuid4) to `create` method
- `export_date` added as optional argument to `Observation.create` method
- `wkt` added to `Form` model
- `RelationType` model added
- `relations` added to `Observation` model
- `direction` added to `Observation` model
- `centroid` added to `Place` model
- `order` added to `Place` model
- `wkt` added to `Place` model
- `local_name` added to `Site` model
- `id_reference_locality` added to `Site` model
- `id_protocol` added to `Site` model
- `transect_places` added to `Site` model
- `point_places` added to `Site` model
- `polygon_places` added to `Site` model
- `boundary_wkt` added to `Site` model
- `observers` added to `Site` model
- `place` added to `Site` model
- `created_by` added to `Place` model
- `created_date` added to `Place` model
- `last_updated_by` added to `Place` model
- `last_updated_date` added to `Place` model
- `diff` method added to `Place` model
- `id_waterbird_conditions` setter added to `Form` model
- `comment` setter added to `Form` model
- `protocol_headers` argument added to form creation method
- `BadGatewayException` added
- `retries` argument to requests methods added
- `potential_breeding_pairs` added to `Observation` model
- `ServiceUnavailableException` added

### Changed

- `observation.id_atlas_code` returns the ornitho id prefixed with `3_`
- `sites` can now be retrieved directly via api endpoint 
- raise `ObjectNotFoundException` instead of `APIException` if no object is retrieved
- `observation.diff` returns a dictionary containing the updated and deleted observations

### Fixed

- `observation.mark_as_exported`: subtract 2 seconds from default date

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

[unreleased]: https://github.com/dda-dev/ornitho-client-python/compare/v0.3.0...master
[0.3.0]: https://github.com/dda-dev/ornitho-client-python/releases/tag/v0.3.0
[0.2.0]: https://github.com/dda-dev/ornitho-client-python/releases/tag/v0.2.0
[0.1.0]: https://github.com/dda-dev/ornitho-client-python/releases/tag/v0.1.0