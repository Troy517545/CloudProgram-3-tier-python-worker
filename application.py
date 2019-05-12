import logging

logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.info('python worker app start')
logging.info('hi')

import flask
from flask import request, Response

from boto.sqs.message import RawMessage
from boto.sqs.message import Message
from boto.s3.key import Key
import boto

# s3_output_bucket = "nthu-105060005"
# write_excel_to_s3('example.log','example.log', s3_output_bucket)

application = flask.Flask(__name__)


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


@application.route('/worker', methods=['POST'])
def worker():
    logging.info('in worker')
    # s3_output_bucket = "nthu-105060005"
    # write_excel_to_s3('example.log','example.log', s3_output_bucket)

    response = None
    if request.json is None:
        # Expect application/json request
        response = Response("", status=415)
    else:
        try:
            user = request.json['user']
            excelURL = request.json['url']
            fileName = request.json['filename']
            logging.info('hi')

            logging.info("user: %s URL: %s" % (user, excelURL))


            s3_output_bucket = "nthu-105060005"
            write_excel_to_s3('test.txt','test.txt', s3_output_bucket)

            response = Response("success", status=200)

        except Exception as ex:
            logging.exception('Error processing message: %s' % request.json)
            response = Response(ex.message, status=500)

    return response
    

# test


if __name__ == '__main__':
    #excel.init_excel(application)
    application.run(host='127.0.0.1', port='80')
