cd .venv/lib/python3.8/site-packages/
zip -FSr ../../../../weather-reminder.zip .
cd -
zip -g ./weather-reminder.zip lambda_function.py -r lambda_lib