import logging
import os

from email_handler import EmailHandler
import config

# 先判断文件是否存在,不存在则创建
if not os.path.exists(os.path.dirname(config.LOGGING["FILE"])):
    os.mkdir(os.path.dirname(config.LOGGING["FILE"]))
log_format = "[%(asctime)s] - %(name)s - [%(levelname)s] - %(message)s"
logging.basicConfig(filename=config.LOGGING["FILE"], filemode='a+', level=logging.ERROR, format=log_format)
logger = logging.getLogger("load")


# def log_handler(func):
#     with open(config.LOGGING["FILE"], 'r+') as rf:
#         count = len(rf.readlines())
#         if count >= 50:
#             EmailHandler().send_email()
#             rf.seek(0)
#             rf.truncate()
#
#     def inner(*args, **kwargs):
#         func(*args, **kwargs)
#         nonlocal count
#         count += 1
#
#     return inner

# @log_handler
# def write_log(msg):
#     logger.error(msg)

def show_errors():
    with open(config.LOGGING["FILE"], 'r+') as rf:
        str_line = ''
        for line in rf.readlines():
            str_line += line
        rf.seek(0)
        rf.truncate()
        return str_line

def write_log(msg):
    logger.error(msg)
