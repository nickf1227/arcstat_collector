# ZFS ARC Statistics Monitoring Script

A Python script to collect and log ZFS Adaptive Replacement Cache (ARC) and L2ARC statistics using the `arcstat` utility.

## Features

- Collects ARC/L2ARC performance metrics at configurable intervals
- Logs data to CSV for long-term monitoring and analysis
- Tracks extended statistics including:
  - L2ARC MRU/MFU percentages
  - MRU/MFU size metrics
  - Ghost cache statistics
  - Hit ratios and cache sizes
- Automatic unit conversion (bytes to GB)
- Configurable sampling parameters

## Prerequisites

- Python 3.x
- `arcstat` utility (part of ZFS on Linux/OpenZFS)
- Subprocess access to run system commands
- (Optional) Root privileges for arcstat if required by your system

## Installation

1. Download the script:
   ```bash
   wget https://example.com/path/to/arcstat_monitor.py
Make executable:

bash
Copy
chmod +x arcstat_monitor.py
Usage
bash
Copy
python3 arcstat_monitor.py
The script will:

Run continuously until interrupted (Ctrl+C)

Create arcstat.csv in the current directory

Collect data points every 30 seconds (configurable)

Configuration
Edit these variables in the script:

python
Copy
SAMPLING_INTERVAL = 10   # arcstat collection window (seconds)
SAMPLING_FREQUENCY = 30  # Time between samples (seconds)
CSV_OUTPUT_PATH = "."    # Output directory for CSV file
Output File (arcstat.csv)
Columns include:

timestamp: Measurement time (YYYY-MM-DD HH:MM:SS )

size (GB): Total ARC size

hit%: ARC hit percentage

l2size (GB): L2ARC device size

l2hit%: L2ARC hit percentage

l2mru%: L2ARC MRU (Most Recently Used) percentage

mrusz%: MRU size percentage

mrugsz (GB): MRU ghost size

l2mfu%: L2ARC MFU (Most Frequently Used) percentage

mfusz%: MFU size percentage

mfugsz (GB): MFU ghost size

Troubleshooting
Common Issues:

Permission Denied for arcstat

Run with sudo: sudo python3 arcstat_monitor.py

Configure sudoers file if needed

Missing Fields in Output

Verify arcstat version supports all required fields

Check field names match your arcstat implementation

CSV File Not Created

Verify write permissions in output directory

Check for existing file locks

Ensure script has proper execution rights

License
MIT License - see LICENSE file

Note: Field availability depends on your arcstat version. Verify supported fields with:

bash
Copy
arcstat -h
Sample CSV Output:

Copy
timestamp,size (GB),hit%,l2size (GB),l2hit%,l2mru%,mrusz%,mrugsz (GB),l2mfu%,mfusz%,mfugsz (GB)
2023-10-15 14:30:00,12.34,94.7,39.33,0.0,15.2,25.1,0.01,84.8,74.9,0.02
