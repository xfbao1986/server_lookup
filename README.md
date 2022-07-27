# package install
```
pip install -r requirements.txt
```

# how to run
   * start cpx_server in first terminal tab
   ```
   python cpx_server.py --protocol 4 8080
   ```

   * use server_lookup.py cmd in another terminal tab
   * show help
   ```
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

   ```

   * display all status per server (one-time)
   ```
   python ./server_lookup.py -s
   ```

   * display all status per server (watch mode)
   ```
   python ./server_lookup.py -s -w
   ```

   * display all status per service (one-time)
   ```
   python ./server_lookup.py -v
   ```

   * display all status per server (watch mode)
   ```
   python ./server_lookup.py -v -w
   ```

   * display server status by ip (one-time)
   ```
   python ./server_lookup.py --ip <IP>
   ```

   * display server status by ip (watch mode)
   ```
   python ./server_lookup.py --ip <IP> -w
   ```

   * display service status by name (one-time)
   ```
   python ./server_lookup.py --service <NAME>
   ```

   * display service status by name (watch)
   ```
   python ./server_lookup.py --service <NAME> -w
   ```

# option explaination
   1. in watch mode, when you didn't input anything, will automatically update per 5 seconds.
   2. in watch mode, when you press any key. the auto update will stop.
   3. in watch mode, press 'q' or 'ctrl+c', will quit
   4. in watch mode, press 'j' will scroll down, press 'k' will scroll up.

# example show
[![demo](https://img.youtube.com/vi/-0HSnVVS_g8/maxresdefault.jpg)](https://youtu.be/-0HSnVVS_g8)

# unit test
   * mock cpx_server response
   * 5 unit test
      1. test data aggregate
      2. test server_lookup.py -s
      3. test server_lookup.py -v
      4. test server_lookup.py --ip 192.168.1.7
      5. test server_lookup.py --service BService

   * how to run: execute pytest in the root dir
   ```
   $ pytest
   =========================================================================================== test session starts ============================================================================================
   platform darwin -- Python 3.8.12, pytest-7.1.2, pluggy-1.0.0
   rootdir: /Users/xiaofei.bao/SRE_take_home_challenge, configfile: pyproject.toml
   plugins: mock-3.8.2
   collected 5 items
   
   test_all.py::test_prepare_data_from_cpx PASSED                                                                                                                                                       [ 20%]
   test_all.py::test_server_lookup_byServer
   ---------------------------------------------------------------------------------------------- live log call -----------------------------------------------------------------------------------------------
   2022-07-27 02:40:51 [    INFO]              IP             Service         Status            CPU         Memory
   ----------------------------------------------------------------------------------------------------
       192.168.1.1            BService        Healthy            11%            12%
       192.168.1.2            CService        Healthy            21%            22%
       192.168.1.3            DService        Healthy            31%            32%
       192.168.1.4            AService      Unhealthy            41%            42%
       192.168.1.5            BService        Healthy            51%            52%
       192.168.1.6            CService        Healthy            61%            62%
       192.168.1.7            DService        Healthy            71%            72%
   
    (test_all.py:82)
   PASSED                                                                                                                                                                                               [ 40%]
   test_all.py::test_server_lookup_byService
   ---------------------------------------------------------------------------------------------- live log call -----------------------------------------------------------------------------------------------
   2022-07-27 02:40:51 [    INFO]              Service         Status          Count
   ----------------------------------------------------------------------------------------------------
               BService        Healthy              2
               CService        Healthy              2
               DService        Healthy              2
               AService      Unhealthy              1
   
    (test_all.py:101)
   PASSED                                                                                                                                                                                               [ 60%]
   test_all.py::test_server_lookup_ip
   ---------------------------------------------------------------------------------------------- live log call -----------------------------------------------------------------------------------------------
   2022-07-27 02:40:51 [    INFO]              IP             Service         Status            CPU         Memory
   ----------------------------------------------------------------------------------------------------
       192.168.1.7            DService        Healthy            71%            72%
   
    (test_all.py:117)
   PASSED                                                                                                                                                                                               [ 80%]
   test_all.py::test_server_lookup_service
   ---------------------------------------------------------------------------------------------- live log call -----------------------------------------------------------------------------------------------
   2022-07-27 02:40:51 [    INFO]              Service         Status          Count
   ----------------------------------------------------------------------------------------------------
               BService        Healthy              2
   
    (test_all.py:130)
   PASSED                                                                                                                                                                                               [100%]
   
   ============================================================================================ 5 passed in 0.22s =============================================================================================
   ```

# summary
   > I developed some similar tool(ruby version) for checking server status when I was in previous company. So basical feature I finished smoothly. We can get info based on server, or based on service. The watch mode (continuous tracing info & update on screen) took me some time. I searched and found curses (Terminal handling for display), which solved the problem.

# furture improvement
   * we can add more metrics, for example: now only CPU/Memory utilization percentage displayed for server, we can show CPU/Memory detail. (of course, depends on cpx api can provide or not)
   * make the display result more user friendly, for example: if CPU/Memory utilization percentage over 70%, display in RED. if service status is Unhealthly, display in RED.
   * create test case for watch mode
      * if nothing press
        - test output on screen will update every 5 seconds.
        - test cpx api call will happen every 5 seconds.
      * if press 'j' 'k', output on screen will scroll down or up

