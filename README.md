### ROVER LINUX

First configure the environment in the config/config.sh file.
/config/config.sh

Then export the config add to .bashrc:
```bash
source $HOME/Projects/rover-linux/config/config.sh
```

Create virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install requirements in the virtual environment:
```bash
pip install -r requirements.txt
```

Execute all scripts:
```bash
bash $PROJECT_ROOT/launcher/launcher.sh
```
