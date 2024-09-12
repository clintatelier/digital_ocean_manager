# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2023-05-28

### Added
- Comprehensive error handling and logging
  - All scripts now include robust error handling
  - Detailed logging for setup process (setup.log) and resource monitoring (resource_monitoring.log)
- Resource cleanup mechanism
  - Option to clean up created resources in case of setup failure
- Dry run mode
  - Allows users to see what actions would be taken without actually creating or modifying resources
- Step-by-step execution with confirmation
  - Setup process now proceeds step-by-step, asking for confirmation before each major action
- Resource usage monitoring
  - New script (scripts/monitor_resources.py) for continuous monitoring of CPU, memory, and disk usage
  - Logs information and provides warnings if usage exceeds specified thresholds

### Changed
- Updated README.md with information about new features and improvements
- Enhanced setup process to include new features like dry run mode and step-by-step confirmation

### Fixed
- Improved error handling to prevent orphaned resources in DigitalOcean account

## [1.0.0] - 2023-05-01

### Added
- Initial release of DigitalOcean Manager
- Automated setup for managing multiple web applications and static sites on a single DigitalOcean droplet
- Deployment scripts for web apps and static sites
- Project management functionality
- DigitalOcean credentials management
- VS Code integration guide
- Comprehensive deployment information generation
- Configuration management for different environments