# Veracode Community Software Composition Analysis (SCA) Azure DevOps Extenstion.

## Overview

Seamlessly integrate Veracode Agent Based SCA scans in either a classic or yaml based build or release pipeline. 

## Testing

To test the json result parsing, test-output.xml creation and coverage, run:

```bash
cd tests
pytest -v test_parsescaresults.py --cov=../buildAndReleaseTask/. --cov-report=xml
```

## Known Issues and Limitations of the Microsoft hosted Azure Pipeline agent

If you intend to test a private endpoint (i.e., internal source code repository), it is probable that the Microsoft hosted agents do not have access to your internal network. As a result, please use a self-hosted Azure Pipeline agent. For self-hosted agents, Python >= 3.7.x is required. Please Note: Windows is currently not supported for the Veracode Community SCA Azure DevOps Extension.

Please refer to the links below for your target platform:

* [Linux](https://docs.microsoft.com/en-us/azure/devops/pipelines/agents/v2-linux?view=azure-devops)
* [MacOS](https://docs.microsoft.com/en-us/azure/devops/pipelines/agents/v2-osx?view=azure-devops)

The location of the latest self-hosted agents is [here](https://github.com/microsoft/azure-pipelines-agent)

## References

[Here](https://www.paraesthesia.com/archive/2020/02/25/tips-for-custom-azure-devops-build-tasks/) are some useful tips for developing tasks for Azure DevOps.

## Feedback

Send me mail at joe@metlife.com