import smtplib

EMAIL = "info.youthversity@gmail.com"
# CAUTION: Please enter the password before using!
PASSWORD = ""


def serverStatus(text):
    """
    Send the given status text to our internal email.
    """
    mail(EMAIL, text)


def mail(recipient, text):
    """
    Send out an an email to the given recipient with the given text.
    """
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, recipient, text)
    server.quit()
