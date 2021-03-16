# gpu_lurker

![Python 3.5+](https://img.shields.io/badge/Python-3.5%2B-brightgreen.svg)
![PyPI](https://img.shields.io/pypi/v/gpulurker?label=PyPI)
![status](https://img.shields.io/pypi/status/gpulurker)
![Top Language](https://img.shields.io/github/languages/top/RenShuhuai-Andy/gpu_lurker?label=Python)
![License](https://img.shields.io/github/license/RenShuhuai-Andy/gpu_lurker?label=License)

服务器 GPU 监控程序，当 GPU 属性满足预设条件时通过微信发送提示消息

## 安装

从 PyPI 上安装:

```bash
$ pip install --upgrade gpulurker
```

从 GitHub 上安装最新版本 (*推荐*):

```bash
$ pip install git+https://github.com/RenShuhuai-Andy/gpu_lurker.git#egg=gpulurker
```

或克隆该仓库手动安装:

```bash
$ git clone --depth=1 https://github.com/RenShuhuai-Andy/gpu_lurker.git
$ cd gpulurker
$ pip install .
```

## 使用

#### 示例

```bash
# 每隔 30 分钟检查服务器状态，当有 8 张卡，每张卡的显存多余 1000M 时，向微信发送提示消息
$ gpulurker -m 1000 -n 8 -f '*|*|*/30'
```

#### 主要参数

- `-m`, `--cuda-memory`: 每张卡所需的显存
- `-n`, `--device-num`: 所需的 GPU 数
- `-f`, `--check-freq`: 检查服务器状态的间隔时间
- `-r`, `--reload`: 重新输入用户信息

键入 `ctrl+c` 终止监控。

键入 `gpulurker --help` 以获得更多信息:


## Screenshots

## 致谢
本项目参考了以下仓库的代码：

- [check_gpu_usage_and_forward_wechat](https://github.com/mzy97/check_gpu_usage_and_forward_wechat)
- [nvitop](https://github.com/XuehaiPan/nvitop)

## 许可证

GNU General Public License, version 3 (GPLv3)