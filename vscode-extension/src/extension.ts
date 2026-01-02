import * as vscode from 'vscode';
import { generateTimeLapse, generateFileTimeLapse, showOutput } from './commands';
import { SidebarProvider } from './sidebar';
import { Logger } from './logger';

/**
 * Called when the extension is activated.
 */
export function activate(context: vscode.ExtensionContext): void {
    const logger = Logger.getInstance();
    logger.info('Git Chronoscope extension activated');

    // Register commands
    const generateCommand = vscode.commands.registerCommand(
        'chronoscope.generate',
        generateTimeLapse
    );

    const generateFileCommand = vscode.commands.registerCommand(
        'chronoscope.generateFile',
        generateFileTimeLapse
    );

    const showOutputCommand = vscode.commands.registerCommand(
        'chronoscope.showOutput',
        showOutput
    );

    // Register sidebar
    const sidebarProvider = new SidebarProvider(context.extensionUri);
    const sidebarView = vscode.window.registerWebviewViewProvider(
        'chronoscope.sidebar',
        sidebarProvider
    );

    // Add to subscriptions
    context.subscriptions.push(
        generateCommand,
        generateFileCommand,
        showOutputCommand,
        sidebarView
    );

    logger.info('All commands registered');
}

/**
 * Called when the extension is deactivated.
 */
export function deactivate(): void {
    const logger = Logger.getInstance();
    logger.info('Git Chronoscope extension deactivated');
    logger.dispose();
}
