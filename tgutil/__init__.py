import telegram
import logging
import setting

logger = logging.getLogger('cgm')

def sendLatestEntry(db):
    config = setting.getCurrent()
    
    bot = telegram.Bot(token = config['tg_bot_token'])
    updates = bot.getUpdates()
    if len(updates) == 0:
        return

    r = db.getDisplayValues()
    if r['val'] == 0:
        return

    latest = updates[-1]
    # logger.info(latest)
    
    if latest.channel_post != None:
        chatId = latest.channel_post.chat.id
    elif latest.message != None:
        chatId = latest.message.chat.id
    else:
        return

    m = int(r['elapsed'] / 60)

    msg = '혈당: {2}\n\n지난 시간: {0} 분\n변동량: {1}\n방향성: {3}'.format(m, r['delta'], r['val'], r['direction'])
    bot.sendMessage(chat_id = chatId, text = msg)
    