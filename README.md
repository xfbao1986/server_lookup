# package install

```
pip install -r requirements.txt
```

# how to run

```
# start cpx_server
python cpx_server.py --protocol 4 8080

# show help
python ./server_lookup.py -h
usage: server_lookup.py [-h] [-s] [-i] [--ip IP] [--service SERVICE] [-w]

check servers/services status

optional arguments:
  -h, --help         show this help message and exit
  -s, --byServer     check per server
  -v, --byService    check per service
  --ip IP            which server want to check, input IP
  --service SERVICE  which service want to check, input service name
  -w, --watch        watch mode

# display all status per server (one-time)
python ./server_lookup.py -s

# display all status per server (watch mode)
python ./server_lookup.py -s -w

# display all status per service (one-time)
python ./server_lookup.py -v

# display all status per server (watch mode)
python ./server_lookup.py -v -w

# display server status by ip (one-time)
python ./server_lookup.py --ip <IP>

# display server status by ip (watch mode)
python ./server_lookup.py --ip <IP> -w

# display service status by name (one-time)
python ./server_lookup.py --service <NAME>

# display service status by name (one-time)
python ./server_lookup.py --service <NAME> -w
```

# tip
    1. in watch mode, when you didn't input anything, will automatically update per 5 seconds.
    2. in watch mode, when you press any key. the auto update will stop.
    3. in watch mode, press 'q' or 'ctrl+c', will quit
    4. in watch mode, press 'j' will scroll down, press 'k' will scroll up.

# demo
![demo](./demo.mov)

