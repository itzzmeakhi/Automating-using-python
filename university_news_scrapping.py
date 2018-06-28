
""" Import webdriver from selenium """

from selenium import webdriver

import csv

import schedule

import time

from datetime import date

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

""" Import BeautifulSoup from bs4 """

from bs4 import BeautifulSoup

def daily_news():

	""" Load chrome webdriver """

	driver = webdriver.Chrome(executable_path = '/Users/akhilreddy/Downloads/chromedriver')

	""" Get the URL of page to be loaded """

	url = 'http://www.sathyabama.ac.in'

	""" Download the html page """

	driver.get(url)

	""" To retrieve the source of page loaded using webdriver """

	html_doc = driver.page_source

	""" Passing html_doc to BeautifulSoup to parse """

	soup = BeautifulSoup(html_doc, 'lxml')

	""" Organize html source """

	soup.prettify()

	""" Select by class """

	today = str(date.today())

	data_list = []

	class_select_data = soup.find('ul', class_ = 'latest_news')

	li_select_data = class_select_data.find_all('a')


	for list_data in li_select_data:

		data=[list_data.text, list_data['href']]

		data_list.append(data)

		with open ('news/' + today + '.csv','w') as file:

			writer = csv.writer(file)

			for row in data_list:

				writer.writerow(row)




	fromaddr = "akhilmallidi.98@gmail.com"
	toaddr = "akhilmallidi.98@gmail.com"

	# instance of MIMEMultipart
	msg = MIMEMultipart()

	# storing the senders email address  
	msg['From'] = fromaddr
	 
	# storing the receivers email address 
	msg['To'] = toaddr
	 
	# storing the subject 
	msg['Subject'] = "Subject of the Mail"
	 
	# string to store the body of the mail
	body = "Today's News published"

	# attach the body with the msg instance
	msg.attach(MIMEText(body, 'plain'))

	# open the file to be sent 
	filename = today + '.csv'
	attachment = open('news/' + today + '.csv', 'rb')
	 
	# instance of MIMEBase and named as p
	p = MIMEBase('application', 'octet-stream')
	 
	# To change the payload into encoded form
	p.set_payload((attachment).read())
	 
	# encode into base64
	encoders.encode_base64(p)
	  
	p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
	 
	# attach the instance 'p' to instance 'msg'
	msg.attach(p)
	 
	# creates SMTP session
	s = smtplib.SMTP('smtp.gmail.com', 587)
	 
	# start TLS for security
	s.starttls()
	 
	# Authentication
	s.login(fromaddr, "AkHiL777")
	 
	# Converts the Multipart msg into a string
	text = msg.as_string()
	 
	# sending the mail
	s.sendmail(fromaddr, toaddr, text)
	 
	# terminating the session
	s.quit()



schedule.every().day.at("23:17").do(daily_news)

while True:
	schedule.run_pending()
	time.sleep(1)










