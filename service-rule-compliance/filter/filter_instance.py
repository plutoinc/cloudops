import logging
import jmespath
from dateutil import tz
from datetime import datetime, timedelta

log = logging.getLogger()


def _launched_in_60min(instance):
    utcnow = datetime.utcnow().replace(tzinfo=tz.tzutc())
    start_at = utcnow - timedelta(minutes=60)
    end_at = utcnow - timedelta(minutes=10)

    if start_at <= instance.launch_time <= end_at:
        return True
    else:
        return False


def _running(instance):
    return instance.state['Name'] == 'running'


def _terminated(instance):
    return instance.state['Name'] == 'terminated'


def tag_policy_not_satisfied(instance):
    if not _running(instance):
        log.debug("[%s] is not running" % instance.instance_id)
        return False

    if not _launched_in_60min(instance):
        log.debug("[%s] out of range of launch time" % instance.instance_id)
        return False

    id = instance.instance_id
    tags = instance.tags or []
    role_tag = jmespath.search("[?Key=='role'].Value | [0]", tags)

    if not bool(role_tag):
        log.info("[%s] no_tag" % id)
        return True

    return False

