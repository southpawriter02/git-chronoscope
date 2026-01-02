import * as vscode from 'vscode';
import * as path from 'path';
import { Chronoscope } from './chronoscope';
import { Logger } from './logger';

const logger = Logger.getInstance();
const chronoscope = new Chronoscope();

/**
 * Command: Generate time-lapse for the workspace.
 */
export async function generateTimeLapse(): Promise<void> {
    const workspaceFolders = vscode.workspace.workspaceFolders;

    if (!workspaceFolders || workspaceFolders.length === 0) {
        vscode.window.showErrorMessage('No workspace folder open');
        return;
    }

    const repoPath = workspaceFolders[0].uri.fsPath;
    logger.info(`Generating time-lapse for: ${repoPath}`);

    // Ask for output location
    const outputUri = await vscode.window.showSaveDialog({
        defaultUri: vscode.Uri.file(path.join(repoPath, 'timelapse.mp4')),
        filters: {
            'Video': ['mp4'],
            'GIF': ['gif'],
            'HTML': ['html']
        },
        title: 'Save Time-Lapse'
    });

    if (!outputUri) {
        return;
    }

    const outputPath = outputUri.fsPath;
    const format = path.extname(outputPath).slice(1);

    try {
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: 'Generating Time-Lapse',
            cancellable: false
        }, async (progress) => {
            progress.report({ message: 'Processing commits...' });
            await chronoscope.generate(repoPath, outputPath, { format });
            return;
        });

        vscode.window.showInformationMessage(`Time-lapse saved to ${outputPath}`);
    } catch (error) {
        const err = error as Error;
        logger.error('Failed to generate time-lapse', err);
        vscode.window.showErrorMessage(`Failed to generate time-lapse: ${err.message}`);
    }
}

/**
 * Command: Generate time-lapse for the current file.
 */
export async function generateFileTimeLapse(): Promise<void> {
    const editor = vscode.window.activeTextEditor;

    if (!editor) {
        vscode.window.showErrorMessage('No file open');
        return;
    }

    const filePath = editor.document.uri.fsPath;
    const workspaceFolders = vscode.workspace.workspaceFolders;

    if (!workspaceFolders || workspaceFolders.length === 0) {
        vscode.window.showErrorMessage('No workspace folder open');
        return;
    }

    const repoPath = workspaceFolders[0].uri.fsPath;
    const relativePath = path.relative(repoPath, filePath);

    logger.info(`Generating time-lapse for file: ${relativePath}`);

    // Ask for output location
    const baseName = path.basename(filePath, path.extname(filePath));
    const outputUri = await vscode.window.showSaveDialog({
        defaultUri: vscode.Uri.file(path.join(repoPath, `${baseName}_timelapse.mp4`)),
        filters: {
            'Video': ['mp4'],
            'GIF': ['gif']
        },
        title: 'Save Time-Lapse'
    });

    if (!outputUri) {
        return;
    }

    const outputPath = outputUri.fsPath;
    const format = path.extname(outputPath).slice(1);

    try {
        await vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: `Generating Time-Lapse for ${relativePath}`,
            cancellable: false
        }, async (progress) => {
            progress.report({ message: 'Processing commits...' });
            await chronoscope.generate(repoPath, outputPath, {
                format,
                include: relativePath
            });
            return;
        });

        vscode.window.showInformationMessage(`Time-lapse saved to ${outputPath}`);
    } catch (error) {
        const err = error as Error;
        logger.error('Failed to generate file time-lapse', err);
        vscode.window.showErrorMessage(`Failed to generate time-lapse: ${err.message}`);
    }
}

/**
 * Command: Show output channel.
 */
export function showOutput(): void {
    logger.show();
}
