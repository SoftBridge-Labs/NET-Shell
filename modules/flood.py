import asyncio
import aiohttp
import time
from datetime import datetime

# Range of successful HTTP response codes
SUCCESS_CODES = range(200, 400)

# ANSI escape sequences for terminal styling
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
DIM = "\033[2m"
BLINK = "\033[5m"
RESET = "\033[0m"

def latency_bar(latency, avg, width=20):
    """Generates a visual bar representing current latency relative to the average."""
    ratio = min(latency / max(avg, 1), 2)
    filled = int((ratio / 2) * width)
    return "█" * filled + "░" * (width - filled)

async def _single_request(session, url, rid):
    """Performs a single GET request and returns data immediately upon completion."""
    start = time.perf_counter()
    ts = datetime.now().strftime("%H:%M:%S")

    try:
        async with session.get(url, timeout=10) as r:
            latency = (time.perf_counter() - start) * 1000
            return rid, ts, r.status, round(latency, 2)
    except Exception:
        latency = (time.perf_counter() - start) * 1000
        return rid, ts, None, round(latency, 2)

async def _runner(url, cycles, interval, concurrency):
    """Manages execution using as_completed for real-time status reporting."""
    success = fail = total = 0
    latencies = []
    rid_counter = 0

    try:
        async with aiohttp.ClientSession() as session:
            for cycle in range(1, cycles + 1):
                print(f"\n{CYAN}{'═'*50}")
                print(f"▶ CYCLE #{cycle} (Launching {concurrency} concurrent tasks)")
                print(f"{'═'*50}{RESET}")

                start_cycle = time.time()
                
                # Create the tasks
                tasks = []
                for _ in range(concurrency):
                    rid_counter += 1
                    tasks.append(_single_request(session, url, rid_counter))

                # key change: as_completed yields tasks as they finish, one by one
                for task in asyncio.as_completed(tasks):
                    rid, ts, status, latency = await task
                    
                    total += 1
                    latencies.append(latency)
                    avg = sum(latencies) / len(latencies)

                    is_ok = status in SUCCESS_CODES
                    status_color = GREEN if is_ok else RED
                    
                    if is_ok: success += 1
                    else: fail += 1

                    # Print the line IMMEDIATELY
                    bar = latency_bar(latency, avg)
                    print(
                        f"{DIM}│{RESET} [{ts}] Req#{rid:<3} | "
                        f"Status: {status_color}{str(status):<3}{RESET} | "
                        f"Latency: {latency:>7.2f} ms | {bar}"
                    )

                    # Update the footer counter
                    print(
                        f"\r{DIM}╰─ Totals → {GREEN}OK:{success}{RESET} | "
                        f"{RED}FAIL:{fail}{RESET} | {YELLOW}AVG:{avg:.2f}ms{RESET}", 
                        end="", flush=True
                    )

                # Wait for the remainder of the interval after the cycle completes
                wait_time = max(0, interval - (time.time() - start_cycle))
                if cycle < cycles:
                    await asyncio.sleep(wait_time)
    
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Flood sequence aborted by operator.{RESET}")
    finally:
        print(f"\n\n{YELLOW}--- FINAL SESSION SUMMARY ---{RESET}")
        print(f"Total Requests: {total} | Success: {success} | Failed: {fail}")

def requestURL(url, request_count, time_in_seconds, concurrent_requests=2):
    try:
        asyncio.run(_runner(url, request_count, time_in_seconds, concurrent_requests))
    except KeyboardInterrupt:
        pass