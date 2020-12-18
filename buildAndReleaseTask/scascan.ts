/* tslint:disable:linebreak-style no-unsafe-any no-submodule-imports no-relative-imports no-console */
/**
 * Veracode Community SCA Azure DevOps Extension
 *
 */

import * as tl from 'azure-pipelines-task-lib/task';
import * as trm from 'azure-pipelines-task-lib/toolrunner';
import * as path from 'path';

/**
 * Get Agent.TempDirectory which is a temp folder that is cleaned after each pipeline job.
 * This is where we will store the Veracode SCA tool so we do not take up too much disk space
 * on self hosted agents.
 */
const tempPath: string = <string>tl.getVariable('Agent.TempDirectory');
if (tempPath !== undefined) {
    // Per https://help.veracode.com/r/c_sc_ci_script if we set
    // the CACHE_DIR variable, we can direct where the files are downloaded to
    const cacheDir = tl.setVariable('CACHE_DIR', tempPath);
    console.log(`CACHE_DIR: ${cacheDir}`)
}


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
   
            // Test the environment to see which collectors are available, equivalent to 'srcclr test'
            if (testAgent === true) {
                await testSCA();
            }
            
            // Run the scan
            await runScan(scanType, scanTarget);

            // Find the python3 installation
            const pythonPath: string = tl.which('python3');

            try {
                // Install junitparser
                const python3: trm.ToolRunner = tl.tool(pythonPath);
                python3.arg('-m');
                python3.arg('pip');
                python3.arg('install');
                python3.arg('--upgrade');
                python3.arg('pip');
                python3.arg('junitparser');
                // Run the command
                await python3.exec();
                tl.setResult(tl.TaskResult.Succeeded, "pip install was successful.");

            } catch(err) {

                return tl.setResult(tl.TaskResult.Failed, "pip install failed.");
            }

            try {
                // Generate the results
                const genResults: trm.ToolRunner = tl.tool(pythonPath);
                genResults.arg(path.join(__dirname, 'parsescaresults.py'));
                genResults.arg('--target');
                genResults.arg(`${appName}`);
                genResults.arg('--mincvss');
                genResults.arg(`${minCVSS}`);
                genResults.arg('--failbuild');
                genResults.arg(`${failBuild}`);
                // Run the command
                await genResults.exec();
                return tl.setResult(tl.TaskResult.Succeeded, "SCA result parsing and upload was successful.");

            } catch(err) {

                return tl.setResult(tl.TaskResult.Failed, "SCA result parsing and upload failed.");
            }

        } else {
            // Need to add Windows support
            throw new Error('This task does not work on windows(yet).');

        }

    } catch (err) {

        tl.setResult(tl.TaskResult.Failed, err.message);

        return;
    }
}

// Run the SCA scan
async function runScan(scanType: string,
                       scanTarget: string): Promise<void> {

    try {
        const curlPath: string = tl.which('curl', true);
        const shPath: string = tl.which('sh', true);
        const curl: trm.ToolRunner = tl.tool(curlPath);
        curl.arg('-sSL');
        curl.arg('https://download.sourceclear.com/ci.sh');
        const sh: trm.ToolRunner = tl.tool(shPath);
        sh.arg('-s');
        sh.arg('--');
        sh.arg('scan');
        if (scanType !== 'directory') {
            sh.arg(`--${scanType}`);
        }
        sh.arg(`${scanTarget}`);
        sh.arg('--recursive');
        sh.arg('--json');
        sh.arg('scaresults.json');
        const pipe: trm.ToolRunner = curl.pipeExecOutputToTool(sh);
        await pipe.exec();

        return;

    } catch (err) {
        throw new Error(err);

    }
}

// Test the SCA scan environment
async function testSCA(): Promise<void> {

    try {
        const curlPath: string = tl.which('curl', true);
        const shPath: string = tl.which('sh', true);
        const curl: trm.ToolRunner = tl.tool(curlPath);
        curl.arg('-sSL');
        curl.arg('https://download.sourceclear.com/ci.sh');
        const sh: trm.ToolRunner = tl.tool(shPath);
        sh.arg('-s');
        sh.arg('--');
        sh.arg('test');
        const pipe: trm.ToolRunner = curl.pipeExecOutputToTool(sh);
        await pipe.exec();

        return;

    } catch (err) {
        throw new Error(err);

    }
}

run();
