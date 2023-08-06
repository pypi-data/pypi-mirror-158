# Python Substrate Interface Library
#
# Copyright 2018-2021 Stichting Polkascan (Polkascan Foundation).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from reefinterface import SubstrateInterface, ReefInterface
from test import settings


class SubscriptionsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reef = ReefInterface(url=settings.REEF_NODE_URL)

    @classmethod
    def tearDownClass(cls):
        cls.reef.close()

    def test_query_subscription(self):
        def subscription_handler(obj, update_nr, subscription_id):

            return {"update_nr": update_nr, "subscription_id": subscription_id}

        result = self.reef.query(
            "System", "Events", [], subscription_handler=subscription_handler
        )

        self.assertEqual(result["update_nr"], 0)
        self.assertIsNotNone(result["subscription_id"])

    def test_subscribe_new_heads(self):
        def block_subscription_handler(obj, update_nr, subscription_id):
            return obj["header"]["number"]

        result = self.reef.subscribe_block_headers(
            block_subscription_handler, finalized_only=True
        )

        self.assertGreater(result, 0)


if __name__ == "__main__":
    unittest.main()
