""" Veracode Community SCA json result parser """
import argparse
import json
import os
from typing import Dict, List

from junitparser import TestCase, TestSuite, JUnitXml, Failure

# Create the parser
arg_parser = argparse.ArgumentParser(prog="scaresultparser")

# Add the arguments
arg_parser.add_argument(
    "--target",
    "-t",
    metavar="target",
    type=str,
    required=True,
    help="The target tested",
)
arg_parser.add_argument(
    "--mincvss",
    "-c",
    metavar="mincvss",
    type=int,
    required=True,
    default=5,
    help="Minimum CVSS score to report on.",
)
arg_parser.add_argument(
    "--failbuild",
    "-f",
    metavar="failbuild",
    type=str,
    required=True,
    default="false",
    choices=["true", "false"],
    help="Fail the build (default is false).",
)


def parse_sca_json(data: Dict, min_cvss: int) -> List[Dict]:
    """Parse Veracode SCA output
    JSON schema: https://help.veracode.com/reader/hHHR3gv0wYc2WbCclECf_A/MRCzRYqmVX_PduRZ15UQyA"""

    results: List[Dict] = []

    if len(data["records"][0]["vulnerabilities"]) > 0:
        for vuln in data["records"][0]["vulnerabilities"]:
            # Check the minimum CVSS score to report on
            if min_cvss > vuln["cvssScore"]:
                pass
            else:
                # A vulnerability can have more than one library listed which is tracked x times.
                # ajv is an example where it is two different vulnerable versions (with the same
                # vulnerability) but two different modules in a project are using it.
                for library in vuln["libraries"]:
                    result_dict = create_result_dict()
                    result_dict["Vulnerability"] = vuln["title"]
                    result_dict["CVE"] = vuln["cve"]
                    result_dict["CVSS"] = vuln["cvssScore"]
                    result_dict["Language"] = vuln["language"]
                    for key, value in vuln["libraries"][0]["details"][0].items():
                        if key == "updateToVersion":
                            result_dict["Upgrade to Version"] = value

                    for ref, value in library["_links"].items():
                        # This gets the ref value
                        library = value.split("/")[4]
                        version = value.split("/")[6]
                        result_dict["Vulnerable Library"] = data["records"][0][
                            "libraries"
                        ][int(library)]["name"]
                        # Version is important because there could be more than one
                        # version installed/used in a project
                        result_dict["Version"] = data["records"][0]["libraries"][
                            int(library)
                        ]["versions"][int(version)]["version"]

                    results.append(result_dict)
                    result_dict = None

        # No vulnerabilities >= the min CVSS score
        if len(results) == 0:
            results.append(
                {"Results": f"No vulnerabilities >= the min CVSS score {min_cvss}."}
            )

    else:
        # No vulnerabilities to address
        results.append({"Results": "No vulnerabilities."})

    return results


def create_result_dict() -> Dict:
    """Create the results dictionary"""
    return {
        "Vulnerable Library": None,
        "Version": None,
        "Language": None,
        "Vulnerability": None,
        "CVE": None,
        "CVSS": None,
        "Upgrade to Version": None,
    }


def write_output(target: str, results: list, min_cvss: int) -> None:
    """Write scan results in junitxml format"""

    suite = TestSuite(f"{target}")

    no_vulns: List = [
        {"Results": "No vulnerabilities."},
        {"Results": f"No vulnerabilities >= the min CVSS score {min_cvss}."},
    ]

    for result in results:
        if result not in no_vulns:
            test_case = TestCase(result["Vulnerable Library"])
            test_case.name = (
                result["Vulnerable Library"]
                + " - "
                + result["Vulnerability"]
                + " - "
                + "CVSS "
                + str(result["CVSS"])
            )
            test_case.result = [Failure(result)]
        else:
            test_case = TestCase("No vulnerabilities")
            test_case.result = result

        suite.add_testcase(test_case)

    xml = JUnitXml()
    xml.add_testsuite(suite)
    xml.write("test-output.xml")


def main() -> None:

    """Main function"""
    # Execute the parse_args() method
    args = arg_parser.parse_args()
    target = args.target
    min_cvss = args.mincvss
    fail_build = args.failbuild

    # Open the Veracode SCA JSON results
    with open("scaresults.json", "r") as sca_results:
        data = json.load(sca_results)
    # Parse results
    results = parse_sca_json(data, min_cvss)

    # Generate test-output.xml
    write_output(target, results, min_cvss)

    # Remove scaresults.json file
    os.remove("scaresults.json")

    output = os.path.normpath(
        os.path.abspath(os.path.expanduser(os.path.expandvars("test-output.xml")))
    )

    # Borrowed from pytest-azurepipelines
    # https://github.com/tonybaloney/pytest-azurepipelines/blob/master/pytest_azurepipelines.py

    run_title = f"{target}"

    print(
        f"##vso[results.publish type=JUnit;runTitle={run_title};failTaskOnFailedTests={fail_build};]{output}"
    )


if __name__ == "__main__":

    main()
