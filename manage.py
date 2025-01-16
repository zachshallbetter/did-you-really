#!/usr/bin/env python3
import os
import sys
import subprocess
import signal
import time
import psutil

PID_FILE = 'flask_app.pid'

def start_service():
    """Start the Flask application."""
    if os.path.exists(PID_FILE):
        print("Service appears to be running. If it's not, remove flask_app.pid and try again.")
        return

    # Start the Flask app in the background
    process = subprocess.Popen(
        ['python', 'app.py'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
    
    # Give it a moment to start
    time.sleep(1)
    
    # Check if process is still running
    if process.poll() is not None:
        print("Failed to start service.")
        return
    
    # Save the PID
    with open(PID_FILE, 'w') as f:
        f.write(str(process.pid))
    
    print(f"Service started with PID: {process.pid}")

def stop_service():
    """Stop the Flask application."""
    if not os.path.exists(PID_FILE):
        print("Service doesn't appear to be running.")
        return

    try:
        # Read the PID
        with open(PID_FILE) as f:
            pid = int(f.read().strip())

        # Get the process and all its children
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            
            # Stop children first
            for child in children:
                child.terminate()
            
            # Stop parent
            parent.terminate()
            
            # Wait for processes to stop
            gone, alive = psutil.wait_procs(children + [parent], timeout=3)
            
            # Force kill if still alive
            for p in alive:
                p.kill()
            
        except psutil.NoSuchProcess:
            print("Process was already stopped.")
        
        os.remove(PID_FILE)
        print("Service stopped.")
        
    except Exception as e:
        print(f"Error stopping service: {e}")
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)

def status_service():
    """Check if the service is running."""
    if not os.path.exists(PID_FILE):
        print("Service is not running.")
        return

    try:
        with open(PID_FILE) as f:
            pid = int(f.read().strip())
        
        process = psutil.Process(pid)
        if process.is_running():
            print(f"Service is running (PID: {pid})")
        else:
            raise psutil.NoSuchProcess(pid)
            
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        print("Service crashed or was killed. Cleaning up PID file.")
        os.remove(PID_FILE)
    except Exception as e:
        print(f"Error checking service: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in ['start', 'stop', 'status']:
        print("Usage: python manage.py [start|stop|status]")
        sys.exit(1)

    command = sys.argv[1]
    
    if command == 'start':
        start_service()
    elif command == 'stop':
        stop_service()
    elif command == 'status':
        status_service() 