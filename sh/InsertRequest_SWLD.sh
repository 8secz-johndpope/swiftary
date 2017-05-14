zip InsertRequest_SWLD.zip InsertRequest_SWLD.py
#aws lambda update-function-configuration --function-name InsertRequest_SWLD --handler InsertRequest_SWLD.lambda_handler
aws lambda update-function-code --function-name InsertRequest_SWLD --zip-file fileb://InsertRequest_SWLD.zip
