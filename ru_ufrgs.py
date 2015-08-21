# coding: utf-8
import os
import urllib2
from datetime import date, datetime
from bs4 import BeautifulSoup
from PyRSS2Gen import RSS2, RSSItem, Guid

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/ru')
def menu():
	resource = urllib2.urlopen("http://www.ufrgs.br/ufrgs/ru")
	page = BeautifulSoup(resource)
	items = []
	for ru in page.find_all("div", "ru"):
		ru_name = ru.h3.contents[0]
		desc = ', '.join([(item or '').strip() for item in ru.div.contents if not hasattr(item, 'contents')])
		items.append(RSSItem(
			title = '%s - %s' % (ru_name, date.today().strftime('%d/%m/%Y')),
			link='http://www.ufrgs.br/ufrgs/ru',
			description=desc,
			guid=Guid(ru_name+date.today().isoformat()),
		))
	feed = RSS2(
		title=u"Cardápio do RU-UFRGS - diário",
		link='http://www.ufrgs.br/ufrgs/ru',
		description=u"Cardápio do dia no Restaurante Universitário da UFRGS",
		pubDate=datetime.today(),
		items=items,
	)
	return feed.to_xml()

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
