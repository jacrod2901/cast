import smtplib

gmail_user = "jacrod2901@gmail.com"
gmail_password = "Big@data10"

sent_from_user = gmail_user
to = "jaitssat@gmail.com"
subject = "Cowin Appointment Availability Alert"
subject_test = 'TEST_EMAIL'
email_text = 'TEST EMAIL'


try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 534)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print ('Email sent!')
except Exception as e:
    print(e)
    print ('Something went wrong...')
