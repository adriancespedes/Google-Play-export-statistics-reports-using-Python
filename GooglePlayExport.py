import json

from httplib2 import Http

from oauth2client.service_account import ServiceAccountCredentials 

from datetime import datetime, timedelta
import googleapiclient.discovery
import googleapiclient.http

# Change these variables in order to change authentication
json_file = 'privateAccountKeys.json'
client_email = json.loads(open(json_file).read())['client_email']
cloud_storage_bucket = 'pubsite_prod_rev_XXXXXXXXXX'


def create_service():
    #     http://g.co/dv/api-client-library/python/apis/
    return googleapiclient.discovery.build('storage', 'v1', http=credentials.authorize(Http()))

def get_object(bucket, filename, out_file):
    service = create_service()
    # http://g.co/dv/resources/api-libraries/documentation/storage/v1/python/latest/storage_v1.objects.html#get_media
    req = service.objects().get_media(bucket=bucket, object=filename)

    downloader = googleapiclient.http.MediaIoBaseDownload(out_file, req)

    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download {}%.".format(int(status.progress() * 100)))

    return out_file

# Today's reports are not available, we get last day reports
i = datetime.today() - timedelta(3)
lastMonth = i.strftime('%Y%m')
lastDate = i.strftime('%Y%m%d')
report_to_download = 'stats/installs/installs_com.XXXXX.YYYYYY.eysa_'+lastMonth+'_overview.csv'

private_key = json.loads(open(json_file).read())['private_key']

scope = ['https://www.googleapis.com/auth/devstorage.read_only']
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file,'https://www.googleapis.com/auth/devstorage.read_only')

file = open('report_'+lastMonth+'.csv', 'ab')

get_object(cloud_storage_bucket,report_to_download,file)

