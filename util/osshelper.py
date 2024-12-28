import os
import boto3
from botocore.exceptions import NoCredentialsError

# s3实现
class OssHelper:

    def __init__(self, access_key, secret_key, endpoint_url,bucket_name, region='cn-north-1',):
        self.s3 = boto3.client('s3',
                                aws_access_key_id=access_key,
                                aws_secret_access_key=secret_key,
                                region_name=region,
                               endpoint_url=endpoint_url
                               )
        self.bucket_name = bucket_name

    def get_file_list(self, prefix=''):
        result = []
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
        if 'Contents' in response:
            for obj in response['Contents']:
                result.append({
                    "name": os.path.basename(obj['Key']),
                    "size": obj['Size'],
                    "type": "s3"
                })
        return result

    def upload(self, upload_path, file_path):
        """
        upload_path: 文件上传后的完整路径，包括本身
        file_path: 本地文件路径
        """
        try:
            self.s3.upload_file(file_path, self.bucket_name, upload_path)
            print(f"上传成功: {file_path} 到 {upload_path}")
        except FileNotFoundError:
            print(f"文件未找到: {file_path}")
        except NoCredentialsError:
            print("凭证错误")

    def delete(self, obj_name):
        self.s3.delete_object(Bucket=self.bucket_name, Key=obj_name)

    def percentage(self, consumed_bytes, total_bytes):
        """进度条回调函数，计算当前完成的百分比"""
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            print('\r{0}% '.format(rate), end='')

    def download(self, s3_object, local_file):
        try:
            self.s3.download_file(self.bucket_name, s3_object, local_file)
            print(f"下载成功: {s3_object} 到 {local_file}")
        except Exception as e:
            print(f"下载失败: {e}")

if __name__ == '__main__':

    # 阿里云oss访问地址需要带bucket_name https://backup2222.oss-cn-shenzhen.aliyuncs.com
    oss = OssHelper('ak', 'sk',
                      'https://backup2222.oss-cn-shenzhen.aliyuncs.com','db-backup' )

    oss = OssHelper('ak', 'sk',
                      'https://oss.doamin.com','db-backup' )

    # oss = OssHelper(ossConf.accessKey, ossConf.secretKey,
    #                 ossConf.url, ossConf.bucket)

    ossPath =    'local' + "/" + 'cat2.png'
    oss.upload(ossPath, 'C:\\Users\\w\\Pictures\\cat.png')
    pass