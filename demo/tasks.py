from main.message.handler import CommandHandler
from main.mirai import MiraiBot
from modles.messages import GroupMessage

import time


async def get_dota2_record_by_qq(group_message):
    # 1 获取qq号
    x = group_message.sender.id
    print(x)
    # 2 根据qq号去数据库取出对应的数据
    # 3 调用sendGroupMessage接口发送数据
    return "成功"


if __name__ == '__main__':
    # 实例化
    handler = MiraiBot("1", 1, "1", 1)

    group_message = handler.get_group_message()
    # 加载命令和func
    handler.add_commands("哈哈", "123", get_dota2_record_by_qq, params=group_message)
    # 开启任务循环
    handler.listen()

    def listen(get_new_msg,self.command,params):
        while True:
            msg = get_new_msg.pop()
            if msg.text == command:
                command[command].func(msg, *params)