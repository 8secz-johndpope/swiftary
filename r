zip s3faceupload.zip s3faceupload.py
aws lambda update-function-code --function-name s3faceupload --zip-file fileb://s3faceupload.zip
./s3copy.sh 
