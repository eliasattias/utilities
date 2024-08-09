# %%
import logging
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
class EmailUtils:
    """
    Class for email utility functions.
    """

    logger = logging.getLogger(os.getenv('LOG_ENV'))

    def __init__(self,server_address,smtp_port):
        """Initialize the logger for EmailUtils"""
        self.session = smtplib.SMTP(server_address, smtp_port)

    def send_email(self, subject, sender_address, receiver_address, receiver_address_Cc, template, placeholders=None, attachment_path=None):
        """
        Send an email with dynamic content based on a template.

        Parameters:
        - subject: Subject of the email
        - template: Template string with placeholders for dynamic content (e.g., '{content}', '{link}')
        - placeholders: Dictionary containing key-value pairs for filling in placeholders in the template
        - sender_address: Sender's email address
        - receiver_address: List of recipient email addresses
        - receiver_address_Cc: List of CC recipient email addresses
        - attachment_path: Optional file path of attachment
        
        Returns:
        - None
        """
        
        # Create the email message with HTML content
        message = MIMEMultipart("alternative")
        message["From"] = sender_address
        message["To"] = ",".join(receiver_address)
        message["Cc"] = ",".join(receiver_address_Cc)
        message["Subject"] = subject

        # Create the HTML content
        if not placeholders:
            placeholders = {}
        html_content = template.format(**placeholders)

        # Attach the HTML content as a MIMEText object
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)

        if attachment_path:
            # Attach the file as a MIMEApplication object
            attachment_name = os.path.basename(attachment_path)
            with open(attachment_path, "rb") as file:
                attachment = MIMEApplication(file.read(), _subtype="pdf")  # Change the subtype accordingly
                attachment.add_header("Content-Disposition", f"attachment; filename={attachment_name}")
                message.attach(attachment)

        text = message.as_string()
        toaddr = receiver_address_Cc + receiver_address
        self.session.sendmail(sender_address, toaddr, text)
        EmailUtils.logger.info("Mail Sent")
    
    def close_session(self):
        """Close the SMTP session."""
        self.session.quit()

