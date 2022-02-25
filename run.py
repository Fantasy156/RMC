from platform import machine, python_version
from sys import exit
from local.main import run

if python_version() < '3.10':
    exit('需要python版本大于或等于3.10')

if machine() == 'x86_64':
    target = 'PC'
    run(target)

elif machine() == 'aarch64' or machine() in 'arm*':
    target = 'AARCH64'
    run(target)

else:
    exit(f'暂不支持 {machine()}')
