import subprocess

# Port number to search for
port = "1080"

# Get the output of the "ufw status" command
output = subprocess.run(["ufw", "status", "numbered"], capture_output=True, text=True)

# Search for the rule with port 1080
for line in output.stdout.split("\n"):
   print(f"{line.split(' ')[0]} - {line.split(' ')[1]}")
