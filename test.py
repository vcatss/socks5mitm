import subprocess
import re
# Port number to search for
port = "1080"

# Get the output of the "ufw status" command
output = subprocess.run(["ufw", "status", "numbered"], capture_output=True, text=True)

# Search for the rule with port 1080
for line in output.stdout.split("\n"):
    numbers = re.findall(r'\d+', line)
    if len(numbers) > 1:
        print(f"Rule number: {numbers[0]} : Port number: {numbers[1]}")