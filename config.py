import os

CURRENTPATH = os.path.dirname(os.path.abspath(__file__))
# PROJECTPATH = "/Users/grave/Desktop/work/comics"  # todo linux下项目目录
PROJECTPATH = "/home/ljx/opt/project/comics/comic"  # todo linux下项目目录

MYSQLDATABASES = {
    "host": 'localhost',
    "port": 3306,
    "user": 'root',
    "passwd": 'DingYu@906',
    # "passwd": 'root',
    "db": 'comics',
    "charset": 'utf8',
}

COMICSPATH = {
    "COMICSRESOURCE": r"%s/media/img" % PROJECTPATH  # 漫画资源绝对路径
}

LOGGING = {
    "FILE": r"%s/logs/load_error.log" % PROJECTPATH  # 漫画加载错误文件
}
