## How to start the application

This application must run on a Linux operating system.

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

![image](https://github.com/user-attachments/assets/c0ab5539-73bf-4393-9309-e62460b655cd)

![image](https://github.com/user-attachments/assets/37d40b25-40e3-4c87-9286-0c3046c260b0)
