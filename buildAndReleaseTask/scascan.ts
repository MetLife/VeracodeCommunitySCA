/* tslint:disable:linebreak-style no-unsafe-any no-submodule-imports no-relative-imports no-console */
/**
 * Veracode Community SCA Azure DevOps Extension
 *
 */

import * as tl from 'azure-pipelines-task-lib/task';
import * as trm from 'azure-pipelines-task-lib/toolrunner';
import * as path from 'path';

async function run(): Promise<void> {
    try {
        tl.setResourcePath(path.join(__dirname, 'task.json'));

        // Get task inputs
        const scanType: string = <string>tl.getInput('scanType', true);
        const scanTarget: string = <string>tl.getInput('scanTarget', true);
        const testAgent: boolean = <boolean>tl.getBoolInput('testAgent', true);
        const minCVSS: string = <string>tl.getInput('minCVSS', true);
        const failBuild: boolean = <boolean>tl.getBoolInput('failBuild', true);
        let appName: string | undefined = <string>tl.getInput('appName');

        // Get SRCCLR_API_TOKEN environmental variable
        const SRCCLR_API_TOKEN: string = <string>tl.getVariable('SRCCLR_API_TOKEN');
        if (SRCCLR_API_TOKEN === '' || SRCCLR_API_TOKEN === undefined) {
            throw new Error('You must define the SRCCLR_API_TOKEN environmental variable.');
        }

        // Set appName to the project name if it was left blank
        if (appName === '' || appName === undefined) {
            appName = tl.getVariable('System.TeamProject');
        }

        console.log('Scan Type: ' + `${scanType} selected`);
        console.log('Scan Target: ' + `${scanTarget}`);
        console.log('Minimum CVSS Score: ' + `${minCVSS} selected`);
        console.log('Fail build? ' + `${failBuild}`);

        // Set the scope of the scan if defined
        const scanScope: string = <string>tl.getVariable('SRCCLR_NPM_SCOPE');
        if (scanScope !== undefined) {
            console.log('Scan scope: ' + `${scanScope}`);
        }

        // Get the agent platform
        const agentPlatform: string = process.platform;
        console.log('Agent platform: ' + `${agentPlatform}`);

        //This only works on linux or MacOs Agents
        if (agentPlatform === 'linux' || agentPlatform === 'darwin') {

            try {
                // Is srcclr already installed?
                const srcclrPath: string = tl.which('srcclr', true);
                console.log('Found SCA Agent install here: ' + `${srcclrPath}`);

            } catch {
                // Install srcclr
                const curlPath: string = tl.which('curl', true);
                const shPath: string = tl.which('sh', true);

                // Install SCA Agent
                const curl: trm.ToolRunner = tl.tool(curlPath);
                curl.arg('-sSL');
                curl.arg('https://www.sourceclear.com/install');
                const sh: trm.ToolRunner = tl.tool(shPath);
                // On self-hosted agents this may not work if the agent is not running as root
                const pipe: trm.ToolRunner = curl.pipeExecOutputToTool(sh);
                const scaAgentInstall: number = await pipe.exec();
                tl.setResult(tl.TaskResult.Succeeded, tl.loc('curlReturnCode', scaAgentInstall));

            }

            // Test the environment to see which collectors are available, equivalent to 'srcclr test'
            if (testAgent === true) {
                const scaAgentTest: trm.ToolRunner = tl.tool('srcclr');
                scaAgentTest.arg('test');
                const scaAgentTestResult: number = await scaAgentTest.exec();
                tl.setResult(tl.TaskResult.Succeeded, tl.loc('bashReturnCode', scaAgentTestResult));
            }

            // Scan against an artifact directory
            if (scanType === 'directory') {
                const scanDirectory: trm.ToolRunner = tl.tool('srcclr');
                scanDirectory.arg('scan');
                scanDirectory.arg(`${scanTarget}`);
                scanDirectory.arg('--json');
                scanDirectory.arg('scaresults.json');
                const directoryResults: number = await scanDirectory.exec();
                tl.setResult(tl.TaskResult.Succeeded, tl.loc('bashReturnCode', directoryResults));
            // Scan against a URL - Need to make sure it begins with http(s)
            } else if (scanType === 'url') {
                const scanUrl: trm.ToolRunner = tl.tool('srcclr');
                scanUrl.arg('scan');
                scanUrl.arg('--url');
                scanUrl.arg(`${scanTarget}`);
                scanUrl.arg('--json');
                scanUrl.arg('scaresults.json');
                const urlResults: number = await scanUrl.exec();
                tl.setResult(tl.TaskResult.Succeeded, tl.loc('bashReturnCode', urlResults));
            // Scan a Docker image
            } else if (scanType === 'image') {
                const scanDockerImage: trm.ToolRunner = tl.tool('srcclr');
                scanDockerImage.arg('scan');
                scanDockerImage.arg('--image');
                scanDockerImage.arg(`${scanTarget}`);
                scanDockerImage.arg('--json');
                scanDockerImage.arg('scaresults.json');
                const dockerResults: number = await scanDockerImage.exec();
                tl. setResult(tl.TaskResult.Succeeded, tl.loc('bashReturnCode', dockerResults));
            }

            // Need error handling when selecting python for non Microsoft hosted agents
            // Install junitparser
            const pythonPath: string = tl.which('python3');
            const python3: trm.ToolRunner = tl.tool(pythonPath);
            python3.arg('-m');
            python3.arg('pip');
            python3.arg('install');
            python3.arg('--upgrade');
            python3.arg('junitparser');
            const pipinstall: number = await python3.exec();
            tl.setResult(tl.TaskResult.Succeeded, tl.loc('pipReturnCode', pipinstall));

            // Generate the results
            const genResults: trm.ToolRunner = tl.tool(pythonPath);
            genResults.arg(path.join(__dirname, 'parsescaresults.py'));
            genResults.arg('--target');
            genResults.arg(`${appName}`);
            genResults.arg('--mincvss');
            genResults.arg(`${minCVSS}`);
            genResults.arg('--failbuild');
            genResults.arg(`${failBuild}`);
            const publishResults: number = await genResults.exec();
            tl.setResult(tl.TaskResult.Succeeded, tl.loc('bashReturnCode', publishResults));

            return;

        } else {
            // Need to add Windows support
            throw new Error('This task does not work on windows(yet).');

        }

    } catch (err) {

        tl.setResult(tl.TaskResult.Failed, err.message);

        return;
    }
}

run();
