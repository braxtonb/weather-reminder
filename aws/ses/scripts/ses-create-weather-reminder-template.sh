echo 'Craeting weather-reminder-email-template'
aws ses create-template --cli-input-json file://aws/ses/emails/weather-email/weather-reminder-email-template.json
echo 'Craete successful'
