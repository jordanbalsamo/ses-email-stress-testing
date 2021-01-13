import datetime

email_templates = [
    {
        'id': 0, # Reserving this for testing code.
        'contents': {
            'SENDER': 'example@example.co.uk',
            'RECIPIENT': 'example@example.co.uk',
            'SUBJECT': f'Test Email',
            'ATTACHMENT': 'attachments/textfile.txt',
            'BODY_TEXT': 'Hello,\r\nPlease see the attached file.',
            'BODY_HTML': """\
                <html>
                <head></head>
                <body>
                <h1>Hello!</h1>
                <p>Please see the attached file.</p>
                </body>
                </html>
            """,
            'CHARSET': 'utf-8'
        }
    },
    # Add additional dictionaries and set ID's to refer to via CLI.
]