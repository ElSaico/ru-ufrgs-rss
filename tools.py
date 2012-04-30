# coding: utf-8
import os
import urllib2
from datetime import date, datetime
from bs4 import BeautifulSoup
from PyRSS2Gen import RSS2, RSSItem, Guid

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/ru')
def ru_ufrgs():
	WEEK_DAYS = ('Segunda-feira', 'Terça-feira', 'Quarta-feira',
	             'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo')
	week_day = date.today().weekday()
	resource = urllib2.urlopen("http://www.ufrgs.br/ufrgs/ru")
	page = BeautifulSoup(resource)
	for day in page.find_all("div", "dia"):
		day_name = day.h3.contents[0]
		if day_name == WEEK_DAYS[week_day]:
			desc = ', '.join([item.strip() for item in day.div.contents if not hasattr(item, 'contents')])
			feed = RSS2(
				title=u"Cardápio do RU-UFRGS - diário",
				link='http://www.ufrgs.br/ufrgs/ru',
				description=u"Cardápio do dia no Restaurante Universitário da UFRGS",
				pubDate=datetime.today(),
				items=[RSSItem(
					title = '%s (%s)' % (day_name, date.today().strftime('%d/%m/%Y')),
					link='http://www.ufrgs.br/ufrgs/ru',
					description=desc,
					guid=Guid(date.today().isoformat()),
				)]
			)
			return feed.to_xml()

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)
