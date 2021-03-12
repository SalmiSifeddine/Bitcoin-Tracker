from tkinter import *
from bs4 import BeautifulSoup
import urllib
from urllib import request
from datetime import datetime


#interface parameters
root = Tk()
root.title("Bitcoin Tracker")
root.geometry("550x200")
root.config(bg="black")

global previous
previous = False

#Get Current time
now = datetime.now()
Current_date_time = now.strftime("%I:%M:%S %p")

#Create a frame
my_frame = Frame(root, bg="black")
my_frame.pack(pady=20)

#bitcoin price label
bitcoin_label = Label(my_frame,
 	bg="black", 
 	text='', 
 	font=("Helvetika", 45), 
 	fg="green", 
 	bd=0)
bitcoin_label.grid(row=1, column=3, padx=20, sticky="s")

#price label
price_label = Label(my_frame,
	bg="black",
	text="",
	font=("Helvetika", 10),
	fg="red",
	bd=0)
price_label.grid(row=2, column=3,  sticky="n")

#Grabe the bitcoin Price
def Update():
	global previous

	try:
		#Grabing the price
		Page = urllib.request.urlopen("https://www.coindesk.com/price/bitcoin").read()
		#excepting errors
	except SSLError:
		print("check ur internet connection ...")

	html = BeautifulSoup(Page, "html.parser")
	price_large = html.find(class_="price-large")


	#convert to string
	price_large1 = str(price_large)

	#Grab the slice that contain the string
	price_large2 = price_large1[54:63]
	print("DONE !")	

	#Update our Bitcoin Label
	bitcoin_label.config(text=f"${price_large2}")

	#Updating each second
	root.after(30000, Update)

	# Update the status bar
	Status_bar.config(text=f'Last Updated: {Current_date_time}   ')

	#Determine Price Change
	#grab current price
	current = price_large2

	#Turrning into float
	current = current.replace(',', '')

	if previous:
		if float(previous) > float(current):
			price_label.config(
				text=f'Price Down ${round(float(previous) - float(current), 2)}', fg="red")
		elif float(previous) == float(current):
			price_label.config(text="Price Unchaged", fg="grey")

		else:
			price_label.config(
				text=f'Price Up ${round(float(current) - float(previous), 2)}', fg="green")
		
	else:
		previous = current
		price_label.config(text="Price Unchaged", fg="grey")

#Create Status Bar
Status_bar = Label(root, text=f'Last Updated: {Current_date_time}    ',
	bg="black", 
	fg="grey", 
	bd=0,
	anchor=E)
Status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#Call Update 
Update()
root.mainloop()