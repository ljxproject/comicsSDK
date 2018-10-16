import zipfile
import os
import time
import sys

import config
import log_handler
import mysql_handler
import txt_handler
from mysql_handler import MysqlHandler


class ComicsHandler(object):
    deep_list = []
    suspense_list = []
    exist_comics_list = []
    chap_dir_list = []
    table = "api_comicinfo"

    @classmethod
    def check_file(cls, directory):
        """
        检查file文件夹是否为空,名字
        :return:
        """
        sub_dir_name_list = os.listdir(directory)
        key_name_list = ["my", "en"]
        suffix_list = [".jpg"]
        for file_name in sub_dir_name_list:  # 其他语言
            suffix = os.path.split(file_name)[1]
            if suffix in suffix_list:
                cls.suspense_list.append(directory)
                return 3
        if len(sub_dir_name_list) <= 0:
            log_handler.write_log("%s文件夹为空" % directory)
            return 0
        if os.path.basename(directory) in key_name_list:
            cls.suspense_list.append(directory)
            return 1
        else:
            cls.deep_list.append(directory)
            return 2

    @classmethod
    def deep_recursive(cls):
        """
        深度递归
        :return:
        """
        if len(cls.deep_list):
            directory = cls.deep_list.pop(0)
            sub_dir_name_list = os.listdir(directory)
            for fileName in sub_dir_name_list:
                #        拼接目录
                abs_path = os.path.join(directory, fileName)
                if os.path.isdir(abs_path):  # 判断是否是一个目录
                    status = cls.check_file(abs_path)
                    if not status:
                        continue
                    cls.deep_recursive()
            print("%s目录已加载完成,接下来处理数据" % directory)

    @classmethod
    def unzip(cls, compress):
        # 解压
        target_path = os.path.dirname(compress)
        r = zipfile.is_zipfile(compress)
        if r:
            rz = zipfile.ZipFile(compress, "r")
            rz.extractall(path=target_path)
            directory = os.path.join(target_path, os.path.splitext(os.path.basename(compress))[0])
            target_dir = config.COMICSPATH["COMICSRESOURCE"]
            os.system("/bin/cp -rf %s/* %s" % (directory, target_dir))  # todo linux下命令不一样
            for f in os.listdir(directory):
                if f.startswith("."):
                    continue
                else:
                    return directory, target_dir
        else:
            raise ValueError("上传文件并非.zip格式")

    @classmethod
    def comics_handle(cls, compress):
        # 安装第三方库
        # 解压
        directory, target_dir = cls.unzip(compress)
        status = cls.check_file(directory)
        re = MysqlHandler().read_table(cls.table)
        for i in re:
            v = str(i["com_id"])
            cls.exist_comics_list.append(v)
        if not status:
            return print("Finish")
        elif status == 2:
            cls.deep_recursive()
            print("共有待处理合法资源文件夹: %d个 %s" % (len(cls.suspense_list), cls.suspense_list))
        cls.resource_handler(target_dir)

    @classmethod
    def resource_handler(cls, target_dir):
        # 从imgresource表中提取对应com_id的chap_id,形成字典
        check_com_id_list = list(set([os.path.basename(os.path.dirname(i)) for i in cls.suspense_list]))
        check_table = "api_imgresource"
        exist_chap_dict = {}
        for i in check_com_id_list:
            re = mysql_handler.MysqlHandler().read_table(check_table, "com_id=%s" % i)
            if not re:
                tmp_chap_list = []
            else:
                tmp_chap_list = [str(j["chap_id"]) for j in re]
            exist_chap_dict[i] = tmp_chap_list
        # 处理漫画每个语言
        while True:  #
            if len(cls.suspense_list):
                directory = cls.suspense_list.pop()
            else:
                print("全部数据以加载完成")
                break
            lang = os.path.basename(directory)
            com_id = os.path.basename(os.path.dirname(directory))
            if com_id in cls.exist_comics_list:
                is_exist = 1
            else:
                is_exist = 0
            # 提取文件
            sub_dir_name_list = os.listdir(directory)
            print("%s 语言子文件" % com_id, sub_dir_name_list)
            chap_cover_img_dict = {}
            necessary_file_list = ["comics_detail.txt", "com_cover_img.jpg",
                                   "chap_title_list.txt"]
            for file_name in sub_dir_name_list:
                if file_name == "comics_detail.txt":
                    necessary_file_list.remove(file_name)
                    data = txt_handler.read_comics_txt(os.path.join(directory, file_name))
                elif file_name == "com_cover_img.jpg":
                    necessary_file_list.remove(file_name)
                    com_cover_img = os.path.splitext(file_name)[0]
                elif file_name == "chap_title_list.txt":
                    necessary_file_list.remove(file_name)
                    chap_dict = txt_handler.read_chapter_txt(os.path.join(directory, file_name))
                elif os.path.isdir(os.path.join(directory, file_name)):
                    # cls.chap_dir_list.append(os.path.join(directory, file_name))
                    name_list = os.listdir(os.path.join(directory, file_name))
                    for fn in name_list:
                        if fn == "chap_cover_img.jpg":
                            chap_cover_img = fn
                            chap_cover_img_dict[file_name] = chap_cover_img
            # 是否有必须文件否则报错
            if necessary_file_list:
                #print(necessary_file_list)
                log_handler.write_log(
                    "%s缺少运行必须文件,例如:'comics_detail.txt', 'com_cover_img.jpg','chap_title_list.txt'" % com_id)
                continue
            # 统计该语言文件夹下有多少个文件夹
            c = txt_handler.count_dir(directory)
            chap_list = list(chap_dict.keys())
            if c != len(chap_list):
                log_handler.write_log("%s章节数与文件夹数不相等" % com_id)
                continue
            # api_imgresource
            exist_chap_list = exist_chap_dict[com_id]
            create_chap_list = list(set(chap_list).difference(set(exist_chap_list)))
            print(create_chap_list, "有效章节列表", len(chap_list))
            # 生成有效章节的价格列表
            data_price = data["chapter_list"][0].get("price", "")
            if data_price:
                suspense_price_dict = eval(data["chapter_list"][0]["price"])[0]
            else:
                suspense_price_dict = {}
            free_chap =[]
            for i in range(data["free_chapter"]):
                free_chap.append(str(i+1))
            suspense_price_dict["0.00"] = free_chap
            default_price = data["default_price"]
            create_price_dict = txt_handler.create_price_list(suspense_price_dict, create_chap_list, default_price)
            feed_i_data = []
            for i in create_chap_list:
                tmp = {"com_id": data["com_id"], "%s_title" % lang: chap_dict[i],
                       "chap_cover_img": chap_cover_img_dict.get(i, ""), "chap_id": int(i),
                       "%s_img_list_path" % lang: "%s/%s/%s" % (data["com_id"], lang, i),
                       "price": create_price_dict[i]
                       }
                feed_i_data.append(tmp)
            cls.comics_imgresource_handler(feed_i_data)

            # api_category
            feed_ca_data = [{"com_id": data["com_id"], "category": data["category"]}]
            cls.comics_category_handler(feed_ca_data, is_exist)
            # api_search
            feed_s_data = [{"com_id": data["com_id"], "%s_title" % lang: data["title"],
                            "%s_author" % lang: data["author"], "%s_subtitle" % lang: data["subtitle"],
                            "%s_introduction" % lang: data["introduction"]
                            }]
            cls.comics_search_handler(feed_s_data, is_exist)
            # api_cominfo
            feed_co_data = [{"com_id": data["com_id"],
                             "%s_com_cover_img" % lang: com_cover_img,
                             "free_chapter": data["free_chapter"],
                             "total_chapter": txt_handler.count_dir(target_dir + "/%s/%s" % (com_id, lang)),
                             "download": 0, "created": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time())),
                             "modified": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time())),
                             "status": data["status"], "category": data["category"]
                             }]
            cls.comics_info_handler(feed_co_data, is_exist)

    @classmethod
    def comics_info_handler(cls, feed_co_data, is_exist=None):
        table = "api_comicinfo"
        com_id = "com_id=%s" % feed_co_data[0]["com_id"]
        if is_exist:
            del_list = ["download", "created", "com_id"]
            for i in del_list:
                del feed_co_data[0][i]
            k, v_l = txt_handler.data_change(feed_co_data)
            msg = MysqlHandler().update_sql(table, k, v_l[0], com_id)
            if msg:
                log_handler.write_log("%s %s" % (table, msg) % com_id)
        else:
            k, v_l = txt_handler.data_change(feed_co_data)
            msg = MysqlHandler().create_sql(table, k, v_l)
            if msg:
                log_handler.write_log("%s %s" % (table, msg) % com_id)

    @classmethod
    def comics_category_handler(cls, feed_ca_data, is_exist=None):
        table = "api_category"
        com_id = "com_id=%s" % feed_ca_data[0]["com_id"]
        if not is_exist:
            k, v_l = txt_handler.data_change(feed_ca_data)
            msg = MysqlHandler().create_sql(table, k, v_l)
            if msg:
                log_handler.write_log("%s %s" % (table, msg) % com_id)
        else:
            del feed_ca_data[0]["com_id"]
            k, v_l = txt_handler.data_change(feed_ca_data)
            msg = MysqlHandler().update_sql(table, k, v_l[0], com_id)
            if msg:
                log_handler.write_log("%s %s" % (table, msg) % com_id)

    @classmethod
    def comics_search_handler(cls, feed_s_data, is_exist=None):
        table = "api_search"
        com_id = "com_id=%s" % feed_s_data[0]["com_id"]
        if not is_exist:
            k, v_l = txt_handler.data_change(feed_s_data)
            msg = MysqlHandler().create_sql(table, k, v_l)
            if msg:
                log_handler.write_log("%s %s" % (table, msg) % com_id)
        else:
            del feed_s_data[0]["com_id"]
            k, v_l = txt_handler.data_change(feed_s_data)
            msg = MysqlHandler().update_sql(table, k, v_l[0], com_id)
            if msg:
                log_handler.write_log("%s %s" % (table, msg) % com_id)

    @classmethod
    def comics_imgresource_handler(cls, feed_i_data):
        table = "api_imgresource"
        if feed_i_data:
            com_id = "com_id=%s" % feed_i_data[0]["com_id"]
            k, v_l = txt_handler.data_change(feed_i_data)
            msg = mysql_handler.MysqlHandler().create_sql(table, k, v_l)
            if msg:
                log_handler.write_log("%s %s" % (table, msg) % com_id)
        else:
            print("%s无需更新" % table)


if __name__ == '__main__':
    ComicsHandler.comics_handle(sys.argv[1])

