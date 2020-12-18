# Changelog for VeracodeCommunitySCA

# v1.0.0
- Initial Release

# v1.1.0
- Removed scanner installation functionality. We now run the SRCCLR CI script from https://download.sourceclear.com/ci.sh. This will ensure we are always running the latest version of the SRCCLR scanner when using a local Azure DevOps Agent and will preclude us from needing root permissions to install the scanner.
- Added the --recursive directive so that url and directory scans provide better coverage when applications use multiple package managers.
- Set the CACHE_DIR to Agent.TempDirectory. CACHE_DIR is a feature for SCA to direct where the SCA scanner is downloaded to. The Agent.TempDirectory is cleaned out after every job, which is useful for users leveraging a local Azure DevOps agent and disk space fills up (default was /tmp).
- Improved error handling for python tasks.