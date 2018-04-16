"""
数据处理
"""


def cut_list_by_key(items, key):
    """
    把数组按照{}里的关键字分成多个数组
    [{},{},{}]
    :param items:
    :param key:
    :return:
    """
    key_list = []
    for item in items:
        if item[key] not in key_list:
            key_list.append(item[key])
    pass
