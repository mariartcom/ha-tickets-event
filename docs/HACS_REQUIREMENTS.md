# HACS Requirements Checklist

Reference: https://www.hacs.xyz/docs/contribute/

## Repository Requirements

### Structure
- [ ] Repository must be public
- [ ] Repository must have a description
- [ ] Repository must have topics/tags including `home-assistant` and `hacs`
- [ ] Repository must have a README.md with:
  - [ ] Integration description
  - [ ] Installation instructions
  - [ ] Configuration guide
  - [ ] Screenshots/examples
  - [ ] Troubleshooting section

### Files
- [ ] `manifest.json` in custom_components/{domain}/
- [ ] `__init__.py` in custom_components/{domain}/
- [ ] `hacs.json` in repository root
- [ ] `README.md` in repository root
- [ ] `LICENSE` file (appropriate open source license)
- [ ] `.gitignore` file

### manifest.json Requirements
- [ ] `domain`: Unique domain name
- [ ] `name`: Integration name
- [ ] `documentation`: Link to documentation
- [ ] `issue_tracker`: Link to GitHub issues
- [ ] `version`: Semantic versioning
- [ ] `codeowners`: List of maintainers
- [ ] `requirements`: Python dependencies
- [ ] `dependencies`: HA dependencies
- [ ] `config_flow`: true (if configuration UI is provided)
- [ ] `iot_class`: Appropriate classification

### hacs.json Requirements
- [ ] `name`: Integration display name
- [ ] `render_readme`: true (optional)
- [ ] `domains`: List of domains (optional)

## Code Quality

### Python Standards
- [ ] Python 3.11+ compatibility
- [ ] Type hints on all functions
- [ ] Async/await patterns where appropriate
- [ ] Proper exception handling
- [ ] Follow Home Assistant code style
- [ ] Use Home Assistant helpers

### Integration Standards
- [ ] Use Config Flow for configuration
- [ ] Implement proper entity platforms (sensor, binary_sensor, etc.)
- [ ] Device registry integration (if applicable)
- [ ] Area registry support (if applicable)
- [ ] Translation files (strings.json)
- [ ] Services with proper schema validation
- [ ] Options flow for reconfiguration

### Testing
- [ ] Unit tests with pytest
- [ ] Test coverage > 80%
- [ ] Integration tests
- [ ] Fixtures for mocking API responses

## Documentation

### README.md Sections
- [ ] Overview/Description
- [ ] Features list
- [ ] Installation via HACS
- [ ] Manual installation (optional)
- [ ] Configuration steps
- [ ] Available entities
- [ ] Available services
- [ ] Example automations
- [ ] Lovelace card examples
- [ ] Screenshots
- [ ] Troubleshooting
- [ ] Contributing guidelines
- [ ] License information

### In-Code Documentation
- [ ] Docstrings for all classes
- [ ] Docstrings for all public methods
- [ ] Comment complex logic
- [ ] Service YAML descriptions

## Functionality

### Core Features
- [ ] Proper setup and teardown
- [ ] Configuration validation
- [ ] API error handling
- [ ] Rate limiting handling
- [ ] Network timeout handling
- [ ] Offline mode handling
- [ ] Data caching (if appropriate)
- [ ] Update coordinator pattern

### User Experience
- [ ] Clear error messages
- [ ] Configuration validation with helpful errors
- [ ] Persistent notifications for critical errors
- [ ] Debug logging for troubleshooting
- [ ] Sensible default values
- [ ] Translation support

## Entities

### Sensor Entities
- [ ] Proper device class
- [ ] Correct unit of measurement
- [ ] State class (if applicable)
- [ ] Icon or icon template
- [ ] Attributes with additional data
- [ ] Availability tracking

### Binary Sensor Entities
- [ ] Proper device class
- [ ] Icon or icon template
- [ ] Attributes with context

## Services

### Service Definitions
- [ ] services.yaml with descriptions
- [ ] Schema validation for service data
- [ ] Proper error handling
- [ ] Service response data (HA 2023.7+)

## Versioning

### Git Tags
- [ ] Use semantic versioning (vX.Y.Z)
- [ ] Create release for each version
- [ ] Include changelog in releases
- [ ] Properly formatted release notes

### Updates
- [ ] Version bump in manifest.json
- [ ] Update CHANGELOG.md
- [ ] Create git tag
- [ ] Create GitHub release

## Publishing to HACS

### Pre-submission
- [ ] Test with custom repository
- [ ] Verify all requirements met
- [ ] Clean commit history
- [ ] Update all documentation

### Submission Process
1. [ ] Fork HACS default repository
2. [ ] Add integration to appropriate category
3. [ ] Create pull request
4. [ ] Respond to review feedback
5. [ ] Await approval

### Post-approval
- [ ] Monitor issues
- [ ] Provide support
- [ ] Regular maintenance
- [ ] Security updates

## IoT Class Options
Choose the most appropriate:
- `cloud_polling`: Fetching data from cloud (likely for this integration)
- `cloud_push`: Cloud pushes data
- `local_polling`: Local device polling
- `local_push`: Local device pushes data
- `calculated`: Data is calculated

## License
Choose an open source license:
- MIT (recommended for simplicity)
- Apache 2.0
- GPL v3

## GitHub Repository Settings

### Topics/Tags to Add
- `home-assistant`
- `hacs`
- `homeassistant`
- `custom-component`
- `events`
- `attractions`
- `tickets`

### Branch Protection
- [ ] Protect main/master branch
- [ ] Require review before merge
- [ ] Require status checks

### Issues
- [ ] Enable issues
- [ ] Create issue templates
- [ ] Add labels

### Discussions (Optional)
- [ ] Enable discussions for Q&A
