from nonebot.plugin.on import on_message,on_notice
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    Message,
    MessageEvent,
    PokeNotifyEvent,
)
from .utils import *

# 优先级99, 条件: 艾特bot就触发
ai = on_message(rule=to_me(), priority=99,block=False)
# 优先级1, 不会向下阻断, 条件: 戳一戳bot触发
poke_ = on_notice(rule=to_me(),block=False)


@ai.handle()
async def _(event: MessageEvent):
    # 获取消息文本
    msg = str(event.get_message())
    # 去掉带中括号的内容(去除cq码)
    msg = re.sub(r"\[.*?\]", "", msg)

    # 如果是光艾特bot(没消息返回)或者打招呼的话,就回复以下内容
    if (not msg) or msg.isspace() or msg in hello__bot:
        await ai.finish(Message(random.choice(hello__reply)))

    # 获取用户nickname
    if isinstance(event, GroupMessageEvent):
        nickname = event.sender.card or event.sender.nickname
    else:
        nickname = event.sender.nickname

    # 从字典里获取结果
    result = await get_chat_result2(msg,  nickname)
    if result != None:
        await ai.finish(Message(result))
    else:
        result = await get_chat_result(msg,  nickname)# 从备用字典里获取结果
        if result != None:
            await ai.finish(Message(result))
        else:
            await ai.finish(Message(random.choice(cant__reply)))# 随机回复cant__reply的内容

@poke_.handle()
async def _poke_event(event: PokeNotifyEvent):
    if event.is_tome:        
        # 随机回复poke__reply的内容
        await poke_.send(Message(random.choice(poke__reply)))
