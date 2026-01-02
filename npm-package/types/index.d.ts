/**
 * Type definitions for git-chronoscope npm package
 */

export interface GenerateOptions {
  /** Output format: 'mp4', 'gif', or 'html' */
  format?: 'mp4' | 'gif' | 'html';
  /** Git branch to visualize */
  branch?: string;
  /** Frames per second (default: 2) */
  fps?: number;
  /** Resolution: '720p', '1080p', or '4k' (default: '1080p') */
  resolution?: '720p' | '1080p' | '4k';
  /** Background color in hex format (e.g., '#141618') */
  bgColor?: string;
  /** Text color in hex format (e.g., '#FFFFFF') */
  textColor?: string;
  /** Glob patterns for files to include */
  include?: string[];
  /** Glob patterns for files to exclude */
  exclude?: string[];
  /** Enable author color highlighting */
  authorColors?: boolean;
  /** Hide author emails */
  noEmail?: boolean;
  /** Redact sensitive data (API keys, passwords, etc.) */
  redactSecrets?: boolean;
  /** Preview without generating video */
  dryRun?: boolean;
  /** Process every Nth commit (for large repos) */
  sampleRate?: number;
  /** Limit to N most recent commits */
  maxCommits?: number;
  /** Only include commits after this date (YYYY-MM-DD) */
  since?: string;
  /** Only include commits before this date (YYYY-MM-DD) */
  until?: string;
}

export interface GenerateResult {
  /** Whether generation succeeded */
  success: boolean;
  /** Standard output from the CLI */
  output: string;
  /** Error message if failed */
  error: string;
}

export interface InstallationCheck {
  /** Whether all dependencies are installed */
  ok: boolean;
  /** List of missing dependencies */
  errors: string[];
}

/**
 * Generate a time-lapse visualization of a Git repository
 *
 * @param repoPath - Path to the Git repository
 * @param outputPath - Path for the output file
 * @param options - Generation options
 * @returns Promise resolving to generation result
 *
 * @example
 * ```javascript
 * const { generate } = require('git-chronoscope');
 *
 * const result = await generate('/path/to/repo', 'output.mp4', {
 *   format: 'mp4',
 *   resolution: '1080p',
 *   authorColors: true
 * });
 *
 * if (result.success) {
 *   console.log('Video generated successfully!');
 * } else {
 *   console.error('Error:', result.error);
 * }
 * ```
 */
export function generate(
  repoPath: string,
  outputPath: string,
  options?: GenerateOptions
): Promise<GenerateResult>;

/**
 * Get the version of the npm wrapper
 * @returns Version string (e.g., '0.9.0-beta.2')
 */
export function version(): string;

/**
 * Check if all required dependencies are installed
 * @returns Promise resolving to installation status
 *
 * @example
 * ```javascript
 * const { checkInstallation } = require('git-chronoscope');
 *
 * const { ok, errors } = await checkInstallation();
 * if (!ok) {
 *   console.error('Missing dependencies:', errors);
 * }
 * ```
 */
export function checkInstallation(): Promise<InstallationCheck>;
