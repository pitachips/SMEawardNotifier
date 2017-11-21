
import requests
from bs4 import BeautifulSoup
import os
import telegram
from settings import TOKEN


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

bot = telegram.Bot(token=TOKEN)
chat_id = bot.getUpdates()[-1].message.chat.id
chat_text = bot.getUpdates()[-1].message.text

req = requests.get(
	'http://www.smtech.go.kr/front/ifg/no/notice02_intro.do?buclYy=')
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


def notify(content, filename):
	try:
		with open(os.path.join(BASE_DIR, filename), 'r') as f1:
			before = f1.read()
			if before != content:
				bot.sendMessage(chat_id=chat_id,
					text= filename + ' changed' + '\n' + content)
			else:
				bot.sendMessage(chat_id=chat_id,
					text= filename + ' unchanged' + '\n' + content)
	except FileNotFoundError :
		bot.sendMessage(chat_id=chat_id,
			text=filename + 'will be created with the following content'
			+ '\n' + content)

	with open(os.path.join(BASE_DIR, filename), 'w') as f2:
		f2.write(str_upcoming)


notify(str_ongoing, "latest_ongoing.txt")
notify(str_upcoming, "latest_upcoming.txt")