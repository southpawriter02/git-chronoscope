"""
Environment Manager for git-chronoscope.
Handles ephemeral environment cleanup and session isolation.
"""
import os
import atexit
import shutil
import tempfile
from typing import List, Optional


class EnvironmentManager:
    """
    Manages ephemeral environments and ensures cleanup.
    Tracks all temporary directories and registers cleanup handlers.
    """
    
    def __init__(self, cleanup_on_exit: bool = True):
        """
        Initialize the environment manager.
        
        :param cleanup_on_exit: If True, register atexit handler for cleanup.
        """
        self.temp_dirs: List[str] = []
        self.cleanup_on_exit = cleanup_on_exit
        self.cleaned_up = False
        
        if cleanup_on_exit:
            atexit.register(self.cleanup)
    
    def create_temp_dir(self, prefix: str = "chronoscope_") -> str:
        """
        Create a tracked temporary directory.
        
        :param prefix: Prefix for the temp directory name.
        :return: Path to the created temp directory.
        """
        temp_dir = tempfile.mkdtemp(prefix=prefix)
        self.temp_dirs.append(temp_dir)
        return temp_dir
    
    def track_temp_dir(self, path: str) -> None:
        """
        Track an existing temporary directory for cleanup.
        
        :param path: Path to the temp directory.
        """
        if path and os.path.exists(path) and path not in self.temp_dirs:
            self.temp_dirs.append(path)
    
    def cleanup(self, force: bool = False) -> int:
        """
        Clean up all tracked temporary directories.
        
        :param force: If True, cleanup even if already cleaned up.
        :return: Number of directories cleaned up.
        """
        if self.cleaned_up and not force:
            return 0
        
        cleaned = 0
        for temp_dir in self.temp_dirs:
            try:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    cleaned += 1
            except Exception:
                pass  # Best effort cleanup
        
        self.temp_dirs.clear()
        self.cleaned_up = True
        return cleaned
    
    def get_stats(self) -> dict:
        """Get environment statistics."""
        return {
            'temp_dirs_tracked': len(self.temp_dirs),
            'cleanup_on_exit': self.cleanup_on_exit,
            'cleaned_up': self.cleaned_up
        }


class NetworkPolicy:
    """
    Network egress control policy.
    Since git-chronoscope is offline-capable, this documents network requirements.
    """
    
    # git-chronoscope does NOT require network access for core functionality
    REQUIRES_NETWORK = False
    
    # Optional network features (none currently)
    OPTIONAL_NETWORK_FEATURES = []
    
    def __init__(self, offline_mode: bool = True):
        """
        Initialize network policy.
        
        :param offline_mode: If True, document that no network is needed.
        """
        self.offline_mode = offline_mode
    
    @classmethod
    def get_network_requirements(cls) -> dict:
        """
        Get network requirements for git-chronoscope.
        
        :return: Dictionary describing network needs.
        """
        return {
            'requires_network': cls.REQUIRES_NETWORK,
            'description': 'git-chronoscope operates fully offline. '
                          'It only reads local git repositories and generates local output files.',
            'optional_features': cls.OPTIONAL_NETWORK_FEATURES
        }
    
    def verify_offline_capable(self) -> bool:
        """
        Verify that git-chronoscope can run offline.
        
        :return: True (always, as no network is required).
        """
        return True
