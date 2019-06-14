import telegram
import logging
import setting

logger = logging.getLogger('cgm')

def sendLatestEntry(db):
    try:
        r = db.getDisplayValues()
        if r['val'] == 0:
            return

        config = setting.getCurrent()
        
        bot = telegram.Bot(token = config['tg_bot_token'])
        updates = bot.getUpdates()

        chatId = config['tg_chat_id']        

        if len(updates) > 0:
            latest = updates[-1]    

            if latest.channel_post != None:
                chatId = latest.channel_post.chat.id
                setting.setTGChatId(chatId)
            elif latest.message != None:
                chatId = latest.message.chat.id
                setting.setTGChatId(chatId)

        m = int(r['elapsed'] / 60)

        msg = '혈당: {2}\n\n지난 시간: {0} 분\n변동량: {1}\n방향성: {3}'.format(m, r['delta'], r['val'], r['direction'])
        bot.sendMessage(chat_id = chatId, text = msg)
    
    except Exception as e:
        pass
        # logger.info(e)
    