import subprocess

# Port number to search for
port = "1080"

# Get the output of the "ufw status" command
output = subprocess.run(["ufw", "status", "numbered"], capture_output=True, text=True)

# Search for the rule with port 1080
for line in output.stdout.split("\n"):
    if port in line:
        rule_number = line.split()[0]
        rule_status = line.split()[1]
        if rule_status == "allow":
            # Delete the rule
            subprocess.run(["ufw", "delete", rule_number])
            print(f"Rule {rule_number} containing port {port} was deleted.")
        else:
            print(f"Rule {rule_number} containing port {port} is not 'allow'.")