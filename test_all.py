import lib
import server_lookup
import argparse
import os
import sys
import pytest
import logging
logger = logging.getLogger(__name__)

def mock_ips():
    return [
        '192.168.1.1',
        '192.168.1.2',
        '192.168.1.3',
        '192.168.1.4',
        '192.168.1.5',
        '192.168.1.6',
        '192.168.1.7',
    ]

def mock_get_server_info(ip):
    key = int(ip.split('.')[-1])
    if key % 4 == 0:
        service = 'AService'
    elif key % 4 == 1:
        service = 'BService'
    elif key % 4 == 2:
        service = 'CService'
    elif key % 4 == 3:
        service = 'DService'
    return {
        'cpu': f'{key}1%',
        'service': service,
        'memory': f'{key}2%'
    }

def cpx_api_mock(mocker):
    m1 = mocker.patch("lib.cpx_api.CpxApi.get_servers_list", return_value=mock_ips())
    m2 = mocker.patch("lib.cpx_api.CpxApi.get_server_info", side_effect=mock_get_server_info)
    return m1, m2

def test_prepare_data_from_cpx(mocker):
    m1, m2 = cpx_api_mock(mocker)
    result_by_ip = {
        '192.168.1.1': {'cpu': '11%', 'service': 'BService', 'memory': '12%'},
        '192.168.1.2': {'cpu': '21%', 'service': 'CService', 'memory': '22%'},
        '192.168.1.3': {'cpu': '31%', 'service': 'DService', 'memory': '32%'},
        '192.168.1.4': {'cpu': '41%', 'service': 'AService', 'memory': '42%'},
        '192.168.1.5': {'cpu': '51%', 'service': 'BService', 'memory': '52%'},
        '192.168.1.6': {'cpu': '61%', 'service': 'CService', 'memory': '62%'},
        '192.168.1.7': {'cpu': '71%', 'service': 'DService', 'memory': '72%'},
    }

    result_by_service = {
        'BService': {'ips': ['192.168.1.1', '192.168.1.5'], 'count': 2, 'status': 'Healthy'},
        'CService': {'ips': ['192.168.1.2', '192.168.1.6'], 'count': 2, 'status': 'Healthy'},
        'DService': {'ips': ['192.168.1.3', '192.168.1.7'], 'count': 2, 'status': 'Healthy'},
        'AService': {'ips': ['192.168.1.4'],                'count': 1, 'status': 'Unhealthy'},
    }

    cpx = lib.cpx_api.CpxApi()
    info = cpx.get_all_data()
    # logger.info(info)
    assert m1.call_count == 1
    assert m2.call_count == 7
    m2.assert_has_calls([
        mocker.call('192.168.1.1'),
        mocker.call('192.168.1.2'),
        mocker.call('192.168.1.3'),
        mocker.call('192.168.1.4'),
        mocker.call('192.168.1.5'),
        mocker.call('192.168.1.6'),
        mocker.call('192.168.1.7'),
    ])
    assert info == (result_by_ip, result_by_service)

def test_server_lookup_byServer(mocker, capsys):
    cpx_api_mock(mocker)
    mocker.patch("server_lookup.parse_args", return_value=argparse.Namespace(byServer=True, byService=False, watch=False))
    server_lookup.main()
    out, err = capsys.readouterr()
    logger.info(out)
    assert err is ''
    assert out == '\n'.join([
        '             IP             Service         Status            CPU         Memory',
        '----------------------------------------------------------------------------------------------------',
        '    192.168.1.1            BService        Healthy            11%            12%',
        '    192.168.1.2            CService        Healthy            21%            22%',
        '    192.168.1.3            DService        Healthy            31%            32%',
        '    192.168.1.4            AService      Unhealthy            41%            42%',
        '    192.168.1.5            BService        Healthy            51%            52%',
        '    192.168.1.6            CService        Healthy            61%            62%',
        '    192.168.1.7            DService        Healthy            71%            72%',
    ]) + '\n\n'

def test_server_lookup_byService(mocker, capsys):
    cpx_api_mock(mocker)
    mocker.patch("server_lookup.parse_args", return_value=argparse.Namespace(byServer=False, byService=True, watch=False))
    server_lookup.main()
    out, err = capsys.readouterr()
    logger.info(out)
    assert err is ''
    assert out == '\n'.join([
        '             Service         Status          Count',
        '----------------------------------------------------------------------------------------------------',
        '            BService        Healthy              2',
        '            CService        Healthy              2',
        '            DService        Healthy              2',
        '            AService      Unhealthy              1',
    ]) + '\n\n'

def test_server_lookup_ip(mocker, capsys):
    cpx_api_mock(mocker)
    mocker.patch("server_lookup.parse_args", return_value=argparse.Namespace(byServer=False, byService=False, ip='192.168.1.7', service=None, watch=False))
    server_lookup.main()
    out, err = capsys.readouterr()
    logger.info(out)
    assert err is ''
    assert out == '\n'.join([
        '             IP             Service         Status            CPU         Memory',
        '----------------------------------------------------------------------------------------------------',
        '    192.168.1.7            DService        Healthy            71%            72%',
    ]) + '\n\n'

def test_server_lookup_service(mocker, capsys):
    cpx_api_mock(mocker)
    mocker.patch("server_lookup.parse_args", return_value=argparse.Namespace(byServer=False, byService=False, ip=None, service='BService', watch=False))
    server_lookup.main()
    out, err = capsys.readouterr()
    logger.info(out)
    assert err is ''
    assert out == '\n'.join([
        '             Service         Status          Count',
        '----------------------------------------------------------------------------------------------------',
        '            BService        Healthy              2',
        '',
        '      Member Servers:',
        '                  IP            CPU         Memory',
        '         192.168.1.1            11%            12%',
        '         192.168.1.5            51%            52%',
    ]) + '\n\n'
