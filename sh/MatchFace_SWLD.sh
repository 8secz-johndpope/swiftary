zip MatchFace_SWLD.zip MatchFace_SWLD.py
#aws lambda update-function-configuration --function-name MatchFace_SWLD --handler MatchFace_SWLD.lambda_handler
aws lambda update-function-code --function-name MatchFace_SWLD --zip-file fileb://MatchFace_SWLD.zip
