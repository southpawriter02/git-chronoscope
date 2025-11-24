// Git Chronoscope - Web Interface JavaScript

let currentJobId = null;
let statusCheckInterval = null;

document.addEventListener('DOMContentLoaded', function() {
    // Set up event listeners
    document.getElementById('load-branches-btn').addEventListener('click', loadBranches);
    document.getElementById('generate-btn').addEventListener('click', generateTimelapse);
    document.getElementById('download-btn').addEventListener('click', downloadTimelapse);
    
    // Load repository path from localStorage if available
    const savedRepoPath = localStorage.getItem('lastRepoPath');
    if (savedRepoPath) {
        document.getElementById('repo-path').value = savedRepoPath;
    }
});

async function loadBranches() {
    const repoPath = document.getElementById('repo-path').value.trim();
    
    if (!repoPath) {
        alert('Please enter a repository path first.');
        return;
    }
    
    const btn = document.getElementById('load-branches-btn');
    btn.disabled = true;
    btn.textContent = 'Loading...';
    
    try {
        const response = await fetch('/api/branches', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ repo_path: repoPath })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to load branches');
        }
        
        const branchSelect = document.getElementById('branch');
        branchSelect.innerHTML = '<option value="">Current branch</option>';
        
        data.branches.forEach(branch => {
            const option = document.createElement('option');
            option.value = branch;
            option.textContent = branch;
            branchSelect.appendChild(option);
        });
        
        alert(`Successfully loaded ${data.branches.length} branch(es)!`);
        
    } catch (error) {
        alert(`Error loading branches: ${error.message}`);
    } finally {
        btn.disabled = false;
        btn.textContent = 'Load Branches';
    }
}

async function generateTimelapse() {
    const repoPath = document.getElementById('repo-path').value.trim();
    
    if (!repoPath) {
        alert('Please enter a repository path.');
        return;
    }
    
    // Save repository path
    localStorage.setItem('lastRepoPath', repoPath);
    
    // Get configuration
    const config = {
        repo_path: repoPath,
        branch: document.getElementById('branch').value || null,
        format: document.getElementById('format').value,
        resolution: document.getElementById('resolution').value,
        fps: parseInt(document.getElementById('fps').value),
        bg_color: document.getElementById('bg-color').value,
        text_color: document.getElementById('text-color').value,
        font_size: parseInt(document.getElementById('font-size').value),
        no_email: document.getElementById('no-email').checked
    };
    
    const btn = document.getElementById('generate-btn');
    btn.disabled = true;
    btn.textContent = 'Starting...';
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(config)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to start generation');
        }
        
        currentJobId = data.job_id;
        
        // Show status section
        document.getElementById('status-section').style.display = 'block';
        document.getElementById('download-btn').style.display = 'none';
        
        // Start polling for status
        startStatusPolling();
        
    } catch (error) {
        alert(`Error starting generation: ${error.message}`);
        btn.disabled = false;
        btn.textContent = 'Generate Time-lapse';
    }
}

function startStatusPolling() {
    // Clear any existing interval
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
    }
    
    // Check status immediately
    checkStatus();
    
    // Then check every 2 seconds
    statusCheckInterval = setInterval(checkStatus, 2000);
}

async function checkStatus() {
    if (!currentJobId) return;
    
    try {
        const response = await fetch(`/api/status/${currentJobId}`);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to check status');
        }
        
        // Update progress bar
        const progressFill = document.getElementById('progress-fill');
        progressFill.style.width = `${data.progress}%`;
        progressFill.textContent = `${data.progress}%`;
        
        // Update status message
        document.getElementById('status-message').textContent = data.message;
        
        // Update detail based on status
        const statusDetail = document.getElementById('status-detail');
        if (data.status === 'running') {
            statusDetail.textContent = 'Processing... This may take a few minutes.';
        } else if (data.status === 'completed') {
            statusDetail.textContent = 'Your time-lapse is ready!';
            document.getElementById('download-btn').style.display = 'block';
            stopStatusPolling();
            
            // Re-enable generate button
            const btn = document.getElementById('generate-btn');
            btn.disabled = false;
            btn.textContent = 'Generate Time-lapse';
        } else if (data.status === 'failed') {
            statusDetail.textContent = `Error: ${data.error || 'Unknown error occurred'}`;
            statusDetail.style.color = 'var(--danger-color)';
            stopStatusPolling();
            
            // Re-enable generate button
            const btn = document.getElementById('generate-btn');
            btn.disabled = false;
            btn.textContent = 'Generate Time-lapse';
        }
        
    } catch (error) {
        console.error('Error checking status:', error);
        // Don't stop polling on error, might be temporary
    }
}

function stopStatusPolling() {
    if (statusCheckInterval) {
        clearInterval(statusCheckInterval);
        statusCheckInterval = null;
    }
}

function downloadTimelapse() {
    if (!currentJobId) return;
    
    window.location.href = `/api/download/${currentJobId}`;
}

// Clean up interval when page is unloaded
window.addEventListener('beforeunload', function() {
    stopStatusPolling();
});
