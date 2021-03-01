import re
from datetime import datetime
from typing import List
import nmap3
import requests
from service import config


def get_time() -> str:
    """

    """
    now = datetime.now()
    date_time = now.strftime("%d.%m.%Y %H:%M:%S")
    return date_time


def get_hosts(host: str) -> str:
    """

    """
    try:
        clients_list = []
        hd_scan = nmap3.NmapHostDiscovery()
        result = hd_scan.nmap_no_portscan(host)
        for res in result:
            check_ip = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", res)
            if check_ip:
                ip = check_ip.group()
                clients_list.append(ip)
    except Exception as e:
        print(f'error {e}')
        clients_list = []
    record_result(data=clients_list)
    return "success"


def record_result(data: List):
    """

    """
    try:
        for host_discovery in data:
            data_ip = requests.post(config.Config.API_DATABASE + '/get_one', json={"data": {"ip": host_discovery},
                                                                     "base": "host_discovery", "collection": "result"})
            data_ip = data_ip.json()
            if len(data_ip['data']) == 0:
                requests.post(config.Config.API_DATABASE + '/insert',
                              json={"data": {"ip": host_discovery, "tag": "None", "time": get_time()},
                                    "base": "host_discovery", "collection": "result"})
                requests.post(config.Config.API_DATABASE + '/insert',
                              json={"data": {"time": get_time(), "message": f"New IP: {host_discovery}"},
                                    "base": "notification", "collection": "notifications"})
                # telegram_message(message)
            else:
                requests.post(config.Config.API_DATABASE + '/upsert',
                              json={"data": {"name": {"ip": host_discovery}, "set": {"time": get_time()}},
                                    "base": "host_discovery", "collection": "result"})
    except Exception as e:
        print(f'error {e}')
