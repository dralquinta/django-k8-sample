import os

AWS_ACCESS_KEY_ID=os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.environ.get("AWS_SECRET_ACCESS_KEY")

AWS_STORAGE_BUCKET_NAME= "npieri-bucket"
AWS_S3_ENDPOINT_URL="https://idhkis4m3p5e.compat.objectstorage.uk-london-1.oraclecloud.com"

AWS_S3_REGION_NAME="uk-london-1"

DEFAULT_FILE_STORAGE = "django_k8s.cdn.backends.MediaRootS3BotoStorage"
STATICFILES_STORAGE = "django_k8s.cdn.backends.StaticRootS3BotoStorage"