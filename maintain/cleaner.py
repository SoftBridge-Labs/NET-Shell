import os
import shutil

def purge_cache():
    """
    Recursively finds and removes all __pycache__ directories 
    within the project folder to keep the workspace clean.
    """
    print("\033[93m[*] Scanning for temporary cache files...\033[0m")
    count = 0
    # Walk through the current directory and all subdirectories
    for root, dirs, files in os.walk(".", topdown=False):
        for name in dirs:
            if name == "__pycache__":
                path = os.path.join(root, name)
                try:
                    # Remove the directory and all its contents
                    shutil.rmtree(path)
                    print(f"\033[2m[-] Removed: {path}\033[0m")
                    count += 1
                except Exception as e:
                    print(f"\033[91m[!] Failed to remove {path}: {e}\033[0m")
    
    if count > 0:
        print(f"\033[92m[+] Successfully purged {count} cache directories.\033[0m")
    else:
        print("\033[96m[i] System is already clean. No cache files found.\033[0m")

if __name__ == "__main__":
    # Allow the script to be run independently for quick cleaning
    purge_cache()