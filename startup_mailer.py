__author__ = 'Cody Giles'
__license__ = "Creative Commons Attribution-ShareAlike 3.0 Unported License"
__version__ = "1.0"
__maintainer__ = "Cody Giles"
__status__ = "Production"

import subprocess
import smtplib
from email.mime.text import MIMEText
import datetime

def connect_type(word_list):
    """ This function takes a list of words, then, depeding which key word, returns the corresponding
    internet connection type as a string. ie) 'ethernet'.
    """
    if 'wlan0' in word_list or 'wlan1' in word_list:
        con_type = 'wifi'
    elif 'eth0' in word_list:
        con_type = 'ethernet'
    elif 'docker0' in word_list:
	con_type = 'docker'
    elif 'flannel0' in word_list:
	con_type = 'flanneld'
    else:
        con_type = 'current'

    return con_type

# Change to your own account information
# Account Information
to = 'rpinsl2050@gmail.com' # Email to send to.
gmail_user = 'rpinsl2050@gmail.com' # Email to send from. (MUST BE GMAIL)
gmail_password = 'nsl2050edison' # Gmail password.
smtpserver = smtplib.SMTP('smtp.gmail.com', 587) # Server to use.
arg = 'hostname'
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
hostname = p.communicate()[0]

smtpserver.ehlo()  # Says 'hello' to the server
smtpserver.starttls()  # Start TLS encryption
smtpserver.ehlo()
smtpserver.login(gmail_user, gmail_password)  # Log in to server
today = datetime.date.today()  # Get current time/date

arg='ip route list'  # Linux command to retrieve ip addresses.
# Runs 'arg' in a 'hidden terminal'.
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data = p.communicate()  # Get data from 'p terminal'.
ip_msg = ''
# Split IP text block into three, and divide the two containing IPs into words.
ip_lines = data[0].splitlines()
for line in ip_lines[1:]:
	split_line = line.split()
	ip_type = connect_type(split_line)

	ip_addr = split_line[split_line.index('src') + 1]
	ip_msg += 'Your %s ip is %s\n' % (ip_type, ip_addr)

msg = MIMEText(ip_msg)
msg['Subject'] = 'IPs For %s on %s' % (hostname, today.strftime('%b %d %Y'))
msg['From'] = gmail_user
msg['To'] = to
# Sends the message
smtpserver.sendmail(gmail_user, [to], msg.as_string())
# Closes the smtp server.
smtpserver.quit()
