import logging
import abc

import jmespath
log = logging.getLogger()


class Resource(object):

    def __init__(self,
                 awsservice,
                 awstype,
                 id_field,
                 index='skewer',
                 candidate_field=None,
                 candidate_value=None,
                 role_field='meta.role',
                 time_field=None,
                 time_range='[now-120m TO now-60m]'
                 ):
        self.index = index
        self.awsservice = awsservice
        self.awstype = awstype
        self.id_field = id_field
        self.role_field = role_field
        self.candidate_field = candidate_field
        self.candidate_value = candidate_value
        self.time_field = time_field
        self.time_range = time_range

    @abc.abstractmethod
    def delete_function(self, resource_id, region, resource=None):
        pass

    @abc.abstractmethod
    def confirm(self, resource):
        pass

    @abc.abstractmethod
    def check_confirm_tag(self, resource):
        return None

    @abc.abstractmethod
    def get_candidates(self):
        return None

    def handle(self):
        candidate_resources = self.get_candidates()
        for k, v in candidate_resources.items():
            for item in v:
                try:
                    resource = item.__dict__['meta'].data
                    resource_id = jmespath.search(self.id_field, resource)
                    self._audit(k, resource_id)
                except BaseException as e:
                    log.info(e.message)

    def _audit(self, region, resource_id):
        message = "[TagViolation] region : %s, service : %s, type : %s, id : %s" \
                  % (region, self.awsservice, self.awstype, resource_id)
        import noti
        noti.notify(message)
