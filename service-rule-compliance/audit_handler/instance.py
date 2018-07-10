from resource import Resource
from query import ec2_instances_by_regions
from filter.filter_instance import tag_policy_not_satisfied

class Instance(Resource):
    def __init__(self):
        super(Instance, self).__init__(
            'ec2',
            'instance',
            'InstanceId',
            candidate_field='State.Name',
            candidate_value='running',
            time_field='LaunchTime'
        )

    def get_candidates(self):
        instances = ec2_instances_by_regions()
        candidates = {}
        for k, v in instances.items():
            candidates_instances = []
            for instance in v:
                if tag_policy_not_satisfied(instance):
                    candidates_instances.append(instance)
            if len(candidates_instances) > 0:
                candidates.update({k: candidates_instances})

        return candidates
