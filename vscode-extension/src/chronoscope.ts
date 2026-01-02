import * as vscode from 'vscode';
import * as cp from 'child_process';
import * as path from 'path';
import { Logger } from './logger';

/**
 * Wrapper for the git-chronoscope Python CLI.
 */
export class Chronoscope {
    private logger: Logger;

    constructor() {
        this.logger = Logger.getInstance();
    }

    /**
     * Get the configured Python path.
     */
    private getPythonPath(): string {
        const config = vscode.workspace.getConfiguration('chronoscope');
        return config.get<string>('pythonPath', 'python3');
    }

    /**
     * Get the chronoscope module path.
     */
    private getModulePath(): string {
        // Assumes chronoscope is installed or in parent directory
        const extensionPath = vscode.extensions.getExtension('git-chronoscope.git-chronoscope')?.extensionPath;
        if (extensionPath) {
            return path.join(extensionPath, '..');
        }
        return '.';
    }

    /**
     * Generate a time-lapse for a repository.
     */
    async generate(
        repoPath: string,
        outputPath: string,
        options: GenerateOptions = {}
    ): Promise<void> {
        const pythonPath = this.getPythonPath();
        const config = vscode.workspace.getConfiguration('chronoscope');

        const args = [
            '-m', 'src.main',
            repoPath,
            outputPath
        ];

        // Add options
        if (options.fps || config.get<number>('fps')) {
            args.push('--fps', String(options.fps || config.get<number>('fps', 5)));
        }
        if (options.format || config.get<string>('outputFormat')) {
            args.push('--format', options.format || config.get<string>('outputFormat', 'mp4'));
        }
        if (options.include) {
            args.push('--include', options.include);
        }

        this.logger.info(`Running: ${pythonPath} ${args.join(' ')}`);

        return new Promise((resolve, reject) => {
            const cwd = this.getModulePath();
            const process = cp.spawn(pythonPath, args, { cwd });

            process.stdout.on('data', (data) => {
                this.logger.info(data.toString().trim());
            });

            process.stderr.on('data', (data) => {
                this.logger.error(data.toString().trim());
            });

            process.on('close', (code) => {
                if (code === 0) {
                    this.logger.info('Time-lapse generated successfully');
                    resolve();
                } else {
                    reject(new Error(`Process exited with code ${code}`));
                }
            });

            process.on('error', (err) => {
                this.logger.error('Failed to start process', err);
                reject(err);
            });
        });
    }
}

export interface GenerateOptions {
    fps?: number;
    format?: string;
    include?: string;
}
