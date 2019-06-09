import telegram
import logging

logger = logging.getLogger('cgm')

TOKEN = '790737403:AAFRd5rwdyOA0wP6XOgBo50Zs_Ga70l0bu0'

def sendLatestEntry(db):
    bot = telegram.Bot(token = TOKEN)
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

    msg = '혈당: {2}\n\n지난 시간: {0} 분\n변동: {1}\n방향성: {3}'.format(m, r['delta'], r['val'], r['direction'])
    bot.sendMessage(chat_id = chatId, text = msg)
    