# socrates experiment
ai for teachers & students

## How to run

0. Install environment (UV)
1. Activate environment
2. Run the following commands*

    ulimit -n 20000
    streamlit run main.py

OR with load balancer (install nginx & start)
move `nginx.conf` to /opt/homebrew/etc/nginx/nginx.conf
    ./start_workers.sh
    brew services restart nginx
Get your ip 
    ipconfig getifaddr en0
Others can access though your ip in local network

## TODO
- MAYBE add text badinter check & file

GPT Suggestion for open files error
*👉 Quick fix for testing with your 150 students:
    Before running streamlit run app.py, run
    ulimit -n 20000


## Options

- Host on web
- Tunnel 
