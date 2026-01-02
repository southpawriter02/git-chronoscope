"""
Interactive Timeline Generator for git-chronoscope.
Generates a self-contained HTML/CSS/JS viewer for exploring repository history.
"""
import os
import json
import html
from typing import List, Dict, Optional


class TimelineGenerator:
    """
    Generates an interactive HTML timeline viewer for a Git repository.
    """
    
    def __init__(self, repo_name: str, branch: str):
        """
        Initialize the timeline generator.
        
        :param repo_name: Name of the repository.
        :param branch: Branch name.
        """
        self.repo_name = repo_name
        self.branch = branch
    
    def generate(
        self,
        commits: List[Dict],
        file_trees: List[Dict[str, str]],
        output_path: str,
        include_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None
    ) -> str:
        """
        Generate the interactive HTML timeline.
        
        :param commits: List of commit dictionaries with metadata.
        :param file_trees: List of file tree dictionaries (one per commit).
        :param output_path: Output path for the HTML file.
        :param include_patterns: Include filter patterns (for display).
        :param exclude_patterns: Exclude filter patterns (for display).
        :return: Path to generated HTML file.
        """
        # Prepare commit data for JSON embedding
        timeline_data = {
            "repository": self.repo_name,
            "branch": self.branch,
            "filters": {
                "include": include_patterns or [],
                "exclude": exclude_patterns or []
            },
            "commits": []
        }
        
        for i, commit in enumerate(commits):
            commit_data = {
                "index": i,
                "hash": commit["hash"],
                "author": commit["author_name"],
                "email": commit.get("author_email", ""),
                "date": commit["date"].isoformat(),
                "message": commit["message"],
                "files": file_trees[i] if i < len(file_trees) else {}
            }
            timeline_data["commits"].append(commit_data)
        
        # Generate the HTML
        html_content = self._generate_html(timeline_data)
        
        # Write to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return output_path
    
    def _generate_html(self, data: Dict) -> str:
        """Generate the complete HTML document."""
        json_data = json.dumps(data, ensure_ascii=False)
        # Escape </script> tags in JSON to prevent breaking the HTML
        json_data = json_data.replace("</script>", "<\\/script>")
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Git Timeline - {html.escape(data["repository"])}</title>
    <style>
{self._get_css()}
    </style>
</head>
<body>
    <div class="app">
        <header class="header">
            <h1>🔬 {html.escape(data["repository"])}</h1>
            <div class="branch-info">Branch: <strong>{html.escape(data["branch"])}</strong></div>
        </header>
        
        <div class="controls">
            <div class="playback">
                <button id="prev-btn" title="Previous commit">⏮️</button>
                <button id="play-btn" title="Play/Pause">▶️</button>
                <button id="next-btn" title="Next commit">⏭️</button>
                <select id="speed-select" title="Playback speed">
                    <option value="2000">0.5x</option>
                    <option value="1000" selected>1x</option>
                    <option value="500">2x</option>
                    <option value="250">4x</option>
                </select>
            </div>
            <div class="search-box">
                <input type="text" id="search-input" placeholder="🔍 Search commits or files...">
            </div>
            <div class="commit-counter">
                <span id="current-index">1</span> / <span id="total-commits">{len(data["commits"])}</span>
            </div>
        </div>
        
        <div class="timeline-container">
            <div class="timeline" id="timeline"></div>
        </div>
        
        <div class="main-content">
            <aside class="sidebar">
                <div class="commit-info" id="commit-info">
                    <div class="info-row"><span class="label">Commit:</span> <span id="info-hash">-</span></div>
                    <div class="info-row"><span class="label">Author:</span> <span id="info-author">-</span></div>
                    <div class="info-row"><span class="label">Date:</span> <span id="info-date">-</span></div>
                    <div class="info-row message"><span class="label">Message:</span><br><span id="info-message">-</span></div>
                </div>
                <div class="file-tree" id="file-tree">
                    <h3>📁 Files</h3>
                    <ul id="file-list"></ul>
                </div>
            </aside>
            <main class="code-viewer">
                <div class="file-header" id="file-header">Select a file to view</div>
                <pre class="code-content" id="code-content"></pre>
            </main>
        </div>
    </div>

    <script>
const TIMELINE_DATA = {json_data};
{self._get_javascript()}
    </script>
</body>
</html>'''

    def _get_css(self) -> str:
        """Return the embedded CSS styles."""
        return '''
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    color: #e4e4e4;
    min-height: 100vh;
}

.app { display: flex; flex-direction: column; height: 100vh; }

