#!/bin/bash

# Welcome to the run.sh tutorial!
# This script solves the challenge of managing multiple tasks that need to run
# at different intervals within a SyftBox application.

# Problem: How do we keep track of when each task was last run?
# Solution: Create a directory to store timestamps for each section
TIMESTAMP_DIR="./script_timestamps"
mkdir -p "$TIMESTAMP_DIR"
mkdir -p "state"

# Problem: How do we determine if enough time has passed to run a task again?
# Solution: Create a function to check the time difference
function should_run() {
    local section=$1
    local interval=$2
    local timestamp_file="$TIMESTAMP_DIR/${section}_last_run"

    if [ ! -f "$timestamp_file" ]; then
        return 0
    fi

    last_run=$(cat "$timestamp_file")
    current_time=$(date +%s)
    time_diff=$((current_time - last_run))

    if [ $time_diff -ge $interval ]; then
        return 0
    else
        return 1
    fi
}

# Problem: How do we ensure our project always has the latest dependencies?
# Solution: Create a function to update dependencies using 'uv'
function update_dependencies() {
    curl -LsSf https://astral.sh/uv/install.sh | sh
    uv venv .venv
    uv pip install -r requirements.txt
}

# Problem: How do we record when a task was last run?
# Solution: Create a function to update the timestamp for a section
function update_timestamp() {
    local section=$1
    local timestamp_file="$TIMESTAMP_DIR/${section}_last_run"
    date +%s > "$timestamp_file"
}

# Problem: How do we handle tasks that should run every 1 second?
# Solution: Create a function for 1-second interval tasks
function section_1() {
    local section="EXAMPLE PROJECT: section_1"
    local interval=1  # 1 second

    if should_run "$section" $interval; then
        echo "Running $section..."
        uv run python main_1_secs.py
        echo "Section 1 completed."
        update_timestamp "$section"
    else
        echo "Skipping $section, not enough time has passed."
    fi
}

# Problem: How do we manage tasks that need to run every 5 seconds?
# Solution: Create a function for 5-second interval tasks
function section_0() {
    local section="EXAMPLE PROJECT: section_0"
    local interval=5  # 5 seconds

    if should_run "$section" $interval; then
        echo "Running $section..."
        uv run python main_pipeline_setup.py
        uv run python main_5_secs.py
        echo "Section 0 completed."
        update_timestamp "$section"
    else
        echo "Skipping $section, not enough time has passed."
    fi
}

# Problem: What about tasks that need to run hourly?
# Solution: Create a function for hourly tasks
function section_2() {
    local section="EXAMPLE PROJECT: section_2"
    local interval=3600  # 1 hour

    if should_run "$section" $interval; then
        echo "Running $section..."
        uv run python main_1_hour.py
        echo "Section 2 completed."
        update_timestamp "$section"
    else
        echo "Skipping $section, not enough time has passed."
    fi
}

# Problem: How do we manage daily tasks and ensure dependencies are up to date?
# Solution: Create a function for daily tasks that also updates dependencies
function section_3() {
    local section="EXAMPLE PROJECT: section_3"
    local interval=86400  # 1 day

    if should_run "$section" $interval; then
        echo "Running $section..."
        uv run python main_1_day.py
        update_dependencies
        echo "Section 3 completed."
        update_timestamp "$section"
    else
        echo "Skipping $section, not enough time has passed."
    fi
}

# Problem: How do we ensure all our tasks are executed in the correct order?
# Solution: Call all section functions in the desired sequence
section_0
section_1
section_2
section_3

# Congratulations! You've reached the end of the run.sh script.
# This script solves the complex problem of managing multiple tasks
# with different execution intervals in a SyftBox application.

# To customize this for your own project:
# 1. Identify the different intervals at which your tasks need to run
# 2. Create or modify sections for each interval
# 3. Replace the Python script calls with your own task scripts
# 4. Adjust the update_dependencies function if needed

# Remember: This script is typically called by a cron job frequently.
# The 'should_run' function ensures each section only runs when appropriate,
# solving the problem of over-execution.

# Next Steps:
# - Explore main_pipeline_setup.py to understand pipeline folder creation