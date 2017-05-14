zip UpdateRequest_SWLD.zip UpdateRequest_SWLD.py
aws lambda update-function-configuration --function-name UpdateRequest_SWLD --handler UpdateRequest_SWLD.lambda_handler
aws lambda update-function-code --function-name UpdateRequest_SWLD --zip-file fileb://UpdateRequest_SWLD.zip
