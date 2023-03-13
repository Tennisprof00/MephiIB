import os
import argparse
import requests
import json

# Функция сканирования хостов по сети
def do_ping_sweep(ip, num_of_host):
    ip_parts = ip.split('.')
    network_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'
    scanned_ip = network_ip + str(int(ip_parts[3]) + num_of_host)
    response = os.popen(f'ping -c 1 {scanned_ip}')
    res = response.readlines()
    print(f"[#] Result of scanning: {scanned_ip} [#]\n{res[2]}", end='\n\n')

# Функция отправки GET или POST запросов
def sent_http_request(target, method, headers=None, payload=None):
    headers_dict = dict()
    if headers:
        for header in headers:
            header_name = header.split(':')[0]
            header_value = header.split(':')[1:]
            headers_dict[header_name] = ':'.join(header_value)
    if method == "GET":
        response = requests.get(target, headers=headers_dict)
    elif method == "POST":
        response = requests.post(target, headers=headers_dict, data=payload)
    print(
        f"[#] Response status code: {response.status_code}\n"
        f"[#] Response headers: {json.dumps(dict(response.headers), indent=4, sort_keys=True)}\n"
        f"[#] Response content: \n {response.text}"
    )

# Парсим аргументы
parser = argparse.ArgumentParser(description='Сетевой сканер')
parser.add_argument('task', choices=['scan', 'httpsend'], help='Сканирование сети или отправка HTTP запросов')
parser.add_argument('-i', '--ip', type=str, help='IP адрес первого хоста')
parser.add_argument('-n', '--num_of_hosts', type=int, help='Сколько хостов сканируем')
parser.add_argument('-t', '--target', type=str, help='Куда обращаемся по HTTP')
parser.add_argument('-m', '--method', choices=['GET', 'POST'], help='Какой используем метод Get или Post')
parser.add_argument('-hd', '--headers', nargs='*', type=str, help='Какие смотрим заголовки')
parser.add_argument('-p', '--payload', type=str, help='Какие смотрим заголовки')
args = parser.parse_args()

# Выполняем скрипт в зависмости от выбора пользователя
if args.task == 'scan':
    for host_num in range(args.num_of_hosts):
        do_ping_sweep(args.ip, host_num)
else:
    sent_http_request(args.target, args.method, args.headers, args.payload)
