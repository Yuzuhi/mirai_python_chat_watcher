from modles.params import Params


def get_dota2_record_by_qq():
    # 1 获取qq号
    x = Params.qq_id
    print(x)
    # 2 根据qq号去数据库取出对应的数据
    # 3 调用sendGroupMessage接口发送数据
    pass

if __name__ == '__main__':
    get_dota2_record_by_qq()