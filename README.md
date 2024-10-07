# Example Project Tutorial

Welcome to the Example Project tutorial! This project demonstrates several key features and best practices for creating a SyftBox application. Throughout this tutorial, we'll explore various aspects of the project structure and functionality.

## How to Customize This Project For Your Own Application

First, begin reading through the "Project Overview", and this will end up taking
you through all the various files and what they do. Then come back here. At that point, you'll likely want to customize your project in the following way:

0. Change the name of the folder to be something other than "example_project". The app looks to this folder to know how to name itself.
1. Create a github repo and put your example project into it. This is going to make syncing your code across multiple test datasites a little bit easier (see Development Tips for more here)
2. Edit the pipeline_folders.txt file to define your desired folder structure and permissions.
3. Edit the requirements.txt file to add any additional dependencies your project needs.
4. Edit the main_1_day.py file to add any additional functionality you want to run once a day.
5. Edit the main_1_hour.py file to add any additional functionality you want to run once an hour.
6. Edit the main_5_mins.py file to add any additional functionality you want to run every 5 minutes.
7. Edit the main_5_secs.py file to add any additional functionality you want to run every 5 seconds.
8. Store your project in a GitHub repository and start sharing it with users! (likely for them to add to their github_app_updater/github_apps.csv file).
9. Drag your folder into the "apps" folder to see it run! (you can also do this earlier if you want it to run during the dev process... which can be chaotic but also can be helpful).
10. (Optional) You might want to create a website (.html file) in <your datasite>/public which helps to raise awareness about your app for others to use.
11. (Optional) If you think your app might be useful for everyone, you might consider
submitting a pull request to the github_app_updater project to have your app added
to the list of default apps!

Happy broad listening!

## Development Tips
- Load your project into the "apps" folder from the beginning so you can see how it regularly behaves (while you code).
- Whenever you want your main_5_mins.py (or some other file) to run, you can either:
  - open a command line to the root of the example_project and run ```uv run python main_5_mins.py```
  - delete the corresponding timestamp folder from ```example_project/script_timestamps```
- Login with multiple datasites so you can see how multi-user interactions work (pro tip: build with a friend over zoom)
- To help make syncing your code across multiple datasites easier in the development process, load your code into a Github repo and then add that repo to ```apps/github_app_updater/github_apps.csv``` for all except the datasite you're actively developing in. That way, if you hit save, commit, and push — it'll automatically propagate the code changes to all of the other datasites you're testing with (especially helpful if you're testing with a friend over zoom).
- If you want to speed up your dev cycles even more, you can launch your own test network locally (although I personally don't recommend this. I think it's best to test on the actual network if you can).

## Project Overview

The Example Project showcases:

1. Regular execution via a cron job
2. Dependency management in a virtual environment
3. Pipeline folder structure initialization
4. Background tasks running at specified intervals

## Getting Started

Let's begin by examining the main components of this project:

### 1. Run Script

The `run.sh` file is the entry point of our application. It's called regularly by cron and manages the execution of various tasks at different intervals.

### 2. Dependency Management

We use a `requirements.txt` file to specify project dependencies. This ensures consistent environments across different setups.

### 3. Pipeline Folder Structure

The project initializes a specific folder structure for pipelines. This structure is defined in the `pipeline_folders.txt` file, which lists the folders to be created along with their permissions.

### 4. Background Tasks

Several Python scripts run at different intervals:

- `main_1_day.py`: Runs once a day
- `main_1_hour.py`: Runs once an hour
- `main_5_mins.py`: Runs every 5 minutes
- `main_5_secs.py`: Runs every 5 seconds

## Next Steps

To dive deeper into the project, let's start by examining the `run.sh` file. This script orchestrates the execution of various components at different intervals.

You can find the `run.sh` file in the root of the example_project folder. Open it and pay attention to how it manages different sections and their execution intervals.

After reviewing `run.sh`, we'll explore the pipeline setup in `main_pipeline_setup.py`.

Happy exploring!
