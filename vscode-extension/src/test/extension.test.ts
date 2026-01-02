import * as assert from 'assert';
import * as vscode from 'vscode';

suite('Extension Test Suite', () => {
    vscode.window.showInformationMessage('Start all tests.');

    test('Extension should be present', () => {
        assert.ok(vscode.extensions.getExtension('git-chronoscope.git-chronoscope'));
    });

    test('Commands should be registered', async () => {
        const commands = await vscode.commands.getCommands(true);

        assert.ok(
            commands.includes('chronoscope.generate'),
            'chronoscope.generate command should be registered'
        );
        assert.ok(
            commands.includes('chronoscope.generateFile'),
            'chronoscope.generateFile command should be registered'
        );
        assert.ok(
            commands.includes('chronoscope.showOutput'),
            'chronoscope.showOutput command should be registered'
        );
    });

    test('Configuration should have default values', () => {
        const config = vscode.workspace.getConfiguration('chronoscope');

        assert.strictEqual(
            config.get('pythonPath'),
            'python3',
            'Default pythonPath should be python3'
        );
        assert.strictEqual(
            config.get('outputFormat'),
            'mp4',
            'Default outputFormat should be mp4'
        );
        assert.strictEqual(
            config.get('fps'),
            5,
            'Default fps should be 5'
        );
    });
});
