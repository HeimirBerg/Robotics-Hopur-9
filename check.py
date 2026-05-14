import subprocess

result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
lines = result.stdout.split("\n")

print("=== Running Python processes ===")
for line in lines:
    if "python" in line.lower():
        print(line)