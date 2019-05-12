import logging

logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.info('python worker app start')

import flask
from flask import request, Response

from boto.sqs.message import RawMessage
from boto.sqs.message import Message
from boto.s3.key import Key
import boto


@application.route('/worker', methods=['POST'])
def worker():
    logging.info('in worker')
    s3_output_bucket = "nthu-105060005"
    write_excel_to_s3('example.log','example.log', s3_output_bucket)



def write_excel_to_s3(path, file_name, s3_output_bucket):
    # Connect to S3 and get the output bucket
    #s3 = boto.connect_s3(host=s3_endpoint)
    s3 = boto.connect_s3()
    output_bucket = s3.get_bucket(s3_output_bucket)

    # Create a key to store the instances_json text
    k = Key(output_bucket)
    k.key = file_name
    #k.set_metadata("Content-Type", "image/jpeg")
    k.set_contents_from_filename(path)
    k.set_acl('public-read')

    # Return a URL to the object
    return "https://%s.s3.amazonaws.com/%s" % (s3_output_bucket, k.key)



if __name__ == '__main__':
    #excel.init_excel(application)
    application.run(host='0.0.0.0', port='80')
