import re
import os


def read_comics_txt(path):
    with open(path, "r", encoding="utf-8") as rf:
        data = rf.read()
        clean_data = eval(data)
        return clean_data


def read_chapter_txt(path):
    with open(path, "r", encoding="utf-8") as rf:
        data = rf.read()
        data_list = re.findall("(\d+\.)(?P<pk>.*)", data)
        data_dict = {}
        for i in data_list:
            data_dict[i[0].strip(".")] = i[1]
        return data_dict


def count_dir(path):
    count = 0
    sub_name_list = os.listdir(path)
    for i in sub_name_list:
        if os.path.isdir(os.path.join(path, i)):
            count += 1
    return count


def create_price_list(price_dict, chap_list, default_price):
    d = price_dict
    _d = {}
    _v = []
    q = {}
    for k, v in d.items():
        for i in v:
            _d[i] = k
            _v.append(i)
    for j in chap_list:
        if str(j) in _v:
            q[str(j)] = _d[str(j)]
        else:
            q[str(j)] = default_price if default_price else "0.19"
    return q


def data_change(data):
    v_l = []
    for i in data:
        k, v = zip(*i.items())
        v_l.append(v)
    return k, v_l
