安装教程:
1: 手机安装原版Termux.apk 运行Termux 获取存储权限
软件下载地址(https://f-droid.org/zh_Hans/packages/com.termux/)

termux-setup-storage

2: 下载git、tar、proot【复制下面命令，在Termux中输入，回车】

pkg update
pkg install git tar proot wget -y

3:0下载ubuntu.tar.xz及安装脚本【复制下面命令，在Termux中输入，回车】

git clone https://gitee.com/sharpeter/proot-ubuntu --depth 1

bash proot-ubuntu/install_ubuntu.sh

4: 执行启动ubuntu 20.04【复制下面命令，在Termux中输入，回车】

ubuntu

执行第4条后进入ubuntu系统 【 PC版教程从此开始，手机端继续往下 】 【复制下面命令，终端中执行】

sudo apt update && sudo apt upgrade -y 【 必须执行 】

sudo apt install git pip openjdk-11-jre p7zip-full -y  && sudo apt pip install tqdm requests

解压此工具到 /data/data/com.termux/files/home/ubuntu/root 目录 解压到出来文件夹设置777权限(需要同时应用到子目录及文件)后执行此命令

cd RMC && python3 RMC.py