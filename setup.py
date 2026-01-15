import os
import subprocess
import sys

def install_requirements():
    """
    Attempts to install dependencies with interrupt handling.
    """
    req_file = "requirements.txt"
    
    if not os.path.exists(req_file):
        print(f"\033[91m[!] Error: {req_file} not found. Cannot proceed with setup.\033[0m")
        return

    print("\033[94m[*] Attempting to install dependencies globally...\033[0m")
    try:
        # Try direct installation
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
        print("\033[92m[+] Dependencies installed successfully.\033[0m")
    except KeyboardInterrupt:
        print("\033[93m\n[!] Setup interrupted by operator. Environment may be unstable.\033[0m")
    except subprocess.CalledProcessError:
        print("\033[93m[!] Global installation failed. Initializing Virtual Environment...\033[0m")
        create_venv(req_file)

def create_venv(req_file):
    """
    Creates a virtual environment and installs requirements with interrupt handling.
    """
    venv_dir = "venv"
    try:
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
        
        if os.name == "nt":  # Windows
            pip_exe = os.path.join(venv_dir, "Scripts", "pip.exe")
        else:  # Linux / macOS
            pip_exe = os.path.join(venv_dir, "bin", "pip")

        print(f"\033[94m[*] Installing requirements into {venv_dir}...\033[0m")
        subprocess.check_call([pip_exe, "install", "-r", req_file])
        print(f"\033[92m[+] Setup complete.\033[0m")
            
    except KeyboardInterrupt:
        print(f"\033[91m\n[!] Virtual environment setup aborted by operator.\033[0m")
    except Exception as e:
        print(f"\033[91m[!] Fatal Error: {e}\033[0m")

if __name__ == "__main__":
    try:
        install_requirements()
    except KeyboardInterrupt:
        sys.exit(0)