import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Union, List


class GmailNotification:
    def __init__(self, user_mail: Optional[str], user_password: Optional[str]) -> None:
        """
        Initializes an smtp session to gmail

        A user mail and password must be provided unless configured in the system's environment variables

        :user_mail: - str
            The email which will send the email
        
        :user_password: - str
            The password for the email which will send the mail
        
        
        """
        self.sender_password: str = user_password
        self.sender_mail: str = user_mail

        self.session = smtplib.SMTP('smtp.gmail.com', 587)
        self.session.starttls()
        self.session.login(
            user=os.environ.get("SENDER_MAIL", self.sender_mail),
            password=os.environ.get("SENDER_PASSWORD", self.sender_password)
        ) 

    def notify(self, alert: str, subject: str, receiver_mails: Union[List[str], str]):
        """
        Send a notification to the receiver emails listed a notification string

        :alert: - str
            The email's body which will be sent in mail

        :subject: - str
            The email's subject/title which will be sent in mail

        :receiver_mails: Union[List[str], str]
            Either a list of receiver emails or a single mail
        
        """
        if isinstance(receiver_mails, list):
            if not all(isinstance(mail, str) for mail in receiver_mails):
                raise TypeError("All values of receiver mails must be of type `str`")

        message = MIMEMultipart()
        message['To'] = ', '.join(receiver_mails) if isinstance(receiver_mails, list) else receiver_mails
        message['From'] = self.sender_mail
        message['Subject'] = subject
        message.attach(MIMEText(alert, 'plain'))
        text = message.as_string()
        self.session.sendmail(self.sender_mail, receiver_mails, text)
