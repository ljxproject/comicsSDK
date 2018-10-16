import os
import shutil
import time
import sys

import config


def lcr(env_path, comics_resource_file):
    # 判断路径有没有对应env
    env_list = os.listdir(env_path)
    if "lcr_env" not in env_list:
        # 无则创建
        # 安装virtualenv包 && 进入env安装目录 && 安装虚拟环境
        re = os.system(
            r'pip install virtualenv && cd %s && virtualenv --python=python3 --no-site-packages lcr_env' % env_path)
        if not re == 0:
            return print("参数不正确")
    # 退出env && 使用env && 安装第三方包 && 运行comics_handle.py
    os.system(
        r'source %s/lcr_env/bin/activate &&'
        r' pip install -r %s/requirement.txt && python %s/comics_handler.py %s && deactivate' %
        (env_path, config.CURRENTPATH, config.CURRENTPATH, comics_resource_file))  # todo linux下语法
    return print("正在计算使用时间")


if __name__ == '__main__':

    try:
        start = time.time()
        env_path = sys.argv[1]
        comics_resource_file = sys.argv[2]
        lcr(env_path, comics_resource_file)
        file = os.path.basename(comics_resource_file)
        path = os.path.dirname(comics_resource_file)
        prefix = os.path.splitext(file)[0]
        shutil.rmtree(os.path.join(path, prefix))
        print("cost time %f" % (time.time() - start))
    except Exception as e:
        print(e)
