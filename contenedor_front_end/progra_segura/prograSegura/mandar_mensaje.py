import requests

def telegram_bot_sendtext(bot_message):
    
    bot_token = '1201671700:AAGvvO00k_rrVJiokhCJsL1SfmzY6BK578k'
    bot_chatID = '-417703328'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()
    

