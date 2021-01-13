import os
import time
import uuid
import click
import boto3
import datetime as dt
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from templates.email_templates import email_templates

def filter_templates(template_data, id):
    filtered = list(filter(lambda e: e.get('id') == id, template_data))
    return filtered

def generate_raw_email(SENDER, RECIPIENT, SUBJECT, ATTACHMENT, BODY_TEXT, BODY_HTML, CHARSET):
    # Create a multipart/mixed parent container.
    email = MIMEMultipart('mixed')
    # Add subject, from and to lines.
    email['Subject'] = SUBJECT 
    email['From'] = SENDER 
    email['To'] = RECIPIENT

    # Create a multipart/alternative child container.
    email_body = MIMEMultipart('alternative')

    # Encode the text and HTML content and set the character encoding. This step is
    # necessary if you're sending a message with characters outside the ASCII range.
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)

    # Add the text and HTML parts to the child container.
    email_body.attach(textpart)
    email_body.attach(htmlpart)

    # Define the attachment part and encode it using MIMEApplication.
    att = MIMEApplication(open(ATTACHMENT, 'rb').read())

    # Add a header to tell the email client to treat this part as an attachment,
    # and to give the attachment a name.
    att.add_header('Content-Disposition','attachment',filename=os.path.basename(ATTACHMENT))

    # Attach the multipart/alternative child container to the multipart/mixed
    # parent container.
    email.attach(email_body)

    # Add the attachment to the parent container.
    email.attach(att)

    return email

def send_raw_email(iterations, sleep_seconds, template):
    #Debug only:
    #print('Parameters: ', int(iterations), int(sleep_seconds))

    client = boto3.client('ses', region_name='eu-west-1')

    try:
        for i in range(int(iterations)):
            
            time.sleep(int(sleep_seconds))

            index = i + 1
            guid = uuid.uuid4()
            generated_template = generate_raw_email(
                                    SENDER = template.get('contents').get('SENDER'),
                                    RECIPIENT = template.get('contents').get('RECIPIENT'),
                                    SUBJECT = f"{template.get('contents').get('SUBJECT')} [Batch count: {index} of {iterations} | Time: {dt.datetime.now()} | UUID: {guid}]",
                                    ATTACHMENT = template.get('contents').get('ATTACHMENT'),
                                    BODY_TEXT = template.get('contents').get('BODY_TEXT'),
                                    BODY_HTML = template.get('contents').get('BODY_HTML'),
                                    CHARSET = template.get('contents').get('CHARSET')
                                ).as_string()


            send_res = client.send_raw_email(
                RawMessage={
                    'Data': generated_template
                }
            )

            print('\n', f'{send_res}\n')
            print(f'Email {index} successfully sent.')
            print(f'Script-generated email ref / UUID: {guid}')

    except ClientError as e:
        print(e.response['Error']['Message'])

    finally:
        print('\nScript finished.')

@click.command()
@click.option('--iterations', required=True, help="Number of email that will be sent.")
@click.option('--sleep-seconds', default=0, help="Time delay between sending emails.")
@click.option('--template-choice', required=True, help="Identifier of the email template chosen in email_templates.py.")
@click.option('--safeguard-limit', required=True)
def main(iterations, sleep_seconds, template_choice, safeguard_limit):
    
    if int(iterations) >= int(safeguard_limit):
        print(f"Looks like you tried to run {iterations} send iteratrions. At this time, you cannot run more than {safeguard_limit} send iterations of send email. Please raise a PR to have this reviewed and ammended.")
        exit()

    validated_template = None if not filter_templates(email_templates, int(template_choice)) else filter_templates(email_templates, int(template_choice))[0]
    if not validated_template:
        print("Looks like you chose an invalid template identifer. To fix this, either: \n\n(1) check that you passed in the desired email template identifier, as defined in email_attachments.py;\n(2) Submit a Pull Request to update the email_attachments.py file with the desired template identifer.")
        exit(1)
    else:
        print(f"You chose template with identifier ({validated_template.get('id')}):")
        
        send_raw_email(iterations, sleep_seconds, validated_template)
       
if __name__ == '__main__':
    main()