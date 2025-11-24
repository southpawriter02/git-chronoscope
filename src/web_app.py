"""
Web-based GUI for git-chronoscope using Flask.
Provides an easy-to-use interface for generating Git repository time-lapses.
"""
import os
import sys
import tempfile
import shutil
import threading
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify, send_file
from src.git_utils import GitRepo
from src.frame_renderer import FrameRenderer
from src.video_encoder import VideoEncoder

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max upload
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()

# Store job status in memory (in production, use Redis or database)
# Note: Jobs are lost on server restart in development mode
jobs = {}


class TimelapseJob:
    """Represents a time-lapse generation job."""
    def __init__(self, job_id, repo_path, options):
        self.job_id = job_id
        self.repo_path = repo_path
        self.options = options
        self.status = 'pending'  # pending, running, completed, failed
        self.progress = 0  # 0-100
        self.message = ''
        self.output_path = None
        self.error = None


def generate_timelapse_worker(job):
    """Worker function to generate time-lapse in background."""
    try:
        job.status = 'running'
        job.message = 'Initializing...'
        
        # Create temporary directory for frames
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Initialize modules
            resolutions = {
                "720p": (1280, 720),
                "1080p": (1920, 1080),
                "4k": (3840, 2160)
            }
            width, height = resolutions[job.options.get('resolution', '1080p')]
            
            frame_renderer = FrameRenderer(
                width=width,
                height=height,
                bg_color=job.options.get('bg_color', '#141618'),
                text_color=job.options.get('text_color', '#FFFFFF'),
                font_path=job.options.get('font_path'),
                font_size=job.options.get('font_size', 15),
                no_email=job.options.get('no_email', False)
            )
            
            git_repo = GitRepo(job.repo_path)
            
            # Get Git history
            job.message = 'Analyzing repository...'
            job.progress = 5
            history = git_repo.get_commit_history(branch=job.options.get('branch'))
            
            if not history:
                raise ValueError("No commits found in the specified branch.")
            
            job.message = f'Found {len(history)} commits. Rendering frames...'
            job.progress = 10
            
            # Render frames
            frame_paths = []
            for i, commit in enumerate(history):
                file_contents = git_repo.get_file_tree_at_commit(commit['commit_obj'])
                frame = frame_renderer.render_frame(commit, file_contents)
                
                frame_path = os.path.join(temp_dir, f"frame_{i:05d}.png")
                frame.save(frame_path)
                frame_paths.append(frame_path)
                
                # Update progress (10% to 80%)
                job.progress = 10 + int((i + 1) / len(history) * 70)
                job.message = f'Rendering frames: {i+1}/{len(history)}'
            
            # Encode video
            job.message = 'Encoding video...'
            job.progress = 80
            
            output_format = job.options.get('format', 'mp4')
            output_filename = f"timelapse_{job.job_id}.{output_format}"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            video_encoder = VideoEncoder(
                output_path,
                frame_rate=job.options.get('fps', 2),
                format=output_format
            )
            video_encoder.create_video_from_frames(frame_paths)
            
            job.output_path = output_path
            job.status = 'completed'
            job.progress = 100
            job.message = 'Time-lapse generated successfully!'
            
        finally:
            # Cleanup temporary frames
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                
    except Exception as e:
        job.status = 'failed'
        job.error = str(e)
        job.message = f'Error: {str(e)}'


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/api/branches', methods=['POST'])
def get_branches():
    """Get available branches from a repository."""
    try:
        data = request.get_json()
        repo_path = data.get('repo_path')
        
        if not repo_path or not os.path.exists(repo_path):
            return jsonify({'error': 'Invalid repository path'}), 400
        
        git_repo = GitRepo(repo_path)
        branches = [ref.name for ref in git_repo.repo.references if 'remotes' not in ref.name]
        
        return jsonify({'branches': branches})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/generate', methods=['POST'])
def generate():
    """Start generating a time-lapse."""
    try:
        data = request.get_json()
        repo_path = data.get('repo_path')
        
        if not repo_path or not os.path.exists(repo_path):
            return jsonify({'error': 'Invalid repository path'}), 400
        
        # Generate job ID
        job_id = f"{int(time.time())}_{len(jobs)}"
        
        # Create job
        options = {
            'format': data.get('format', 'mp4'),
            'branch': data.get('branch'),
            'fps': int(data.get('fps', 2)),
            'resolution': data.get('resolution', '1080p'),
            'bg_color': data.get('bg_color', '#141618'),
            'text_color': data.get('text_color', '#FFFFFF'),
            'font_size': int(data.get('font_size', 15)),
            'no_email': data.get('no_email', False)
        }
        
        job = TimelapseJob(job_id, repo_path, options)
        jobs[job_id] = job
        
        # Start generation in background thread
        thread = threading.Thread(target=generate_timelapse_worker, args=(job,))
        thread.daemon = True
        thread.start()
        
        return jsonify({'job_id': job_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status/<job_id>')
def get_status(job_id):
    """Get the status of a time-lapse generation job."""
    job = jobs.get(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify({
        'status': job.status,
        'progress': job.progress,
        'message': job.message,
        'error': job.error,
        'has_output': job.output_path is not None
    })


@app.route('/api/download/<job_id>')
def download(job_id):
    """Download the generated time-lapse."""
    job = jobs.get(job_id)
    
    if not job or not job.output_path:
        return jsonify({'error': 'Job not found or not completed'}), 404
    
    if not os.path.exists(job.output_path):
        return jsonify({'error': 'Output file not found'}), 404
    
    return send_file(
        job.output_path,
        as_attachment=True,
        download_name=os.path.basename(job.output_path)
    )


def run_server(host='127.0.0.1', port=5000, debug=False):
    """
    Run the Flask development server.
    
    WARNING: Debug mode should NEVER be enabled in production as it can
    allow arbitrary code execution. Only use debug=True during development.
    """
    if debug:
        print("WARNING: Debug mode is enabled. Do not use in production!")
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    # Only enable debug mode if explicitly requested via environment variable
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    run_server(debug=debug_mode)
