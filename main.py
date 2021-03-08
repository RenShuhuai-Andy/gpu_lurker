import requests
from gpustat import GPUStatCollection
from apscheduler.schedulers.blocking import BlockingScheduler
import json
import logging
import time
import argparse
import os

parser = argparse.ArgumentParser(description='check if gpu is avaliable and notify on your wechat')
# config args
parser.add_argument('--key_of_notify', type=str, required=True, help='server jam key')
parser.add_argument('--define_threshold', type=float, default=1000, help='define the threshold of avaliable (in MB)')
parser.add_argument('--check_freq', type=str, default='*|*|*/10', help='corntab format time, eg. (*|*|*/10)')
parser.add_argument('--log_file', type=str, default="gpu.log", help='define the threshold of avaliable (in MB)')

args = parser.parse_args()

f = open(args.log_file, 'w+')
os.stdout = f
os.stderr = f

sckey = args.key_of_notify
empty_card = []
flag = True  # 避免重复发送gpu推送

scheduler = BlockingScheduler()

time_parser = args.check_freq
time_parser = time_parser.split('|')


# check the GPU every 30 min
@scheduler.scheduled_job('cron', day=time_parser[0], hour=time_parser[1], minute=time_parser[2])
def job():
    global flag
    gpu_stats = GPUStatCollection.new_query()
    # logger.info("扫描GPU")
    current_time = time.strftime('%Y-%m-%d@%H-%M')
    print("check GPU at {}".format(current_time), flush=True)
    print("current empty gpu ids {}".format(empty_card), flush=True)
    for i in gpu_stats.gpus:
        if i.memory_used < args.define_threshold:
            if i.index not in empty_card:
                empty_card.append(i.index)
                flag = True
        else:
            if i.index in empty_card:
                empty_card.remove(i.index)
                flag = True

    if len(empty_card) != 0 and flag:
        current_time = time.strftime('%Y-%m-%d@%H-%M')
        print("send to wechat at {}".format(current_time), flush=True)
        push_to_wechat(gpu_stats)
        flag = False


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
        f'https://sc.ftqq.com/{sckey}.send',
        data={
            'text': f'空闲的GPU是{empty_card}',
            'desp': f'{s}',
        },
        timeout=1,
    )

    try:
        return_json = json.loads(sc_res_raw.text)
    except:
        raise RuntimeError(f'Server 酱的返回值不能解析为 JSON，可能您的 SCKEY 配置有误'
                           f'API 的返回是：\n{sc_res_raw}\n您输入的 SCKEY 为\n{sckey}')
    errno = return_json.get('errno')

    if errno != 0:
        raise RuntimeError(
            f'Server 酱调用失败，可能您的 SCKEY 配置有误。API 的返回是：\n{sc_res_raw}\n'
            f'您输入的 SCKEY 为\n{sckey}')


def main():
    scheduler.start()


if __name__ == "__main__":
    main()