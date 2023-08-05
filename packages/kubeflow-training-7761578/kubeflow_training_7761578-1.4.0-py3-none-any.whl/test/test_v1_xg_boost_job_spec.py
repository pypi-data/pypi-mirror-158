# coding: utf-8

"""
    Kubeflow Training SDK

    Python SDK for Kubeflow Training  # noqa: E501

    The version of the OpenAPI document: v1.4.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

from kubeflow.training.models import *
from kubeflow.training.models.v1_xg_boost_job_spec import V1XGBoostJobSpec  # noqa: E501
from kubeflow.training.rest import ApiException

class TestV1XGBoostJobSpec(unittest.TestCase):
    """V1XGBoostJobSpec unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test V1XGBoostJobSpec
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = kubeflow.training.models.v1_xg_boost_job_spec.V1XGBoostJobSpec()  # noqa: E501
        if include_optional :
            return V1XGBoostJobSpec(
                run_policy = V1RunPolicy(
                    active_deadline_seconds = 56, 
                    backoff_limit = 56, 
                    clean_pod_policy = '0', 
                    scheduling_policy = V1SchedulingPolicy(
                        min_available = 56, 
                        min_resources = {
                            'key' : None
                            }, 
                        priority_class = '0', 
                        queue = '0', ), 
                    ttl_seconds_after_finished = 56, ), 
                xgb_replica_specs = {
                    'key' : V1ReplicaSpec(
                        replicas = 56, 
                        restart_policy = '0', 
                        template = None, )
                    }
            )
        else :
            return V1XGBoostJobSpec(
                run_policy = V1RunPolicy(
                    active_deadline_seconds = 56, 
                    backoff_limit = 56, 
                    clean_pod_policy = '0', 
                    scheduling_policy = V1SchedulingPolicy(
                        min_available = 56, 
                        min_resources = {
                            'key' : None
                            }, 
                        priority_class = '0', 
                        queue = '0', ), 
                    ttl_seconds_after_finished = 56, ),
                xgb_replica_specs = {
                    'key' : V1ReplicaSpec(
                        replicas = 56, 
                        restart_policy = '0', 
                        template = None, )
                    },
        )

    def testV1XGBoostJobSpec(self):
        """Test V1XGBoostJobSpec"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
