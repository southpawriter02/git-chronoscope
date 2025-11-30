// Git Chronoscope - Web Interface JavaScript

let currentJobId = null;
let statusCheckInterval = null;

document.addEventListener('DOMContentLoaded', function() {
    // Set up event listeners
    document.getElementById('load-branches-btn').addEventListener('click', loadBranches);
    document.getElementById('generate-btn').addEventListener('click', generateTimelapse);
    document.getElementById('download-btn').addEventListener('click', downloadTimelapse);
    document.getElementById('preview-btn').addEventListener('click', previewFrame);
    document.getElementById('close-preview').addEventListener('click', closePreview);

    // Resolution change listener
    document.getElementById('resolution').addEventListener('change', toggleCustomResolution);

    // Color preview listeners
    document.getElementById('bg-color').addEventListener('input', updateColorPreview);
    document.getElementById('text-color').addEventListener('input', updateColorPreview);
    
    // Load repository path from localStorage if available
    const savedRepoPath = localStorage.getItem('lastRepoPath');
    if (savedRepoPath) {
        document.getElementById('repo-path').value = savedRepoPath;
    }

    // Initial color preview
    updateColorPreview();

    // Load job history
    loadJobHistory();
});

function toggleCustomResolution() {
    const resSelect = document.getElementById('resolution');
    const customGroup = document.getElementById('custom-res-group');

    if (resSelect.value === 'custom') {
        customGroup.style.display = 'block';
    } else {
        customGroup.style.display = 'none';
    }
}

function updateColorPreview() {
    const bgColor = document.getElementById('bg-color').value;
    const textColor = document.getElementById('text-color').value;
    const previewBox = document.getElementById('color-preview');

    previewBox.style.backgroundColor = bgColor;
    previewBox.style.color = textColor;
}

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

async function previewFrame() {
    const repoPath = document.getElementById('repo-path').value.trim();
    
    if (!repoPath) {
        alert('Please enter a repository path.');
        return;
    }

    const config = getConfiguration();
    if (!config) return; // Validation failed
    
    const btn = document.getElementById('preview-btn');
    btn.disabled = true;
    btn.textContent = 'Generating...';
    
    const previewSection = document.getElementById('preview-section');
    const previewImg = document.getElementById('preview-image');
    const loading = document.getElementById('preview-loading');

    previewSection.style.display = 'flex';
    previewImg.style.display = 'none';
    loading.style.display = 'block';

    try {
        const response = await fetch('/api/preview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(config)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate preview');
        }

        previewImg.src = `data:image/png;base64,${data.image}`;
        previewImg.style.display = 'block';
        loading.style.display = 'none';

    } catch (error) {
        alert(`Error generating preview: ${error.message}`);
        previewSection.style.display = 'none';
    } finally {
        btn.disabled = false;
        btn.textContent = 'Preview Frame';
    }
}

function closePreview() {
    document.getElementById('preview-section').style.display = 'none';
}

function getConfiguration() {
    const repoPath = document.getElementById('repo-path').value.trim();

    let width = null;
    let height = null;

    if (document.getElementById('resolution').value === 'custom') {
        width = parseInt(document.getElementById('res-width').value);
        height = parseInt(document.getElementById('res-height').value);

        if (!width || !height || width < 100 || height < 100) {
            alert('Please enter valid custom dimensions (min 100px).');
            return null;
        }
    }

    return {
        repo_path: repoPath,
        branch: document.getElementById('branch').value || null,
        format: document.getElementById('format').value,
        resolution: document.getElementById('resolution').value,
        width: width,
        height: height,
        fps: parseInt(document.getElementById('fps').value),
        bg_color: document.getElementById('bg-color').value,
        text_color: document.getElementById('text-color').value,
        font_size: parseInt(document.getElementById('font-size').value),
        no_email: document.getElementById('no-email').checked
    };
}

async function generateTimelapse() {
    const repoPath = document.getElementById('repo-path').value.trim();

    if (!repoPath) {
        alert('Please enter a repository path.');
        return;
    }

    // Save repository path
    localStorage.setItem('lastRepoPath', repoPath);

    const config = getConfiguration();
    if (!config) return;
    
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
        
        // Refresh job history immediately (it will show as pending/running)
        loadJobHistory();

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

            // Refresh history to show completed status
            loadJobHistory();

        } else if (data.status === 'failed') {
            statusDetail.textContent = `Error: ${data.error || 'Unknown error occurred'}`;
            statusDetail.style.color = 'var(--danger-color)';
            stopStatusPolling();
            
            // Re-enable generate button
            const btn = document.getElementById('generate-btn');
            btn.disabled = false;
            btn.textContent = 'Generate Time-lapse';

            // Refresh history to show failed status
            loadJobHistory();
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

async function loadJobHistory() {
    try {
        const response = await fetch('/api/jobs');
        const data = await response.json();

        const list = document.getElementById('jobs-list');
        list.innerHTML = '';

        if (data.jobs.length === 0) {
            list.innerHTML = '<p class="no-jobs">No recent jobs found.</p>';
            return;
        }

        data.jobs.forEach(job => {
            const item = document.createElement('div');
            item.className = 'job-item';

            const date = new Date(job.created_at * 1000).toLocaleString();

            let statusClass = '';
            if (job.status === 'completed') statusClass = 'status-completed';
            else if (job.status === 'failed') statusClass = 'status-failed';
            else statusClass = 'status-running';

            let actionHtml = '';
            if (job.has_output) {
                actionHtml = `<a href="/api/download/${job.id}" class="btn btn-success btn-sm">Download</a>`;
            }

            item.innerHTML = `
                <div class="job-info">
                    <div class="job-repo">${job.repo_path}</div>
                    <div class="job-meta">
                        ${date} • ${job.format.toUpperCase()}
                        <span class="job-status ${statusClass}">${job.status}</span>
                    </div>
                </div>
                <div class="job-actions">
                    ${actionHtml}
                </div>
            `;

            list.appendChild(item);
        });

    } catch (error) {
        console.error('Error loading job history:', error);
    }
}

// Clean up interval when page is unloaded
window.addEventListener('beforeunload', function() {
    stopStatusPolling();
});
