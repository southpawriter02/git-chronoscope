#!/usr/bin/env python3
"""
Git Chronoscope GUI Launcher
Starts the web-based graphical interface for git-chronoscope.
"""
import sys
import webbrowser
import time
import threading
from src.web_app import run_server

def open_browser(port):
    """Open the browser after a short delay."""
    time.sleep(1.5)
    webbrowser.open(f'http://127.0.0.1:{port}')

def main():
    """Launch the web interface."""
    port = 5000
    
    print("=" * 60)
    print("🎬 Git Chronoscope - Web Interface")
    print("=" * 60)
    print(f"\nStarting web server on http://127.0.0.1:{port}")
    print("\nThe interface will open in your browser automatically.")
    print("Press Ctrl+C to stop the server.\n")
    
    # Open browser in a separate thread
    browser_thread = threading.Thread(target=open_browser, args=(port,))
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Run the Flask server
        run_server(host='127.0.0.1', port=port, debug=False)
    except KeyboardInterrupt:
        print("\n\nShutting down server... Goodbye!")
        sys.exit(0)

if __name__ == '__main__':
    main()
