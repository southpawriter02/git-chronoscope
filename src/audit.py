"""
Audit Logger for git-chronoscope.
Provides immutable, append-only logging of all operations.
"""
import os
import json
from datetime import datetime
from typing import Optional, Any


class AuditLogger:
    """
    Immutable audit logger for security and debugging.
    Writes append-only logs with timestamps.
    """
    
    def __init__(self, log_path: Optional[str] = None):
        """
        Initialize the audit logger.
        
        :param log_path: Path to the audit log file. None to disable logging.
        """
        self.log_path = log_path
        self.enabled = log_path is not None
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.operation_count = 0
    
    def _write_entry(self, entry: dict) -> bool:
        """
        Write an entry to the log file (append-only).
        
        :param entry: Dictionary to log.
        :return: True if written successfully.
        """
        if not self.enabled or not self.log_path:
            return False
        
        try:
            # Append-only write
            with open(self.log_path, 'a', encoding='utf-8') as f:
                json.dump(entry, f)
                f.write('\n')
            return True
        except (IOError, OSError):
            return False
    
    def log_start(self, repo_path: str, output_path: str, args: dict) -> None:
        """
        Log session start.
        
        :param repo_path: Repository path being processed.
        :param output_path: Output file path.
        :param args: CLI arguments.
        """
        self.operation_count += 1
        entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'operation': 'SESSION_START',
            'sequence': self.operation_count,
            'details': {
                'repo_path': repo_path,
                'output_path': output_path,
                'args': {k: str(v) for k, v in args.items() if not k.startswith('_')}
            }
        }
        self._write_entry(entry)
    
    def log_operation(self, operation: str, details: Optional[dict] = None) -> None:
        """
        Log a generic operation.
        
        :param operation: Name of the operation.
        :param details: Optional details dictionary.
        """
        self.operation_count += 1
        entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'operation': operation,
            'sequence': self.operation_count,
            'details': details or {}
        }
        self._write_entry(entry)
    
    def log_commits_processed(self, count: int, branch: str) -> None:
        """
        Log commits processing.
        
        :param count: Number of commits processed.
        :param branch: Branch name.
        """
        self.log_operation('COMMITS_PROCESSED', {
            'commit_count': count,
            'branch': branch
        })
    
    def log_output_generated(self, output_path: str, format: str, size_bytes: Optional[int] = None) -> None:
        """
        Log output file generation.
        
        :param output_path: Path to output file.
        :param format: Output format (mp4, gif, html).
        :param size_bytes: Optional file size.
        """
        self.log_operation('OUTPUT_GENERATED', {
            'output_path': output_path,
            'format': format,
            'size_bytes': size_bytes
        })
    
    def log_end(self, success: bool, error_message: Optional[str] = None) -> None:
        """
        Log session end.
        
        :param success: Whether session completed successfully.
        :param error_message: Optional error message if failed.
        """
        self.operation_count += 1
        entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.session_id,
            'operation': 'SESSION_END',
            'sequence': self.operation_count,
            'details': {
                'success': success,
                'total_operations': self.operation_count,
                'error': error_message
            }
        }
        self._write_entry(entry)
    
    def get_stats(self) -> dict:
        """Get audit logger statistics."""
        return {
            'enabled': self.enabled,
            'log_path': self.log_path,
            'session_id': self.session_id,
            'operation_count': self.operation_count
        }
