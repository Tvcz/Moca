import smtplib

mail = smtplib.SMTP('smtp.gmail.com', 587)
mail.starttls()
mail.login("awesomejh79@gmail.com", "altarserver")

email = """From: Mr. Vargas \nTo: You \nMIME-Version: 1.0\nContent-type: text/html\n
<h1>herro</h1><h6>dere<h1>
<img width=100% src=https://northridgeprep.org/wp-content/uploads/2018/08/5E6A4799.jpg>
"""
n = 1000
friends = ["duhmoney12@gmail.com", "joncpater@gmail.com", "pieinyourface6@gmail.com"]
#for friend in friends:
for number in range(n):
		mail.sendmail("awesomejh79@gmail.com", "pieinyourface6@gmail.com", email)
mail.quit()
quit()