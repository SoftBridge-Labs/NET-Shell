import subprocess
import os
import sys

# Replace this URL with your actual GitHub repository link
REPO_URL = "https://github.com/SoftBridge-Labs/NET-Shell.git"

def check_for_updates():
    """
    Checks the remote repository for any new commits and offers 
    to update the local files if they are behind.
    Includes KeyboardInterrupt handling for graceful exit.
    """
    print(f"\033[94m[*] Connecting to {REPO_URL}...\033[0m")
    
    # Check if the current directory is a git repository
    if not os.path.exists(".git"):
        print("\033[91m[!] Error: Local directory is not a Git repository.\033[0m")
        print("\033[96m[i] Please clone the project using 'git clone' to enable updates.\033[0m")
        return

    try:
        # Fetch the latest metadata from the remote
        subprocess.check_call(["git", "fetch"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Check the status of the local branch relative to the remote
        status = subprocess.check_output(["git", "status", "-uno"]).decode("utf-8")
        
        if "Your branch is behind" in status:
            print("\033[93m[!] UPDATE DETECTED: A newer version is available on GitHub.\033[0m")
            try:
                confirm = input("\033[92m>> Would you like to pull the updates now? (y/n): \033[0m").strip().lower()
                
                if confirm == 'y':
                    print("\033[94m[*] Pulling latest changes...\033[0m")
                    subprocess.check_call(["git", "pull"])
                    print("\033[92m[+] Update complete. Please restart the toolkit.\033[0m")
                else:
                    print("\033[93m[!] Update deferred by operator.\033[0m")
            except KeyboardInterrupt:
                print("\n\033[93m[!] Update cancelled by operator.\033[0m")
        else:
            print("\033[92m[+] System check complete. You are running the latest version.\033[0m")
            
    except subprocess.CalledProcessError:
        print("\033[91m[!] Error: Could not communicate with GitHub. Check your internet connection.\033[0m")
    except KeyboardInterrupt:
        print("\n\033[91m[!] Update check aborted by operator.\033[0m")
    except Exception as e:
        print(f"\033[91m[!] An unexpected error occurred: {e}\033[0m")

if __name__ == "__main__":
    check_for_updates()