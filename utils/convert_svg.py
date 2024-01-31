import os

## find all svg files under /resources/icon


files = os.listdir("../resources/icon")

for f in files:
    if f.endswith("_white.svg"):
        with open(f"../resources/icon/{f}", "r") as f:
            lines = f.readlines()
            for i in range(len(lines)):
                if lines[i].startswith("    <path"):
                    lines[i] = lines[i].replace("white", "black")
