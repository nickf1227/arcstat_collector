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



## Installation

1. I have a seperate dataset in my pool `/mnt/tank/tn_scripts` that I use for this purpose, and I highly recommend you should as well.
2. `git clone https://github.com/nickf1227/zpool-iostat-collector.git /mnt/tank/tn_scripts` Replace the path with where you want to store it on your system, and then run it.
3. You can call the script by running `python3 /mnt/tank/tn_scripts/zpool-iostat-collector.py`
4. If you have more than one pool you would like to monitor, you would need to copy the `zpool-iostat-collector.py` file. Something like this could work `cp /mnt/tank/tn_scripts/zpool-iostat-collector.py /mnt/tank/tn_scripts/zpool-iostat-collector-pool1.py && mv /mnt/tank/tn_scripts/zpool-iostat-collector.py /mnt/tank/tn_scripts/zpool-iostat-collector-pool2.py`
5. Then you would have to configure them booth (see below) and call them both individually.

## Configuration
Edit these variables in the script:

# Configurable settings
SAMPLING_INTERVAL = 30          # arcstat sampling interval in seconds
SAMPLING_FREQUENCY = 300         # How often to collect samples in seconds
CSV_OUTPUT_PATH = "."           # Output directory for CSV file

For now, columns include the below. I plan to expose more later. Please see https://openzfs.github.io/openzfs-docs/man/master/1/arcstat.1.html:
```
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
```
## Troubleshooting
Common Issues:

Permission Denied for arcstat

Run with sudo: sudo python3 arcstat_monitor.py
