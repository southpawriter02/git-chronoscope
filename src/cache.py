"""
Frame caching module for git-chronoscope.
Caches rendered frames by commit hash and configuration to speed up regeneration.
"""
import os
import hashlib
import shutil
import json
from pathlib import Path
from PIL import Image


class FrameCache:
    """
    Caches rendered frames to avoid re-rendering unchanged commits.
    
    Cache structure:
        <cache_dir>/<repo_hash>/<commit_hash>_<config_hash>.png
    """
    
    DEFAULT_CACHE_DIR = os.path.expanduser("~/.git-chronoscope/cache")
    
    def __init__(self, repo_path: str, cache_dir: str = None):
        """
        Initialize the frame cache.
        
        :param repo_path: Path to the Git repository (used to create unique cache dir).
        :param cache_dir: Custom cache directory. Defaults to ~/.git-chronoscope/cache.
        """
        self.cache_dir = cache_dir or self.DEFAULT_CACHE_DIR
        
        # Create a unique subdirectory for this repository
        repo_hash = hashlib.md5(os.path.abspath(repo_path).encode()).hexdigest()[:12]
        self.repo_cache_dir = os.path.join(self.cache_dir, repo_hash)
        
        # Statistics
        self.hits = 0
        self.misses = 0
        
        # Ensure cache directory exists
        os.makedirs(self.repo_cache_dir, exist_ok=True)
    
    def _generate_config_hash(self, config: dict) -> str:
        """
        Generate a hash from rendering configuration.
        
        :param config: Dictionary of rendering settings (resolution, colors, etc.)
        :return: Short hash string.
        """
        config_str = json.dumps(config, sort_keys=True)
        return hashlib.md5(config_str.encode()).hexdigest()[:8]
    
    def _get_cache_path(self, commit_hash: str, config_hash: str) -> str:
        """Get the full path for a cached frame."""
        filename = f"{commit_hash}_{config_hash}.png"
        return os.path.join(self.repo_cache_dir, filename)
    
    def get(self, commit_hash: str, config: dict) -> Image.Image:
        """
        Retrieve a cached frame if it exists.
        
        :param commit_hash: The commit hash (short or full).
        :param config: Rendering configuration dictionary.
        :return: PIL Image if cached, None otherwise.
        """
        config_hash = self._generate_config_hash(config)
        cache_path = self._get_cache_path(commit_hash, config_hash)
        
        if os.path.exists(cache_path):
            try:
                img = Image.open(cache_path)
                img.load()  # Force load to catch corrupted files
                self.hits += 1
                return img
            except Exception:
                # Corrupted cache file, remove it
                os.remove(cache_path)
        
        self.misses += 1
        return None
    
    def put(self, commit_hash: str, config: dict, frame: Image.Image) -> str:
        """
        Store a rendered frame in the cache.
        
        :param commit_hash: The commit hash.
        :param config: Rendering configuration dictionary.
        :param frame: The rendered PIL Image.
        :return: Path to the cached file.
        """
        config_hash = self._generate_config_hash(config)
        cache_path = self._get_cache_path(commit_hash, config_hash)
        
        frame.save(cache_path, "PNG")
        return cache_path
    
    def clear(self) -> int:
        """
        Clear all cached frames for this repository.
        
        :return: Number of files deleted.
        """
        count = 0
        if os.path.exists(self.repo_cache_dir):
            for f in os.listdir(self.repo_cache_dir):
                filepath = os.path.join(self.repo_cache_dir, f)
                if os.path.isfile(filepath):
                    os.remove(filepath)
                    count += 1
        return count
    
    def clear_all(self) -> int:
        """
        Clear all cached frames for all repositories.
        
        :return: Number of directories deleted.
        """
        count = 0
        if os.path.exists(self.cache_dir):
            for d in os.listdir(self.cache_dir):
                dirpath = os.path.join(self.cache_dir, d)
                if os.path.isdir(dirpath):
                    shutil.rmtree(dirpath)
                    count += 1
        return count
    
    def get_stats(self) -> dict:
        """
        Get cache statistics.
        
        :return: Dictionary with hits, misses, and hit rate.
        """
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "total": total,
            "hit_rate": hit_rate
        }
    
    def get_cache_size(self) -> tuple:
        """
        Get the size of the cache for this repository.
        
        :return: Tuple of (file_count, total_bytes).
        """
        file_count = 0
        total_bytes = 0
        
        if os.path.exists(self.repo_cache_dir):
            for f in os.listdir(self.repo_cache_dir):
                filepath = os.path.join(self.repo_cache_dir, f)
                if os.path.isfile(filepath):
                    file_count += 1
                    total_bytes += os.path.getsize(filepath)
        
        return file_count, total_bytes
