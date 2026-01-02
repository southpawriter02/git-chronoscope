import * as vscode from 'vscode';

/**
 * Sidebar webview provider for git-chronoscope configuration.
 */
export class SidebarProvider implements vscode.WebviewViewProvider {
    private _view?: vscode.WebviewView;

    constructor(private readonly extensionUri: vscode.Uri) { }

    resolveWebviewView(
        webviewView: vscode.WebviewView,
        _context: vscode.WebviewViewResolveContext,
        _token: vscode.CancellationToken
    ): void {
        this._view = webviewView;

        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this.extensionUri]
        };

        webviewView.webview.html = this.getHtmlContent();

        // Handle messages from webview
        webviewView.webview.onDidReceiveMessage(async (message) => {
            switch (message.command) {
                case 'generate':
                    await vscode.commands.executeCommand('chronoscope.generate');
                    break;
                case 'generateFile':
                    await vscode.commands.executeCommand('chronoscope.generateFile');
                    break;
            }
        });
    }

    private getHtmlContent(): string {
        return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Git Chronoscope</title>
    <style>
        body {
            padding: 10px;
            font-family: var(--vscode-font-family);
            color: var(--vscode-foreground);
        }
        h2 {
            font-size: 14px;
            margin-bottom: 10px;
        }
        button {
            width: 100%;
            padding: 8px;
            margin-bottom: 8px;
            background: var(--vscode-button-background);
            color: var(--vscode-button-foreground);
            border: none;
            cursor: pointer;
            border-radius: 4px;
        }
        button:hover {
            background: var(--vscode-button-hoverBackground);
        }
        .info {
            font-size: 12px;
            color: var(--vscode-descriptionForeground);
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h2>🎬 Git Chronoscope</h2>
    
    <button id="generate">Generate Time-Lapse</button>
    <button id="generateFile">Time-Lapse for Current File</button>
    
    <div class="info">
        Generate a video visualization of your repository's evolution.
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        
        document.getElementById('generate').addEventListener('click', () => {
            vscode.postMessage({ command: 'generate' });
        });
        
        document.getElementById('generateFile').addEventListener('click', () => {
            vscode.postMessage({ command: 'generateFile' });
        });
    </script>
</body>
</html>
        `;
    }
}
