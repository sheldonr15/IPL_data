import os

with open(os.path.join("./", "Procfile"), "w") as f:
    line = "web: sh setup.sh && streamlit run run.py"
    f.write(line)
