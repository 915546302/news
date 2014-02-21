import platform
import urllib2,sys
import os
from PyQt4.QtWebKit import *  
from PyQt4.QtCore import *  
from PyQt4.QtGui import * 
import time
class News(object):
	
	def __init__(self):
		self.names={
		'cnblogs':'http://news.cnblogs.com',
		'oschina':'http://www.oschina.net'
	}
	def web(self,host):
		return self.names[host]
	def __news(self,name,url,tag,key):
		html=None
		try:
			request = urllib2.Request(url)
			request.add_header('User-Agent', 'Mozilla/5.0 '+
				'(Windows NT 6.1; WOW64) AppleWebKit/537.36'+
				' (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')
			fd = urllib2.urlopen(request)
			html=fd.read()
			fd.close()
		except urllib2.HTTPError, e:
			return []
		parsed_html=BeautifulSoup(html)
		aUrl=parsed_html.findAll(tag,key)
		top=[]
		lis=None
		if len(aUrl)>=10:
			lis=10
		else:
			lis=len(aUrl)
		for i in range(lis):
			a=aUrl[i].findChild('a')
			top.append(a)
		return top
	def cnblogs(self):
		return self.__news('cnblogs',self.names['cnblogs'],\
			'h2',{'class':'news_entry'})
	def oschina(self):
		
		return self.__news('oschina',self.names['oschina'],\
			'li',{'class':'today'})
class Review(object):
	def __init__(self,url):
		self.url=url.replace('http//www.oschina.net','')
		request = urllib2.Request(self.url)
		request.add_header('User-Agent', 'Mozilla/5.0 '+
			'(Windows NT 6.1; WOW64) AppleWebKit/537.36'+
			' (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36')
		fd = urllib2.urlopen(request)
		self.html=fd.read()
		fd.close()
	def getHtml(self):
		content=BeautifulSoup(self.html)
		if 'cnblogs' in self.url:
			div=content.find('div',{'id':'news_body'})
			self.html='<html><head>\
				</head><body bgcolor=\"#e3e3e3\"><div><p>'+unicode(div)+'<p></div></body></html>'
		elif 'oschina' in self.url:
			div=content.find('div',{'class':'Body'})
			if not div:
				div=content.find('div',{'class':'NewsEntity'})
			self.html='<html><head>\
				</head><body bgcolor=\"#e3e3e3\"><div>'+unicode(div)+'</div></body></html>'
		return self.html#unicode(self.html,'utf-8')
class Read(QDialog):
	def __init__(self,parent=None):
		QDialog.__init__(self)
		#self.setWindowFlags(w.windowFlags()&~Qt.WindowContextHelpButtonHint)
		self.setWindowTitle('Content')
		self.setWindowIcon(QIcon('news.png'))
		self.webview=QWebView(self)
		self.resize(600,810)
		self.setFixedWidth(600)
	def load(self,url):
		rev=Review(unicode(url.toString()))
		self.webview.setHtml(rev.getHtml())
		self.webview.resize(600,800)
class WebView(QWebView):
	DATA=None
	def __init__(self,parent=None):
		QWebView.__init__(self,parent)
		#self.setContextMenuPolicy(Qt.CustomContextMenu);
		self.currenturl=None
		self.data=None
		self.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
		self.connect(self, SIGNAL('loadFinished(bool)'),self,SLOT('finished(bool)'))
		self.connect(self,SIGNAL('loadProgress(int)'),self,SLOT('progress(int)'))

		self.connect(self,SIGNAL('linkClicked(const QUrl&)'),self.geturl)
	def geturl(self,u):
		subweb=Read()
		subweb.load(u)
		subweb.exec_()
	@pyqtSlot(bool)
	def finished(self,t):
		#mf=self.page().mainFrame()
		# self.currenturl=self.page()
		# self.currenturl.setViewportSize(QSize(350,790))
		# image=QImage(self.currenturl.viewportSize(), QImage.Format_ARGB32)
		# painter=QPainter(image)
		# self.currenturl.mainFrame().render(painter)
		# painter.end()
		# thu=image.scaled(400,800)
		# print time.ctime().split()[3]
		# timecs=time.ctime().split()[3]
		# savefile="page"+str(timecs)+".png"
		# thu.save(savefile)
		pass
	@pyqtSlot(int)
	def progress(self,p):
		pass


class Web(QWidget):
	def __init__(self):
		QWidget.__init__(self)
	
		home=QPushButton("Home")
		back=QPushButton("Back")
		home.setStyleSheet("color: red;")
		hbox = QHBoxLayout()
		# hbox.addWidget(home)
		hbox.addSpacing(270)
		hbox.addWidget(home)

		self.webview=WebView(self)
		data=self.reload()
		self.webview.setHtml(data)
		WebView.DATA=data
		vbox = QVBoxLayout()
		vbox.addLayout(hbox)
		vbox.addWidget(self.webview)
		self.setLayout(vbox)

		self.setWindowTitle('News')
		self.setWindowIcon(QIcon('news.png'))
		self.resize(350,800)
		self.setFixedWidth(350)
		
		self.connect(home,SIGNAL('clicked()'),\
			self,SLOT("back()"))
		self.connect(self,SIGNAL('loadFinished (bool)'),\
			self,SLOT('loaded(bool)'))
	@pyqtSlot()
	def back(self):
		data=self.reload()
		self.webview.setHtml(data)
		WebView.DATA=data
	@pyqtSlot(bool)
	def loaded(self,t):
		print t


	def reload(self):
		new=News()
		#view=open('index.html','w+')
		view='<html><head><title>News</title> \
			 <style type=\"text/css\"> \
			 body{background-color: #efefef;} \
			 a:link {color: blue;} \
			 a:active:{color: red; }\
			 </style> \
			</head><body><div id=\"cnblogs\">'
		view+='<ol>'
		view+='<h2>Cnblogs</h2>'
		for cn in new.cnblogs():
			src=cn.text
			u= cn.attrs['href']

			view+='<li><a href=\"'+new.web('cnblogs')+u+'\">'+src+'</a></li>'
		view+='</ol><ol>'
		view+='<h2>Oschina</h2>'
		for osc in new.oschina():
			u=new.web('oschina')+osc.attrs['href']
			view+='<li><a href=\"'+u+'\">'+osc.text+'</a></li>'
		view+='</ol>'
		view+='</div></body></html>'
		return view
if __name__=='__main__':
	if 'Windows' in platform.architecture()[1]:
		from bs4 import BeautifulSoup
	else:
		from BeautifulSoup import BeautifulSoup
	app = QApplication(sys.argv)
	web=Web()
	web.show()
	sys.exit(app.exec_())
