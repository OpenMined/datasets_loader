# Welcome to main_pipeline_setup.py!
#
# This script is a crucial part of the Example Project, responsible for setting up
# the pipeline folder structure for your SyftBox application. It addresses several
# key challenges:
#
# 1. Creating a standardized folder structure for pipeline operations
# 2. Setting up proper permissions for each folder
# 3. Ensuring that the folder structure is created in the correct location
# 4. Allowing for easy customization of the folder structure and permissions
#
# As you've seen in run.sh, this script is typically executed every 5 seconds.
# However, it's designed to be idempotent, meaning it's safe to run multiple times
# without causing issues or duplicating work.
#
# Let's dive into how this script solves each of these challenges!

import os
import json
from syftbox.lib import ClientConfig
from pathlib import Path

# Problem: How do we dynamically determine the app name?
# Solution: Extract the app name from the current directory path
app_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

# Problem: How do we access the user's SyftBox configuration?
# Solution: Load the client configuration from a standard location
client_config = ClientConfig.load(
    os.path.expanduser("~/.syftbox/client_config.json")
)

# Problem: How do we define the structure and permissions for pipeline folders,
# while allowing comments in the configuration file?
# Solution: Read from pipeline_folders.txt, ignoring comments and empty lines
pipeline_folders = []
with open("pipeline_folders.txt", "r") as file:
    for line in file:
        # Remove leading/trailing whitespace and ignore comments
        line = line.strip()
        if line and not line.startswith("#"):
            parts = line.split(" ", 1)
            if len(parts) == 2:
                folder, perm_json = parts
                pipeline_folders.append((folder, json.loads(perm_json)))

# Problem: Where should we create the pipeline folders?
# Solution: Construct the path based on the client's email and app name
pipeline_path = (
    Path(os.path.abspath(__file__)).parent.parent.parent
    / client_config["email"]
    / "datasets"
)

# Problem: How do we create the pipeline folders with the correct permissions?
# Solution: Iterate through the defined folders and create them with proper permissions
for folder, perm_json in pipeline_folders:
    folder_path = pipeline_path / folder
    os.makedirs(folder_path, exist_ok=True)
    
    # Problem: How do we indicate that a folder has been created?
    # Solution: Create a dummy file in each folder
    with open(folder_path / ".dummy", "w") as f:
        pass
    
    # Problem: How do we set the correct permissions for each folder?
    # Solution: Create a _.syftperm file with the specified permissions
    perm_json["admin"] = [client_config["email"]]
    perm_json["read"] = [email if email != "me" else client_config["email"] for email in perm_json["read"]]
    perm_json["write"] = [email if email != "me" else client_config["email"] for email in perm_json["write"]]
    perm_json["filepath"] = str(folder_path / "_.syftperm")
    
    with open(folder_path / "_.syftperm", "w") as f:
        json.dump(perm_json, f, indent=2)

# Problem: How do we confirm that the setup was successful?
# Solution: Print a confirmation message with the pipeline path
print(f"Pipeline folders and _.syftperm files created in {pipeline_path}")

# Congratulations! You've completed the main_pipeline_setup.py script.
# This script solves the problem of creating a standardized folder structure
# for your SyftBox application, complete with proper permissions.

# Key points to remember:
# 1. The script uses the app name and client email to determine where to create folders.
# 2. Folder structure and permissions are defined in pipeline_folders.txt.
# 3. Each folder gets a _.syftperm file that defines its access permissions.
# 4. The "me" placeholder in permissions is replaced with the client's email.
# 5. Comments and empty lines in pipeline_folders.txt are now supported.

# To customize this for your own project:
# 1. Modify pipeline_folders.txt to define your desired folder structure and permissions.
# 2. Add comments to pipeline_folders.txt to explain your folder structure.
# 3. Adjust the pipeline_path construction if you need a different folder hierarchy.
# 4. Add any additional setup steps your project might require.

# Next steps:
# - Examine the contents of the created folders in your SyftBox directory.
# - Look at the _.syftperm files to understand the permission structure.
# - Consider how your application will use these pipeline folders.
# - Explore the main_5_secs.py, main_5_mins.py, main_1_hour.py, and main_1_day.py
#   files to see how they interact with this folder structure.
