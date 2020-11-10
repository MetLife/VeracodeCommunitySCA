""" Tests to ensure vulnerabilitiy results are parsed properly """
import json

from buildAndReleaseTask.parsescaresults import parse_sca_json, write_output
from junitparser import JUnitXml


def test_parse_javascript_results():
    """ Test parsing a fork of the srcclr/example-javascript repo
    To generate results:
    srcclr scan --url https://github.com/gattjoe/example-javascript --json example-javascript.json
    """
    # Open the Veracode SCA JSON results
    with open("example-javascript.json", "r") as sca_results:
        data = json.load(sca_results)

    # Include all CVSS in the output
    parsed_data = parse_sca_json(data, 0)

    # As of srcclr 3.7.1 there are 75 detected vulns in this example
    assert len(parsed_data) == 75

    flaw_counter = 0
    for flaw in parsed_data:
        if flaw["CVSS"] >= 5:
            flaw_counter += 1

    # As of srcclr 3.7.1 there are 59 CVSS >= 5 vulnerabilities in this example
    assert flaw_counter == 59

    actual_high_vulns = []
    expected_high_vulns = ["console-io", "ms", "moment", "sequelize", "sequelize",
                           "lodash", "send"]

    for flaw in parsed_data:
        if flaw["CVSS"] >= 7.5:
            actual_high_vulns.append(flaw["Vulnerable Library"])

    # As of srcclr 3.7.1 there are 7 CVSS >= 7.5 vulnerabilities in this example
    assert expected_high_vulns.sort() == actual_high_vulns.sort()


def test_parse_dotnet_results():
    """ Test parsing a fork of the srcclr/example-dotnet repo
    To generate results:
    srcclr scan --url https://github.com/gattjoe/example-dotnet --json example-dotnet.json """

    # Open the Veracode SCA JSON results
    with open("example-dotnet.json", "r") as sca_results:
        data = json.load(sca_results)

    # Include all CVSS in the output
    parsed_data = parse_sca_json(data, 0)

    # As of srcclr 3.7.1 there are 15 detected vulns in this example
    assert len(parsed_data) == 15

    flaw_counter = 0
    for flaw in parsed_data:
        if flaw["CVSS"] >= 5:
            flaw_counter += 1

    # As of srcclr 3.7.1 there are 11 CVSS >= 5 vulnerabilities in this example
    assert flaw_counter == 11

    actual_high_vulns = []
    expected_high_vulns = ["log4net", "GSF.Core", "GSF.Security",
                           "recurly-api-client", "recurly-api-client"]

    for flaw in parsed_data:
        if flaw["CVSS"] >= 7.5:
            actual_high_vulns.append(flaw["Vulnerable Library"])

    # As of srcclr 3.7.1 there are 5 CVSS >= 7.5 vulnerabilities in this example
    assert expected_high_vulns.sort() == actual_high_vulns.sort()


def test_parse_ruby_results():
    """ Test parsing a fork of the srcclr/example-ruby repo
    To generate results:
    srcclr scan --url https://github.com/gattjoe/example-ruby --json example-ruby.json """

    # Open the Veracode SCA JSON results
    with open("example-ruby.json", "r") as sca_results:
        data = json.load(sca_results)

    # Include all CVSS in the output
    parsed_data = parse_sca_json(data, 0)

    # As of srcclr 3.7.1 there are 80 detected vulns in this example
    assert len(parsed_data) == 80

    flaw_counter = 0
    for flaw in parsed_data:
        if flaw["CVSS"] >= 5:
            flaw_counter += 1

    # As of srcclr 3.7.1 there are 58 CVSS >= 5 vulnerabilities in this example
    assert flaw_counter == 58

    actual_high_vulns = []
    expected_high_vulns = ["nokogiri", "nokogiri", "nokogiri", "nokogiri", "nokogiri", "nokogiri",
                           "actionpack", "actionview", "devise", "paperclip", "festivaltts4r"
                           "lingq"]

    for flaw in parsed_data:
        if flaw["CVSS"] >= 7.5:
            actual_high_vulns.append(flaw["Vulnerable Library"])

    # As of srcclr 3.7.1 there are 12 CVSS >= 7.5 vulnerabilities in this example
    assert expected_high_vulns.sort() == actual_high_vulns.sort()


