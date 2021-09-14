import os
import boto3


class EmailClient:
    ses = boto3.client('ses', region_name='us-east-1')
    EMAIL_SOURCE = os.getenv('EMAIL_SOURCE')
    DEFAULT_RECIPIENT = EMAIL_SOURCE
    AWS_SES_EMAIL_TEMPLATE = 'WeatherReminderTemplate'

    @classmethod
    def send_forecast(cls, template_data, recipient=DEFAULT_RECIPIENT):
        response = cls.ses.send_templated_email(
            Source=cls.EMAIL_SOURCE,
            Destination={
                'ToAddresses': [
                    recipient,
                ],
            },
            Template=cls.AWS_SES_EMAIL_TEMPLATE,
            TemplateData=template_data
        )

        print(response)
