import sys
import csv
import os
import subprocess
import time

# Debug print: script start
print("Starting arcstat script...")

# Configurable settings
SAMPLING_INTERVAL = 30          # arcstat sampling interval in seconds
SAMPLING_FREQUENCY = 300         # How often to collect samples in seconds
CSV_OUTPUT_PATH = "."           # Output directory for CSV file

# Updated CSV header with new fields
csv_header = [
    "timestamp",
    "size (GB)",
    "hit%",
    "l2size (GB)",
    "l2hit%",
    "l2mru%",
    "mrusz%",
    "mrugsz (GB)",
    "l2mfu%",
    "mfusz%",
    "mfugsz (GB)"
]

def convert_bytes_to_gb(bytes_val):
    """Convert bytes to gigabytes (GiB)."""
    return round(bytes_val / (1024 ** 3), 2)

def parse_arcstat(input_lines):
    """Parse arcstat output lines into structured data."""
    data = []
    if len(input_lines) < 2:
        return data  # Not enough lines to parse
    
    # Skip header line (input_lines[0]) and process data lines
    for line in input_lines[1:]:
        line = line.strip()
        if not line:
            continue
        
        # Split on any whitespace (including multiple spaces)
        fields = line.split()
        if len(fields) != 11:
            print(f"Skipping invalid line: {line} (fields={len(fields)})")
            continue
        
        try:
            # Use current time as the timestamp
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            
            # Parse all fields
            new_row = [
                timestamp,
                convert_bytes_to_gb(int(fields[1])),   # size
                float(fields[2]),                      # hit%
                convert_bytes_to_gb(int(fields[3])),   # l2size
                float(fields[4]),                      # l2hit%
                float(fields[5]),                      # l2mru%
                float(fields[6]),                      # mrusz%
                convert_bytes_to_gb(int(fields[7])),   # mrugsz
                float(fields[8]),                      # l2mfu%
                float(fields[9]),                      # mfusz%
                convert_bytes_to_gb(int(fields[10]))   # mfugsz
            ]
            data.append(new_row)
        except (ValueError, IndexError) as e:
            print(f"Error parsing line: {line}. Error: {e}")
            continue
    
    return data

def collect_arcstat():
    """Collect arcstat data with additional fields."""
    command = (
        "arcstat -p -f time,size,hit%,l2size,l2hit%,l2mru%,mrusz%,mrugsz,l2mfu%,mfusz%,mfugsz "
        f"{SAMPLING_INTERVAL} 1"
    )
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error running command: {result.stderr}")
        return []
    
    print("Command output:")
    print(result.stdout)
    input_lines = result.stdout.splitlines()
    data = parse_arcstat(input_lines)
    
    if not data:
        print("No data parsed from command output.")
    
    return data

def write_to_csv(data):
    """Append data to the CSV file."""
    csv_file = os.path.join(CSV_OUTPUT_PATH, "arcstat.csv")
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(csv_header)
        writer.writerows(data)

def main():
    """Main loop to collect data periodically."""
    while True:
        print(f"\n--- Starting data collection at {time.strftime('%c')} ---")
        data = collect_arcstat()
        if data:
            write_to_csv(data)
        
        sleep_time = SAMPLING_FREQUENCY - SAMPLING_INTERVAL
        print(f"Sleeping for {sleep_time} seconds until next sample...")
        time.sleep(max(sleep_time, 1))  # Ensure sleep time is at least 1 second

if __name__ == "__main__":
    main()
