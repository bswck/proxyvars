# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/).<br/>
This project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->

## [v0.9.2](https://github.com/bswck/proxyvars/tree/v0.9.2) (2024-02-16)


### Fixed

- Set supported Python version range to `>=3.8,<3.13` instead of `>=3.8,<=3.12` that semantically disallows `3.12` PATCH releases. ([#11](https://github.com/bswck/proxyvars/issues/11))


## [v0.9.1](https://github.com/bswck/proxyvars/tree/v0.9.1) (2023-12-22)


### Changed

- Upgraded the skeleton version.

### Fixed

- A bug when `__doc__` inside proxy is `None` but regardless attempted to be %-formatted.
