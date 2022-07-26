#!/usr/bin/env python3

import argparse
import sys
import time
from lib.cpx_api import CpxApi
from lib.pad import Pad

split_line = '-' * 100 + '\n'
server_title_line = '%15s%20s%15s%15s%15s\n' % ('IP', 'Service', 'Status', 'CPU', 'Memory')
service_title_line = '%20s%15s%15s\n' % ('Service', 'Status', 'Count')
cpx = CpxApi()

def server_line(ip, service, status, cpu, memory):
    return '%15s%20s%15s%15s%15s\n' % (ip, service, status, cpu, memory)

def service_line(service, status, count):
    return '%20s%15s%15s\n' % (service, status, count)

def generate_contents(args):
    contents = []
    result_by_ip, result_by_service = cpx.get_all_data()
    if args.byServer:
        contents.append(server_title_line)
        contents.append(split_line)
        for ip, v in result_by_ip.items():
            contents.append(server_line(ip, v['service'], result_by_service[v['service']]['status'], v['cpu'], v['memory']))
    elif args.byService:
        contents.append(service_title_line)
        contents.append(split_line)
        for service, v in result_by_service.items():
            contents.append(service_line(service, v['status'], v['count']))
    elif args.ip:
        ip = args.ip
        if not result_by_ip.get(ip):
            print('your input IP invalid.')
            sys.exit(1)
        server_info = result_by_ip[ip]
        contents.append(server_title_line)
        contents.append(split_line)
        contents.append(server_line(ip, server_info['service'], result_by_service[server_info['service']]['status'], server_info['cpu'], server_info['memory']))
    elif args.service:
        if not result_by_service.get(args.service):
            print('your input IP invalid.')
            sys.exit(1)
        service_info = result_by_service[args.service]
        contents.append(service_title_line)
        contents.append(split_line)
        contents.append(service_line(args.service, service_info['status'], service_info['count']))
    return contents

def data_refresh(args, pad):
    contents = generate_contents(args)
    pad.fill_in(contents)
    pad.refresh()

def data_print(args):
    contents = generate_contents(args)
    print(''.join(contents))

def parse_args():
    parser = argparse.ArgumentParser(description='check servers/services status')
    parser.add_argument('-s', '--byServer', help='check per server', action='store_true', default=False)
    parser.add_argument('-v', '--byService', help='check per service', action='store_true', default=False)
    parser.add_argument('--ip', help='which server want to check, input IP', type=str)
    parser.add_argument('--service', help='which service want to check, input service name', type=str)
    parser.add_argument('-w', '--watch', help='watch mode', action='store_true', default=False)
    return parser.parse_args()

def main():
    args = parse_args()

    if not (args.byServer or args.byService or args.ip or args.service):
        parser.print_help()
        sys.exit(1)

    if not args.watch:
        data_print(args)
    else:
        pad = Pad()
        watch_mode = True
        auto_update = True
        data_refresh(args, pad)
        while watch_mode:
            try:
                ch = pad.getch()
                if ch < 256 and ch > 0:
                    auto_update = False
                    if chr(ch) == 'j' and pad.pad_pos < pad.pad.getyx()[0] - pad.scr_height/2:
                        pad.pad_pos += 1
                        pad.refresh()
                    elif chr(ch) == 'k' and pad.pad_pos >= 0:
                        pad.pad_pos -= 1
                        pad.refresh()
                    elif chr(ch) == 'q':
                        pad.release()
                        watch_mode = False
                    elif chr(ch) == 'r':
                        data_refresh(args, pad)
            except KeyboardInterrupt:
                pad.release()
                watch_mode = False
            except ValueError:
                pass
                # in 5 seconds didn't getch() timeout
                # auto_update still true, automatically request to api to update
            finally:
                if auto_update: data_refresh(args, pad)


if __name__ == '__main__':
    main()
