import subprocess

scripts = [
"helllp.py"
]

processes = []

# Run the scripts as separate subprocesses
for script in scripts:
    process = subprocess.Popen(["python3", script])
    processes.append(process)

# Wait for all subprocesses to complete
exit_statuses = [process.wait() for process in processes]

# Check the exit status of each script
for script, exit_status in zip(scripts, exit_statuses):
    if exit_status == 0:
        print(f"{script} ran successfully")
    else:
        print(f"{script} did not run successfully")
