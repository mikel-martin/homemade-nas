## How to start the application

1. Create virtual environment

```
python3 -m venv .venv
```

2. Activate the virtual environment

```
source .venv/bin/activate
```

3. Install required libraries

```
cd /path/to/project
pip install -r ./requirements.txt
```

4. Start web server 

```
flask --app . run --debug
```

Open http://127.0.0.1:5000 in your browser
