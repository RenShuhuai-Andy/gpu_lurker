import requests
from .gpustat import GPUStatCollection
from apscheduler.schedulers.blocking import BlockingScheduler
import json
import time
import argparse
import os
import re

parser = argparse.ArgumentParser(description='check if gpu is available and notify on your WeChat')
# config args
parser.add_argument('-m', '--cuda-memory', type=float, default=5000, help='Required CUDA memory per device')
parser.add_argument('-n', '--device-num', type=int, default=1, help='Required number of devices')
parser.add_argument('-f', '--check-freq', type=str, default='10m', help='Frequency of inspection, eg. 10m (10 minutes)')
parser.add_argument('-r', '--reload', default=False, action='store_true',
                    help='Reload and update your appToken and uid')
parser.add_argument('-c', '--continuous', default=False, action='store_true',
                    help='Continue to push message when the conditions are met')
parser.add_argument('--log_file', type=str, default="gpu.log", help='define the threshold of available (in MB)')

args = parser.parse_args()

f = open(args.log_file, 'w+')
os.stdout = f
os.stderr = f

appToken = ""
uid = ""

empty_card = []

scheduler = BlockingScheduler()

time_parser = []
for type in ['d', 'h', 'm', 's']:
    value = re.findall(r'\d+(?=%s)' % type, args.check_freq)
    value = int(value[0]) if len(value) > 0 else 0
    time_parser.append(value)


# check the GPU every 30 min
@scheduler.scheduled_job('interval', days=time_parser[0], hours=time_parser[1], minutes=time_parser[2],
                         seconds=time_parser[3])
def job():
    gpu_stats = GPUStatCollection.new_query()
    current_time = time.strftime('%Y/%m/%d %H:%M')
    print("Check GPU at {}".format(current_time), flush=True)
    for i in gpu_stats.gpus:
        if i.memory_free >= args.cuda_memory:
            if i.index not in empty_card:
                empty_card.append(i.index)
        else:
            if i.index in empty_card:
                empty_card.remove(i.index)
    print("The GPU ids that meets the conditions are {}".format(empty_card), flush=True)

    if len(empty_card) >= args.device_num:
        current_time = time.strftime('%Y/%m/%d %H:%M')
        print("Send to WeChat at {}".format(current_time), flush=True)
        push_to_wechat(gpu_stats)
        if not args.continuous:
            scheduler.shutdown(wait=False)


def push_to_wechat(gpu_stats):
    s = f'gpu stats: \n\n'
    for i in gpu_stats.gpus:
        s += f'gpu {i.index}: | memory used {i.memory_used}/{i.memory_total} | users: '
        for p in i.processes:
            username = p['username']
            mem = p['gpu_memory_usage']
            s += f'{username} use {mem}|'
        s += '\n\n'
    sc_res_raw = requests.post(
        f'http://wxpusher.zjiecode.com/api/send/message',
        json={
            "appToken": appToken,
            'summary': f'满足条件的GPU是{empty_card}',
            'content': f'{s}',
            "contentType": 1,
            "uids": [uid]
        }
    )

    try:
        return_json = json.loads(sc_res_raw.text)
    except:
        raise RuntimeError(f'WxPusher 的返回值不能解析为 JSON，可能您的 appToken 或 uid 配置有误'
                           f'API 的返回是：\n{sc_res_raw}\n您输入的 appToken 为\n{appToken}\n您输入的 uid 为\n{uid}')
    success = return_json.get('success')

    if success is not True:
        raise RuntimeError(
            f'WxPusher调用失败，可能您的 appToken 或 uid 配置有误。API 的返回是：\n{sc_res_raw}\n'
            f'您输入的 appToken 为\n{appToken}\n您输入的 uid 为\n{uid}')


def main():
    global appToken, uid
    if args.reload or not os.path.exists('user.log'):
        appToken = input("Input your appToken: ")
        uid = input("Input your uid: ")
        with open('user.log', 'w', encoding='utf-8') as f:
            f.write(appToken + '\n' + uid)
    else:
        with open('user.log', 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            appToken = lines[0]
            uid = lines[1]
    print('-' * 10 + ' Start lurking ' + '-' * 10)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == "__main__":
    main()
