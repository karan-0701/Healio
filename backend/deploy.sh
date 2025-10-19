# Create a unique bucket name with timestamp
DEPLOY_BUCKET="twin-deploy-$(date +%s)"

# Create the bucket
aws s3 mb s3://$DEPLOY_BUCKET

# Upload your zip file to S3
aws s3 cp backend/lambda-deployment.zip s3://$DEPLOY_BUCKET/

# Display the S3 URI
echo "S3 URI: s3://$DEPLOY_BUCKET/lambda-deployment.zip"
