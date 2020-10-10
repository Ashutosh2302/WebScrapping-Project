import speech_recognition as sr
from bs4 import BeautifulSoup
import requests
import smtplib
import csv
from email.message import EmailMessage
urls={
        'laptops':'https://www.did.ie/laptops-notebooks' , 'mobiles':'https://www.did.ie/catalogsearch/result/where/q/mobile+phones/Trigger/ac' ,
        'earphones':'https://www.did.ie/catalogsearch/result/where/q/earphones/Trigger/ac' , 'microwaves':'https://www.did.ie/microwaves'
      }
details=[]
product ='none'
user=input('Please enter your name')
receiver=input("Please enter your email")


#Code for speech recognition
r=sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    print('Speak: ')
    audio=r.listen(source)
    try:
       text=r.recognize_google(audio)
       print(f"You said: {text}")
    except Exception as e:
       print('Error: '+str(e))

for word in text.split(' '):
    for value in urls:
            if word==value:
                product=word
print(f'searching for {product}')
if(product!='none'):
    source=requests.get(urls[product]).text
    soup=BeautifulSoup(source,'lxml')
    data=soup.find_all('li',class_='item')
    for item in data:
        try:
            desc = item.find('h2', class_='product-name').a.text
            price=item.find('span',class_='price').text
            link=item.find('h2', class_='product-name').a['href']
        except:
            price='none'
        item = [
            desc, price, link
        ]
        details.append(item)
    initials = ['Description', 'Price', 'Link']
    with open('products.csv', 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(initials)
        for entry in details:
            csv_writer.writerow(entry)
    sender = 'demo.acct34@gmail.com'
    password = 'demo321@'
    msg = EmailMessage()

    msg['Subject'] = f'{product} details'
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content(f'Hi {user}\n\nPlease find the details of the product you searched, in the attachment below')
    file=['products.csv']

    with open('products.csv','rb') as f:
        file_data=f.read()
        file_name=f.name

    msg.add_attachment(file_data,maintype='application',subtype='octet-stream',filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

    print(f'Email sent at {receiver}')
else:
    print('Product not found')