.header {
    background: rgba(0,0,0,0.3);
    padding: 15px 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
.header h1 { font-size: 1.4em; color: #64ffda; }
.branch-info { color: #888; font-size: 0.9em; }

.controls {
    background: rgba(0,0,0,0.2);
    padding: 12px 25px;
    display: flex;
    align-items: center;
    gap: 20px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
.playback { display: flex; gap: 8px; align-items: center; }
.playback button {
    background: rgba(100, 255, 218, 0.1);
    border: 1px solid rgba(100, 255, 218, 0.3);
    color: #64ffda;
    padding: 8px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1em;
    transition: all 0.2s;
}
.playback button:hover { background: rgba(100, 255, 218, 0.2); }
.playback select {
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.2);
    color: #e4e4e4;
    padding: 8px 12px;
    border-radius: 6px;
}
.search-box { flex: 1; max-width: 400px; }
.search-box input {
    width: 100%;
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.2);
    color: #e4e4e4;
    padding: 10px 15px;
    border-radius: 8px;
    font-size: 0.9em;
}
.search-box input:focus { outline: none; border-color: #64ffda; }
.commit-counter { color: #888; font-size: 0.9em; }

.timeline-container {
    background: rgba(0,0,0,0.2);
    padding: 20px 25px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    overflow-x: auto;
}
.timeline {
    display: flex;
    gap: 4px;
    min-width: max-content;
    align-items: center;
    height: 40px;
}
.timeline-dot {
    width: 12px;
    height: 12px;
    background: rgba(100, 255, 218, 0.3);
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
}
.timeline-dot:hover { transform: scale(1.4); background: rgba(100, 255, 218, 0.6); }
.timeline-dot.active { background: #64ffda; transform: scale(1.5); box-shadow: 0 0 10px #64ffda; }
.timeline-dot.filtered { opacity: 0.3; }
.timeline-dot .tooltip {
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(0,0,0,0.9);
    color: #fff;
    padding: 6px 10px;
    border-radius: 4px;
    font-size: 0.75em;
    white-space: nowrap;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s;
    margin-bottom: 8px;
}
.timeline-dot:hover .tooltip { opacity: 1; }

.main-content { display: flex; flex: 1; overflow: hidden; }

.sidebar {
    width: 300px;
    background: rgba(0,0,0,0.2);
    border-right: 1px solid rgba(255,255,255,0.1);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}
.commit-info {
    padding: 15px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
.info-row { margin-bottom: 8px; font-size: 0.85em; }
.info-row .label { color: #888; }
.info-row.message { margin-top: 12px; }
#info-message { color: #fff; font-weight: 500; }

.file-tree { flex: 1; overflow-y: auto; padding: 15px; }
.file-tree h3 { margin-bottom: 10px; font-size: 0.9em; color: #888; }
#file-list { list-style: none; }
#file-list li {
    padding: 6px 10px;
    font-size: 0.85em;
    cursor: pointer;
    border-radius: 4px;
    margin-bottom: 2px;
    word-break: break-all;
}
#file-list li:hover { background: rgba(100, 255, 218, 0.1); }
#file-list li.active { background: rgba(100, 255, 218, 0.2); color: #64ffda; }

.code-viewer { flex: 1; display: flex; flex-direction: column; overflow: hidden; }
.file-header {
    padding: 12px 20px;
    background: rgba(0,0,0,0.3);
    border-bottom: 1px solid rgba(255,255,255,0.1);
    font-size: 0.9em;
    color: #64ffda;
}
.code-content {
    flex: 1;
    overflow: auto;
    padding: 20px;
    margin: 0;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 0.85em;
    line-height: 1.6;
    white-space: pre-wrap;
    word-wrap: break-word;
    background: rgba(0,0,0,0.2);
}
'''
    
    def _get_javascript(self) -> str:
        """Return the embedded JavaScript code."""
        return '''
let currentIndex = 0;
let isPlaying = false;
let playInterval = null;
let playSpeed = 1000;
let filteredIndices = null;

const commits = TIMELINE_DATA.commits;
const timeline = document.getElementById('timeline');
const playBtn = document.getElementById('play-btn');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const speedSelect = document.getElementById('speed-select');
const searchInput = document.getElementById('search-input');
const currentIndexEl = document.getElementById('current-index');
const totalCommitsEl = document.getElementById('total-commits');
const fileList = document.getElementById('file-list');
const codeContent = document.getElementById('code-content');
const fileHeader = document.getElementById('file-header');

// Initialize timeline dots
commits.forEach((commit, i) => {
    const dot = document.createElement('div');
    dot.className = 'timeline-dot';
    dot.dataset.index = i;
    dot.innerHTML = `<div class="tooltip">${commit.hash.slice(0,7)} - ${commit.message.slice(0,30)}...</div>`;
    dot.addEventListener('click', () => goToCommit(i));
    timeline.appendChild(dot);
});

function goToCommit(index) {
    if (index < 0 || index >= commits.length) return;
    currentIndex = index;
    updateView();
}

function updateView() {
    const commit = commits[currentIndex];
    
    // Update timeline
    document.querySelectorAll('.timeline-dot').forEach((dot, i) => {
        dot.classList.toggle('active', i === currentIndex);
        dot.classList.toggle('filtered', filteredIndices && !filteredIndices.includes(i));
    });
    
    // Scroll timeline to show current dot
    const activeDot = document.querySelector('.timeline-dot.active');
    if (activeDot) {
        activeDot.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
    }
    
    // Update commit info
    document.getElementById('info-hash').textContent = commit.hash;
    document.getElementById('info-author').textContent = `${commit.author} <${commit.email}>`;
    document.getElementById('info-date').textContent = new Date(commit.date).toLocaleString();
    document.getElementById('info-message').textContent = commit.message;
    
    // Update file tree
    const files = Object.keys(commit.files).sort();
    fileList.innerHTML = files.map(f => `<li data-file="${f}">📄 ${f}</li>`).join('');
    
    // Add click handlers to files
    fileList.querySelectorAll('li').forEach(li => {
        li.addEventListener('click', () => {
            fileList.querySelectorAll('li').forEach(l => l.classList.remove('active'));
            li.classList.add('active');
            showFile(li.dataset.file);
        });
    });
    
    // Update counter
    currentIndexEl.textContent = currentIndex + 1;
    
    // Show first file by default
    if (files.length > 0) {
        showFile(files[0]);
        fileList.querySelector('li').classList.add('active');
    } else {
        fileHeader.textContent = 'No files in this commit';
        codeContent.textContent = '';
    }
}

function showFile(filePath) {
    const commit = commits[currentIndex];
    const content = commit.files[filePath] || '';
    fileHeader.textContent = filePath;
    codeContent.textContent = content;
}

function togglePlay() {
    isPlaying = !isPlaying;
    playBtn.textContent = isPlaying ? '⏸️' : '▶️';
    
    if (isPlaying) {
        playInterval = setInterval(() => {
            if (filteredIndices) {
                const currentPos = filteredIndices.indexOf(currentIndex);
                const nextPos = currentPos + 1;
                if (nextPos < filteredIndices.length) {
                    goToCommit(filteredIndices[nextPos]);
                } else {
                    togglePlay(); // Stop at end
                }
            } else {
                if (currentIndex < commits.length - 1) {
                    goToCommit(currentIndex + 1);
                } else {
                    togglePlay(); // Stop at end
                }
            }
        }, playSpeed);
    } else {
        clearInterval(playInterval);
    }
}

function handleSearch() {
    const query = searchInput.value.toLowerCase().trim();
    
    if (!query) {
        filteredIndices = null;
        totalCommitsEl.textContent = commits.length;
    } else {
        filteredIndices = commits
            .map((c, i) => ({ commit: c, index: i }))
            .filter(({ commit }) => 
                commit.message.toLowerCase().includes(query) ||
                commit.author.toLowerCase().includes(query) ||
                commit.hash.toLowerCase().includes(query) ||
                Object.keys(commit.files).some(f => f.toLowerCase().includes(query))
            )
            .map(({ index }) => index);
        
        totalCommitsEl.textContent = `${filteredIndices.length} (filtered)`;
        
        // Jump to first match if current not in results
        if (filteredIndices.length > 0 && !filteredIndices.includes(currentIndex)) {
            goToCommit(filteredIndices[0]);
            return;
        }
    }
    updateView();
}

// Event listeners
playBtn.addEventListener('click', togglePlay);
prevBtn.addEventListener('click', () => {
    if (filteredIndices) {
        const currentPos = filteredIndices.indexOf(currentIndex);
        if (currentPos > 0) goToCommit(filteredIndices[currentPos - 1]);
    } else {
        if (currentIndex > 0) goToCommit(currentIndex - 1);
    }
});
nextBtn.addEventListener('click', () => {
    if (filteredIndices) {
        const currentPos = filteredIndices.indexOf(currentIndex);
        if (currentPos < filteredIndices.length - 1) goToCommit(filteredIndices[currentPos + 1]);
    } else {
        if (currentIndex < commits.length - 1) goToCommit(currentIndex + 1);
    }
});
speedSelect.addEventListener('change', (e) => {
    playSpeed = parseInt(e.target.value);
    if (isPlaying) {
        togglePlay();
        togglePlay();
    }
});
searchInput.addEventListener('input', handleSearch);

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.target === searchInput) return;
    if (e.key === 'ArrowLeft') prevBtn.click();
    if (e.key === 'ArrowRight') nextBtn.click();
    if (e.key === ' ') { e.preventDefault(); togglePlay(); }
});

// Initialize
updateView();
'''
