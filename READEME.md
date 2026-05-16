```markdown
## Keywords
* Anomaly Detection
* Watchdog
* Behavioral Analysis


## Setup and Installation

Since this iteration runs entirely on simulated operational data logs, no administrative or `sudo` network socket access is required.

1. Create a dedicated project directory on your machine:
   ```bash
   mkdir -p ~/Desktop/NetworkProject

```

2. Move your code execution scripts (`generator.py` and `detector.py`) into this directory.

## How to Run the Tool

Follow these sequential steps in your terminal environment to simulate traffic datasets and execute the detection logic:

1. **Navigate to the target workspace location:**
```bash
cd ~/Desktop/NetworkProject

```


2. **Generate the network traffic profile matrix:**
```bash
python3 generator.py

```


*This outputs `fake_traffic.csv`, mapping out 600 seconds (10 minutes) of typical network packet exchanges alongside a hard-coded, sustained traffic anomaly injection.*
3. **Execute the Anomaly Detector engine:**
```bash
python3 detector.py

```


*The system reads the dataset, structures rows into time-window arrays, computes average historic baseline values over the first 150 seconds, sets a triple-volume alarm threshold, and streams status telemetry row-by-row.*

## Configuration Metrics

You can modify behavior limits directly inside the configuration header of `detector.py`:

* `WINDOW_SIZE`: Adjusts grouping periods (default: `10` seconds).
* `BASELINE_WINDOWS`: Adjusts duration of historical learning input (default: `15` blocks).
* `THRESHOLD_MULTIPLIER`: Defines severity trigger limits (default: `3`x baseline).
* `SUSTAINED_COUNT`: Sets consecutive breach limits before system escalates a `[WARN]` state to `CRITICAL` (default: `3` consecutive windows).

```

```
