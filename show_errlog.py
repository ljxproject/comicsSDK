import log_handler


def show_errlog():
    res = log_handler.show_errors()
    print(res)


if __name__ == '__main__':
    show_errlog()
