import requests
import ipaddress

class CpxApi:
    def __servers_url(self):
        return 'http://localhost:8080/servers'

    def __server_info_url(self, ip):
        return f'http://localhost:8080/{ip}'

    def __get_response_json(self, url):
        return requests.get(url).json()

    def get_servers_list(self):
        ips = self.__get_response_json(self.__servers_url())
        ips = [ipaddress.ip_address(ip) for ip in ips]
        ips.sort()
        return [str(ip) for ip in ips]

    def get_server_info(self, ip):
         return self.__get_response_json(self.__server_info_url(ip))

    def get_all_data(self):
        ips = self.get_servers_list()
        result_by_ip = {}
        result_by_service = {}

        for ip in ips:
            server_info = self.get_server_info(ip)
            result_by_ip[ip] = server_info
            if result_by_service.get(server_info['service']):
                result_by_service[server_info['service']]['ips'].append(ip)
                result_by_service[server_info['service']]['count'] += 1
                result_by_service[server_info['service']]['status'] = 'Healthy'
            else:
                result_by_service[server_info['service']] = {'ips': [ip], 'count': 1, 'status': 'Unhealthy'}
        return result_by_ip, result_by_service

