
import requests
from bs4 import BeautifulSoup
import os
import telegram
from settings.py import TOKEN


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

bot = telegram.Bot(token=TOKEN)
chat_id = bot.getUpdates()[-1].message.chat.id
chat_text = bot.getUpdates()[-1].message.text

req = requests.get('http://www.smtech.go.kr/front/ifg/no/notice02_intro.do?buclYy=')
html = req.text
soup = BeautifulSoup(html, 'html.parser')

ongoing = soup.select(
	'td.ac > a > img[src="../../images/common/icon03.gif"]'
	)
upcoming = soup.select(
	'td.ac > a > img[src="../../images/common/icon05.gif"]'
	)

str_ongoing = ''
for on in ongoing:
	str_ongoing += on.get('alt') + '\n'

str_upcoming = ''
for up in upcoming:
	str_upcoming += up.get('alt') + '\n'


try:
	with open(os.path.join(BASE_DIR, 'latest_ongoing.txt'), 'r') as f1:
		before = f1.read()
		if before != str_ongoing:
			bot.sendMessage(chat_id=chat_id, text='ongoing changed' + '\n' + str_ongoing)
		else:
			bot.sendMessage(chat_id=chat_id, text='ongoing unchanged' + '\n' + str_ongoing)
		f1.close()
except FileNotFoundError :
	bot.sendMessage(chat_id=chat_id, text='ongoing' + '\n' + str_ongoing)


with open(os.path.join(BASE_DIR, 'latest_ongoing.txt'), 'w') as f2:
	f2.write(str_ongoing)
	f2.close()


try:
	with open(os.path.join(BASE_DIR, 'latest_upcoming.txt'), 'r') as f3:
		before = f3.read()
		if before != str_upcoming:
			bot.sendMessage(chat_id=chat_id, text='upcoming changed' + '\n' + str_upcoming)
		else:
			bot.sendMessage(chat_id=chat_id, text='upcoming unchanged' + '\n' + str_upcoming)
		f3.close()
except FileNotFoundError :
	bot.sendMessage(chat_id=chat_id, text='upcoming' + '\n' + str_upcoming)


with open(os.path.join(BASE_DIR, 'latest_upcoming.txt'), 'w') as f4:
	f4.write(str_upcoming)
	f4.close()