def test_parse_jsnpm_results():
    """ Test parsing a fork of the srcclr/test-js-npm repo
    To generate results:
    srcclr scan --url https://github.com/gattjoe/test-js-npm --json example-jsnpm.json """

    # Open the Veracode SCA JSON results
    with open("example-jsnpm.json", "r") as sca_results:
        data = json.load(sca_results)

    # Include all CVSS in the output
    parsed_data = parse_sca_json(data, 0)

    # As of srcclr 3.7.1 there are 35 detected vulns in this example
    assert len(parsed_data) == 35

    flaw_counter = 0
    for flaw in parsed_data:
        if flaw["CVSS"] >= 5:
            flaw_counter += 1

    # As of srcclr 3.7.1 there are 31 CVSS >= 5 vulnerabilities in this example
    assert flaw_counter == 31

    actual_high_vulns = []
    expected_high_vulns = ["semver", "ms", "uglify-js", "semver", "ms", "lodash",
                           "lodash", "morgan", "extend", "lodash"]

    for flaw in parsed_data:
        if flaw["CVSS"] >= 7.5:
            actual_high_vulns.append(flaw["Vulnerable Library"])

    # As of srcclr 3.7.1 there are 10 CVSS >= 7.5 vulnerabilities in this example
    assert expected_high_vulns.sort() == actual_high_vulns.sort()


def test_parse_python_results():
    """ Test parsing a fork of the srcclr/example-python repo
    To generate results:
    srcclr scan --url https://github.com/gattjoe/example-python3-pip --json example-python.json """

    # Open the Veracode SCA JSON results
    with open("example-python.json", "r") as sca_results:
        data = json.load(sca_results)

    # Include all CVSS in the output
    parsed_data = parse_sca_json(data, 0)

    # As of srcclr 3.7.1 there are 41 detected vulns in this example
    assert len(parsed_data) == 41

    flaw_counter = 0
    for flaw in parsed_data:
        if flaw["CVSS"] >= 5:
            flaw_counter += 1

    # As of srcclr 3.7.1 there are 27 CVSS >= 5 vulnerabilities in this example
    assert flaw_counter == 27

    actual_high_vulns = []
    expected_high_vulns = ["PyJWT", "PyJWT", "Django", "pycrypto", "Django"]

    for flaw in parsed_data:
        if flaw["CVSS"] >= 7.5:
            actual_high_vulns.append(flaw["Vulnerable Library"])

    # As of srcclr 3.7.1 there are 5 CVSS >= 7.5 vulnerabilities in this example
    assert expected_high_vulns.sort() == actual_high_vulns.sort()


def test_write_results_no_vulns():
    """ Test parsing results and writing test-output.xml """

    # Open the Veracode SCA JSON results
    with open("example-novulns.json", "r") as sca_results:
        data = json.load(sca_results)

    # Include all CVSS in the output
    parsed_data = parse_sca_json(data, 0)

    # Create the test-output.xml
    write_output("No vulns", parsed_data)

    # Get test-output.xml
    xml = JUnitXml.fromfile('test-output.xml')

    # Assert there are no vulnerabilities in the output
    for suite in xml:
        for case in suite:
            assert case.name == 'No vulnerabilities'


def test_write_results_vulns():
    """ Test parsing results and writing test-output.xml """

    # Open the Veracode SCA JSON results
    with open("example-dotnet.json", "r") as sca_results:
        data = json.load(sca_results)

    # Include all CVSS in the output
    parsed_data = parse_sca_json(data, 0)

    # Create the test-output.xml
    write_output("dotnet vulns", parsed_data)

    # Get test-output.xml
    xml = JUnitXml.fromfile('test-output.xml')

    # Assert there are 15 vulnerabilities in the output
    case_counter = 0

    for suite in xml:
        for case in suite:
            case_counter += 1

    assert case_counter == 15

    # Assert there are 15 failures reported in the Test Suite
    assert xml.failures == 15


def test_multi_instance_of_vuln():
    """ Test parsing of results that have multiple instances
     of a vulnerability but in two or more different libraries """
    
    # Open the Veracode SCA JSON results
    with open("example-dotnet.json", "r") as sca_results:
        data = json.load(sca_results)

    # Include all CVSS in the output
    parsed_data = parse_sca_json(data, 0)

    actual_dupe_vulns = []

    # SQL Injection vulnerability is in both of these libraries
    expected_dupe_vulns = ["GSF.Core", "GSF.Security"]

    for flaw in parsed_data:
        if flaw["Vulnerable Library"] in expected_dupe_vulns:
            actual_dupe_vulns.append(flaw["Vulnerable Library"])

    assert expected_dupe_vulns.sort() == actual_dupe_vulns.sort()
