#!/bin/bash

# ==============================================================================
# Shell script to spawn multiple instances of a Python script for multitasking.
#
# Author: Gemini
# Date:   August 22, 2025
# ==============================================================================

# --- CONFIGURATION ---
# The path to the Python script you want to run.
PYTHON_SCRIPT_PATH="eric_wu/recreation_checker.py"

# The number of Python processes to spawn.
# Change this value to control the level of multitasking.
NUM_PROCESSES=3

# The directory to store the log files.
LOG_DIR="logs"

# --- SCRIPT EXECUTION ---

# Create the log directory if it doesn't exist.
mkdir -p "$LOG_DIR"

echo "Spawning $NUM_PROCESSES processes for '$PYTHON_SCRIPT_PATH'..."
echo "Output and errors will be saved to the '$LOG_DIR' directory."

PIDS=()

# Loop to spawn the specified number of processes.
for i in $(seq 1 $NUM_PROCESSES); do
    # Define unique log file names for each process.
    OUTPUT_LOG="$LOG_DIR/stdout_process_${i}.log"
    ERROR_LOG="$LOG_DIR/stderr_process_${i}.log"

    # Spawn the Python script in the background.
    # We use 'nohup' to ignore hangup signals, allowing the process to continue
    # running in the background even if the terminal is closed.
    # '>' redirects standard output (stdout) to the output log file,
    # '2>' redirects standard error (stderr) to the error log file,
    # '&' sends the process to the background, allowing the loop to continue.
    nohup python3 -u "$PYTHON_SCRIPT_PATH" > "$OUTPUT_LOG" 2> "$ERROR_LOG" &
    
    # Add the process ID (PID) of the last background command to the PIDS array.
    PIDS+=( $! )

    echo "Spawned process #$i (PID: $!)"
done

# Trap EXIT and kill all child processes
trap 'echo "Killing child processes..."; for pid in "${PIDS[@]}"; do kill "$pid" 2>/dev/null; done; exit' EXIT

echo "All processes have been started."
echo "You can check their progress and results in the '$LOG_DIR' directory."

# Wait for all background processes to finish.
wait

echo "All background processes have finished."
echo "Script execution complete."
