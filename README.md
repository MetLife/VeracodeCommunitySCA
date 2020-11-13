# Veracode Community Software Composition Analysis (SCA) Azure DevOps Extension

This project is community contributed and is not supported by Veracode. For a list of supported projects, please visit Veracode.com.

## Overview

Seamlessly integrate Veracode Agent-Based SCA scans with Azure DevOps build or release pipelines. Please note, the Agent-Based scan method is not the same thing as the "Upload and Scan" Method. You can find an overview of each method on Veracode's website [here](https://help.veracode.com/reader/9nOkCbEfhLEzMgzr2zCv5Q/8ogXM1j_wRm_AYmyKdrdoQ).

## Requirements

To run this plug-in in your build or release pipeline, you must be an existing Veracode SCA customer. Additionally, you need a valid SRCCLR_API_TOKEN to use this plug-in. Documentation for how to create a token for Continuous Integration (CI) activities can be found on Veracode's website [here](https://help.veracode.com/reader/hHHR3gv0wYc2WbCclECf_A/OdKcJQRbCpa6eUTX03z~Ag). There are no specific instructions for Azure DevOps; however, if you follow the directions for CircleCI you can successfully generate a SRCCLR_API_TOKEN to be used with this plug-in.

Currently, this plug-in will only run on a Linux or Mac Azure Pipelines agent (either hosted or self-hosted). Additionally, the agent requires Python > 3.6.

## Usage

There are five required inputs: SRCCLR_API_TOKEN, Scan type, Target to scan, Minimum CVSS score to report, and an option to fail the build.

* SRCCLR_API_TOKEN - Secure environment variable with your Veracode SCA token
* Scan type - Dropdown with three options: URL, Docker Image, or a path to the artifact(s)
* Target to scan - Specify the URL, docker image, or a path to the artifact(s) to scan
* Minimum CVSS score to report - Dropdown from 0-10 (Default is 5)
* Fail the build - Fail the build if any vulnerabilities are found (Default is no)

There are two optional inputs: Application Name, and Test Agent capabilities

* Application Name - Optional input used to better label test results
* Test agent capabilities - Optional boolean that will run "srcclr test" during task execution. Useful for troubleshooting environment issues.

## Setting and Securing SRCCLR_API_TOKEN

A high-level overview of setting secret values in YAML pipelines is [here](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/variables?view=azure-devops&tabs=yaml%2Cbatch#secret-variables). To set secret values in Classic pipelines, refer to the documentation [here](https://docs.microsoft.com/en-us/azure/devops/pipelines/process/variables?view=azure-devops&tabs=yaml%2Cbatch#secret-variables).

In either case, first create a variable in your build or release pipeline called SRCCLR_API_TOKEN, store the token in the field, and click on the lock icon to protect the token. Please note, once you protect the token, you can never retrieve the value again. Once you have created the SRCCLR_API_TOKEN variable, you have to populate it in the plug-in. Navigate to the "Environment Variables" section of the plug-in, create a variable called SRCCLR_API_TOKEN and, for value, input $(SRCCLR_API_TOKEN). 

## Testing

To test the json result parsing, test-output.xml creation and coverage, run:

```bash
cd tests
pytest -v test_parsescaresults.py --cov=../buildAndReleaseTask/. --cov-report=xml
```

## Known Issues and Limitations of the Microsoft hosted Azure Pipeline agent

If you intend to test a private endpoint (i.e., internal source code repository), it is probable that the Microsoft hosted agents do not have access to your internal network. As a result, please use a self-hosted Azure Pipeline agent. For self-hosted agents, Python >= 3.6.x is required. Please Note: Windows is currently not supported for the Veracode Community SCA Azure DevOps Extension.

Please refer to the links below for your target platform:

* [Linux](https://docs.microsoft.com/en-us/azure/devops/pipelines/agents/v2-linux?view=azure-devops)
* [MacOS](https://docs.microsoft.com/en-us/azure/devops/pipelines/agents/v2-osx?view=azure-devops)

The location of the latest self-hosted agents is [here](https://github.com/microsoft/azure-pipelines-agent)

## References

[Here](https://www.paraesthesia.com/archive/2020/02/25/tips-for-custom-azure-devops-build-tasks/) are some useful tips for developing tasks for Azure DevOps.

## Feedback

Send me mail at joe@metlife.com