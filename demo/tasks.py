from main.message.handler import MessageHandler
from modles.messages import GroupMessage

import time


async def get_dota2_record_by_qq(group_message: GroupMessage, date):
    # 1 获取qq号
    x = group_message.sender.id
    print(x)
    # 2 根据qq号去数据库取出对应的数据
    # 3 调用sendGroupMessage接口发送数据
    return "成功"


if __name__ == '__main__':
    date = time.time()
    handler = MessageHandler("1", "1", "1", 1)

    handler.add_commands("哈哈", "123", get_dota2_record_by_qq, params=(GroupMessage,1))

    def listen(get_new_msg,self.command,params):
        while True:
            msg = get_new_msg.pop()
            if msg.text == command:
                command[command].func(msg, *params)