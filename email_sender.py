'''
    Email sender
'''
def create_html_content(dataframe):
    # Get HTML from Dataframe

    # render dataframe as html
    return dataframe.to_html()


def send_email(dataframe):
    # Send email to myself of companies analyzied
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    sendFrom = 'ivan.barcia@gmail.com'
    password = 'Navi9300'
    server = 'smtp.gmail.com:587'
    sendTo = 'ivan.barcia@gmail.com'

    message = create_html_content(dataframe)
    
    text = "Hey you!\nHere you can find the companies to look at:\n"

    html = """\
    <html>
        <head>
        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 5px;
                text-align: left;    
            }    
        </style>
        </head>
    <body>
    <p>Companies:<br>
       <br>
       %s
    </p>
    </body>
    </html>
    """ % (message)
    
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    
    # Create the root message and fill in the from, to, and subject headers
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Companies - Fundamental analysis'
    msg['From'] = sendFrom 
    msg['To'] = sendTo
    msg.attach(part1)
    msg.attach(part2)
    
    server = smtplib.SMTP(server)
    server.ehlo()
    server.starttls()
    server.login(sendFrom, password)
    server.sendmail(sendFrom, sendTo, msg.as_string())
    server.quit()