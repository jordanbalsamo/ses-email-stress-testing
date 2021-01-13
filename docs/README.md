# Email Stress Tests

The intention of this set of scripts is to send email templates to a specified email address using the SendRAWEmailAPI for the AWS Simple Email Service (SES).

# An Important Note

- Keep message volumes within sensible limits. Check your AWS account for the limits imposed. Abuse will mean that AWS will stop your use of SES.
- Do not use recipients or senders that have not been validated via the given SES account, as this will cause your reputation on AWS SES to degrade and will have a direct impact on your ability to use AWS SES in the future.

The addition of recipients and senders is controlled via Pull Requests to the repo, where you will need a reviewer to approve prior to running the scipt.

In all cases, please use this script responsibly :).

## Inputs and Outpus

### Inputs

You should provide the following parameters to this script:

```
--iterations (INT): the number of times you wish the email to be sent.

--sleep-seconds (INT): the number of seconds you wish to elapse prior to sending the next email in the batch.

--template-choice (INT): the identifer (ID) of the template in the dictionary of declared email templates contained in email_template.py

--safeguard-limit (INT): primarily for use in a pipeline to limit the maximum number of send iterations input by the user of the script. If using this script outside of a pipeline execution environment - i.e. on your local machine - please pass in the same integer value as iterations.
```

### Outputs

An email is sent (n) number of times, according to the template and number iterations the user provides as parameters to the script.

# How to use these scripts

## My script is wrapped in a pipeline

You simply need to provide the above-noted input parameters.

The ADO pipeline that runs this should supply a hard-coded variable that dictates the iteration safeguard. This will limit the number of emails that can be sent in one iteration.

## My script is not wrapped in a pipeline

### Setup envirnoment variables

In order to use these scripts, you will need to export two environment variables for AWS SES Auth. These are:

```
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
```

These variables represent the AWS IAM service account that has the required SES permissions to perform the methods contained within the scripts.

Please consider the AWS SES daily email limit, as this will be limiting factor on how you use this script.

### Python Dependencies

For best results, use a virtual env to manage dependencies contained within these scripts:

```
python -m venv ./path-containing-scripts/.venv
source ./path-containing-scripts/.venv/bin/activate
pip3 install -r requirements.txt
-- if creating or deleting templates
python3 name-of-script-here.py --template-name
-- if sending emails
python3 name-of-script-here.py --template-name my-template --iterations 100
```

# Future improvements

## How to contribute

If you wish to improve this repo, please raise a PR :).

## Future ideas

1) Config to be driven by a JSON file;
2) Flagged function to randomise choice of template on each iteration using random.choice;
3) Attachments to be downloaded from a given remote object storage facility (Azure Blob Storage, S3, etc.) to keep repo more lightweight.
4) Parallelisation to be achieved via parallel stages running in a pipeline.

# References

SendRawEmail

https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-email-raw.html
