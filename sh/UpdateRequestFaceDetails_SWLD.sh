zip UpdateRequestFaceDetails_SWLD.zip UpdateRequestFaceDetails_SWLD.py
aws lambda update-function-configuration --function-name UpdateRequestFaceDetails_SWLD --handler UpdateRequestFaceDetails_SWLD.lambda_handler
aws lambda update-function-code --function-name UpdateRequestFaceDetails_SWLD --zip-file fileb://UpdateRequestFaceDetails_SWLD.zip
