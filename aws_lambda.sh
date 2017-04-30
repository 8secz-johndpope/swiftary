aws s3 cp ./imagestemp/leonardo_dicaprio2.jpeg s3://swiftarycelebritytemp/
aws s3 cp ./imagestemp/angelina_jolie.jpg s3://swiftarycelebritytemp/
aws lambda update-function-configuration --function-name matchface --handler matchface_lambda.lambda_handler
aws lambda update-function-code --function-name matchface --zip-file fileb://matchface_lambda.zip
aws lambda update-function-code --function-name s3faceupload --zip-file fileb://s3faceupload.zip
aws lambda update-function-configuration --function-name s3faceupload --handler s3faceupload.lambda_handler

aws lambda update-function-code --function-name FetchFaceDetails --zip-file fileb://FetchFaceDetails.zip
aws lambda update-function-configuration --function-name FetchFaceDetails --handler FetchFaceDetails.lambda_handler

aws lambda update-function-code --function-name InsertRequest --zip-file fileb://InsertRequest.py
aws lambda update-function-configuration --function-name InsertRequest --handler InsertRequest.lambda_handler

aws lambda update-function-code --function-name UpdateRequest --zip-file fileb://UpdateRequest.py
aws lambda update-function-configuration --function-name UpdateRequest --handler UpdateRequest.lambda_handler

