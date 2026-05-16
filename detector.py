import csv

# ==========================================
# 1. CONFIGURATION
# ==========================================
WINDOW_SIZE = 10          # Group data into 10-second blocks
BASELINE_WINDOWS = 15     # Use the first 15 windows (150 seconds) to learn "normal"
THRESHOLD_MULTIPLIER = 3  # Flag a window if it's 3x higher than baseline
SUSTAINED_COUNT = 3       # Number of consecutive spikes needed to trigger an alert

# ==========================================
# 2. PHASE 1: READ CSV & GROUP INTO TIME WINDOWS
# ==========================================
windows = []
current_window_bytes = 0
seconds_counted = 0
window_start_time = None

print("[*] Reading fake_traffic.csv and processing time windows...")

with open("fake_traffic.csv", mode="r") as file:
    reader = csv.reader(file)
    header = next(reader)  # Skip the header row ("Timestamp", "Packet_Size_Bytes")
    
    for row in reader:
        timestamp = int(row[0])
        packet_bytes = int(row[1])
        
        # Mark the start timestamp of the current window
        if window_start_time is None:
            window_start_time = timestamp
            
        # Accumulate data volume and increment second counter
        current_window_bytes += packet_bytes
        seconds_counted += 1
        
        # Once we hit our window size (10 seconds), close this window and save it
        if seconds_counted == WINDOW_SIZE:
            window_end_time = timestamp
            windows.append({
                "start": window_start_time,
                "end": window_end_time,
                "total_bytes": current_window_bytes
            })
            # Reset trackers to start fresh for the next window
            current_window_bytes = 0
            seconds_counted = 0
            window_start_time = None

# ==========================================
# 3. PHASE 2: ESTABLISH THE BASELINE
# ==========================================
# Extract the total volumes for just the first 15 windows (historical data)
historical_volumes = [w["total_bytes"] for w in windows[:BASELINE_WINDOWS]]
baseline_average = sum(historical_volumes) / len(historical_volumes)
alert_threshold = baseline_average * THRESHOLD_MULTIPLIER

print(f"[+] Baseline Established: Average window size is {baseline_average:.2f} bytes")
print(f"[+] Alert Threshold set to: {alert_threshold:.2f} bytes (3x baseline)\n")

# ==========================================
# 4. PHASE 3: DETECT SUSTAINED ANOMALIES & PRINT REPORT
# ==========================================
# Print a neat dashboard table header
print(f"{'TIME RANGE (UNIX)':<25} | {'TOTAL TRAFFIC':<15} | {'STATUS'}")
print("-" * 75)

consecutive_spikes = 0

for w in windows:
    time_label = f"{w['start']} - {w['end']}"
    volume = w["total_bytes"]
    
    # Check if this window exceeds our mathematical anomaly line
    if volume > alert_threshold:
        consecutive_spikes += 1
        
        # If it's a spike but hasn't lasted 3 windows yet, it's just a warning
        if consecutive_spikes < SUSTAINED_COUNT:
            status = f"[WARN] Spike Detected (Streak: {consecutive_spikes}/{SUSTAINED_COUNT})"
        # If it reaches or exceeds 3 windows, it escalates to Critical
        else:
            status = f"!!! CRITICAL: SUSTAINED ANOMALY (Streak: {consecutive_spikes}) !!!"
    else:
        # If traffic drops back to normal, completely reset the consecutive counter
        consecutive_spikes = 0
        status = "[OK]"
        
    # Print the formatted row of data
    print(f"{time_label:<25} | {volume:<15,} | {status}")

print("\n[*] Analysis complete.")
