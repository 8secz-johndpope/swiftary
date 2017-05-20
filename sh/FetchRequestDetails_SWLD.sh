zip FetchRequestDetails_SWLD.zip FetchRequestDetails_SWLD.py
aws lambda update-function-configuration --function-name FetchRequestDetails_SWLD --handler FetchRequestDetails_SWLD.lambda_handler
aws lambda update-function-code --function-name FetchRequestDetails_SWLD --zip-file fileb://FetchRequestDetails_SWLD.zip
