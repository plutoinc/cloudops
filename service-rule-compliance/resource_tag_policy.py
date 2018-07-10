import os
import sys
import logging

from helper import noti

from instance import Instance

log_level = os.environ.get('log_level') or logging.INFO

log = logging.getLogger()
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(log_level)


def handler(event, context):
    log.info("[======= %s ========]\n" % (log_level))

    resources = [Instance]

    for resource in resources:
        log.info('handle %s' % resource)
        try:
            resource().handle()
        except Exception as e:
            reason = 'exception detected during handle %s - %s' % (resource, e)
            log.info(reason)
            noti.notify(reason)

    response = {
        "statusCode": 200,
        "body": {
        }
    }
    return response


if __name__ == "__main__":
    event = {}
    handler(event, None)
