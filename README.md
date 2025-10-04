Python File Integrity Monitor
This is a lightweight, command-line tool built with Python to monitor and verify the integrity of files within a specified directory. It's designed to help you detect unauthorized or unexpected changes, ensuring that your critical system files, project code, or important documents remain unaltered.

How It Works
The tool operates on a simple yet effective principle:

Create a Baseline: The script first scans a target directory and all its subdirectories. It calculates a unique SHA-256 hash for every file and stores this information in a baseline.txt file. This baseline acts as a trusted "snapshot" of your files in their known-good state.

Verify Integrity: At any later time, you can run the script in verification mode. It re-scans the directory, calculates new hashes for all current files, and compares them against the stored baseline.

The script then generates a concise report that clearly identifies:

🚨 MODIFIED files whose contents have changed.

✨ NEW files that have been added.

🗑️ DELETED files that have been removed.

This tool is perfect for system administrators, developers, or anyone who needs a simple way to monitor critical directories for changes.
