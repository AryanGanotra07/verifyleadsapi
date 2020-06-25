import boto3
from botocore.exceptions import NoCredentialsError
import base64
import os
from PIL import Image

ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')
BUCKET = os.environ.get('BUCKET')

def upload_to_aws(data, s3_file):
    cur_path = os.path.dirname(__file__)
    fileName = s3_file+".png"
    new_path = os.path.join(cur_path, "images/" + fileName)
    print(new_path)
    with open(new_path, "wb") as fh:
            fh.write(base64.b64decode(data))
    image = Image.open(new_path)
    # x, y = image.size
    # image.resize((int(x//6),int(y//6)),Image.ANTIALIAS)
    image.save(new_path,quality=20,optimize=True)
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
   
    try:
        h = s3.upload_file(new_path, BUCKET, fileName)
        s3.put_object_acl( ACL='public-read', Bucket=BUCKET, Key=fileName )
        location = s3.get_bucket_location(Bucket=BUCKET)['LocationConstraint']
        url = "https://%s.s3.%s.amazonaws.com/%s" % (BUCKET,location, fileName)
        print("Upload Successful", h)
        try:
            os.remove(new_path)
            #pass
        except:
            print("Error in removing image")
            print(url);
        return { 'message' : 'Upload Successful', 'imgUrl' : url, 'code' : 1}
    except FileNotFoundError:
        print("The file was not found")
        return {'message' : 'File not found', 'code' : 0}
    except NoCredentialsError:
        print("Credentials not available")
        return {'message' : 'Credentials not found', 'code' : 0}