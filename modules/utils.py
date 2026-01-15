import sys
import time

def typing_effect(text, speed=0.03):
    """
    Simulates a hacker-style typing effect.
    Includes interrupt handling to skip the animation if Ctrl+C is pressed.
    """
    try:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(speed)
        print()
    except KeyboardInterrupt:
        # If interrupted, print the remaining text immediately and move on
        sys.stdout.write('\r' + text + '\n')
        sys.stdout.flush()

def progress_bar(seconds):
    """
    Displays a visual progress bar for 'loading' sequences.
    Handles Ctrl+C to jump to 100% and continue.
    """
    try:
        for i in range(1, 21):
            time.sleep(seconds / 20)
            # Visual representation using '#' for progress and '.' for remaining space
            sys.stdout.write(f"\r[SYSTEM] Progress: [{'#' * i}{'.' * (20 - i)}] {i * 5}%")
            sys.stdout.flush()
        print()
    except KeyboardInterrupt:
        # Jump to completed bar on interrupt
        sys.stdout.write(f"\r[SYSTEM] Progress: [{'#' * 20}] 100% - INTERRUPTED\n")
        sys.stdout.flush()