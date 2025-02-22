#   Copyright Peznauts <kevin@cloudnull.com>. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.

import json

from unittest.mock import ANY
from unittest.mock import patch

from directord import client
from directord import tests


class TestClient(tests.TestDriverBase):
    def setUp(self):
        super(TestClient, self).setUp()
        self.args = tests.FakeArgs()
        self.client = client.Client(args=self.args)
        self.client.driver = self.mock_driver

    @patch("time.time", autospec=True)
    def test_run_job(self, mock_time):
        job_def = {
            "job_sha3_224": "YYY",
            "skip_cache": True,
            "command": "RUN",
            "job_id": "XXX",
            "job_sha3_224": "YYY",
        }
        self.mock_driver.job_recv.side_effect = [
            (
                None,
                None,
                None,
                json.dumps(job_def),
                None,
                None,
                None,
            )
        ]
        mock_time.side_effect = [1, 1, 1, 1, 1, 1, 1]
        with patch.object(self.mock_driver, "job_check", return_value=False):
            self.client.run_job(sentinel=True)

    @patch("time.time", autospec=True)
    def test_run_job_idle(self, mock_time):
        job_def = {
            "job_sha3_224": "YYY",
            "skip_cache": True,
            "command": "RUN",
            "job_id": "XXX",
            "job_sha3_224": "YYY",
        }
        self.mock_driver.job_recv.side_effect = [
            (
                None,
                None,
                None,
                json.dumps(job_def),
                None,
                None,
                None,
            )
        ]
        mock_time.side_effect = [1, 1, 66, 1, 1, 1, 1]
        with patch.object(self.mock_driver, "job_check", return_value=False):
            self.client.run_job(sentinel=True)

    @patch("time.time", autospec=True)
    def test_run_job_ramp(self, mock_time):
        job_def = {
            "job_sha3_224": "YYY",
            "skip_cache": True,
            "command": "RUN",
            "job_id": "XXX",
            "job_sha3_224": "YYY",
        }
        self.mock_driver.job_recv.side_effect = [
            (
                None,
                None,
                None,
                json.dumps(job_def),
                None,
                None,
                None,
            )
        ]
        mock_time.side_effect = [1, 1, 1, 34, 1, 1, 1]
        with patch.object(self.mock_driver, "job_check", return_value=False):
            self.client.run_job(sentinel=True)

    @patch("diskcache.Cache", autospec=True)
    @patch("time.time", autospec=True)
    def test_run_job_cache_check(
        self,
        mock_time,
        mock_diskcache,
    ):
        job_def = {
            "job_sha3_224": "YYY",
            "skip_cache": True,
            "command": "RUN",
            "job_id": "XXX",
            "job_sha3_224": "YYY",
        }
        self.mock_driver.job_recv.side_effect = [
            (
                None,
                None,
                None,
                json.dumps(job_def),
                None,
                None,
                None,
            )
        ]
        mock_time.side_effect = [1, 1, 1, 1, 5000, 1, 1, 1, 1, 1]
        mock_diskcache.return_value = tests.FakeCache()
        with patch.object(self.mock_driver, "job_check", return_value=False):
            self.client.run_job(sentinel=True)

    @patch("diskcache.Cache", autospec=True)
    @patch("logging.Logger.info", autospec=True)
    @patch("time.time", autospec=True)
    def test_run_job_skip_skip_cache_run(
        self,
        mock_time,
        mock_log_info,
        mock_diskcache,
    ):
        job_def = {
            "job_sha3_224": "YYY",
            "skip_cache": True,
            "command": "RUN",
            "job_id": "XXX",
            "job_sha3_224": "YYY",
        }
        self.mock_driver.job_recv.side_effect = [
            (
                None,
                None,
                "RUN",
                json.dumps(job_def),
                "",
                None,
                None,
            )
        ]
        mock_diskcache.return_value = tests.FakeCache()
        mock_time.side_effect = [1, 1, 1, 1, 1, 1, 1]
        with patch.object(self.mock_driver, "job_check") as mock_job_check:
            mock_job_check.side_effect = [True, False]
            self.client.run_job(sentinel=True)
        mock_log_info.assert_called()

    @patch("diskcache.Cache", autospec=True)
    @patch("logging.Logger.info", autospec=True)
    @patch("time.time", autospec=True)
    def test_run_job_skip_ignore_cache_run(
        self,
        mock_time,
        mock_log_info,
        mock_diskcache,
    ):
        job_def = {
            "job_id": "XXX",
            "job_sha3_224": "YYY",
            "ignore_cache": True,
            "command": "RUN",
            "job_id": "XXX",
            "job_sha3_224": "YYY",
        }
        self.mock_driver.job_recv.side_effect = [
            (
                None,
                None,
                "RUN",
                json.dumps(job_def),
                "",
                None,
                None,
            )
        ]
        mock_diskcache.return_value = tests.FakeCache()
        mock_time.side_effect = [1, 1, 1, 1, 1, 1, 1]
        with patch.object(self.mock_driver, "job_check") as mock_job_check:
            mock_job_check.side_effect = [True, False]
            self.client.run_job(sentinel=True)
        mock_log_info.assert_called()

    @patch("diskcache.Cache", autospec=True)
    @patch("logging.Logger.info", autospec=True)
    @patch("time.time", autospec=True)
    def test_run_job_parent_failed_run(
        self,
        mock_time,
        mock_log_info,
        mock_diskcache,
    ):
        job_def = {
            "job_id": "XXX",
            "job_sha3_224": "YYY",
            "parent_id": "ZZZ",
            "command": "RUN",
        }
        self.mock_driver.job_recv.side_effect = [
            (
                None,
                None,
                "RUN",
                json.dumps(job_def),
                "",
                None,
                None,
            )
        ]
        cache = mock_diskcache.return_value = tests.FakeCache()
        cache.set(key="ZZZ", value=False)
        mock_time.side_effect = [1, 1, 1, 1, 1, 1, 1]
        with patch.object(self.mock_driver, "job_check") as mock_job_check:
            mock_job_check.side_effect = [True, False]
            self.client.run_job(sentinel=True)
        mock_log_info.assert_called()

    @patch("diskcache.Cache", autospec=True)
    @patch("logging.Logger.info", autospec=True)
    @patch("time.time", autospec=True)
    def test_run_job_cache_hit_run(
        self,
        mock_time,
        mock_log_info,
        mock_diskcache,
    ):
        job_def = {
            "job_id": "XXX",
            "job_sha3_224": "YYY",
            "command": "RUN",
            "job_id": "XXX",
            "job_sha3_224": "YYY",
        }
        self.mock_driver.job_recv.side_effect = [
            (
                None,
                None,
                "RUN",
                json.dumps(job_def),
                "",
                None,
                None,
            )
        ]
        cache = mock_diskcache.return_value = tests.FakeCache()
        cache.set(key="YYY", value=self.mock_driver.job_end)
        mock_time.side_effect = [1, 1, 1, 1, 1, 1, 1]
        with patch.object(self.client, "cache", cache):
            with patch.object(self.mock_driver, "job_check") as mock_job_check:
                mock_job_check.side_effect = [True, False]
                self.client.run_job(sentinel=True)
        mock_log_info.assert_called()

    @patch("diskcache.Cache", autospec=True)
    @patch("logging.Logger.info", autospec=True)
    @patch("time.time", autospec=True)
    def test_run_job_run(
        self,
        mock_time,
        mock_log_info,
        mock_diskcache,
    ):
        job_def = {
            "job_id": "XXX",
            "job_sha3_224": "YYY",
            "command": "RUN",
            "parent_id": "ZZZ",
            "job_id": "XXX",
            "job_sha3_224": "YYY",
        }
        self.mock_driver.job_recv.side_effect = [
            (
                None,
                None,
                "RUN",
                json.dumps(job_def),
                "",
                None,
                None,
            )
        ]
        cache = mock_diskcache.return_value = tests.FakeCache()
        cache.set(key="YYY", value=self.mock_driver.job_end)
        mock_time.side_effect = [1, 1, 1, 1, 1, 1, 1]
        with patch.object(self.client, "cache", cache):
            with patch.object(self.mock_driver, "job_check") as mock_job_check:
                mock_job_check.side_effect = [True, False]
                self.client.run_job(sentinel=True)
        mock_log_info.assert_called()
        self.assertEqual(cache.get("YYY"), self.mock_driver.job_end)

    @patch("diskcache.Cache", autospec=True)
    @patch("logging.Logger.info", autospec=True)
    @patch("time.time", autospec=True)
    def test_run_job_run_outcome_false(
        self,
        mock_time,
        mock_log_info,
        mock_diskcache,
    ):
        job_def = {
            "job_id": "XXX",
            "job_sha3_224": "YYY",
            "command": "RUN",
            "job_id": "XXX",
            "job_sha3_224": "YYY",
        }
        self.mock_driver.job_recv.side_effect = [
            (
                None,
                None,
                "RUN",
                json.dumps(job_def),
                "",
                None,
                None,
            )
        ]
        cache = mock_diskcache.return_value = tests.FakeCache()
        cache.set(key="YYY", value=self.mock_driver.job_failed)
        mock_time.side_effect = [1, 1, 1, 1, 1, 1, 1]
        with patch.object(self.mock_driver, "job_check") as mock_job_check:
            mock_job_check.side_effect = [True, False]
            self.client.run_job(sentinel=True)
        mock_log_info.assert_called()
        self.assertEqual(cache.get("YYY"), self.mock_driver.job_failed)

    @patch("os.makedirs", autospec=True)
    @patch("diskcache.Cache", autospec=True)
    @patch("directord.client.Client.run_threads", autospec=True)
    def test_worker_run(self, mock_run_threads, mock_diskcache, mock_makedirs):
        self.client.worker_run()
        mock_run_threads.assert_called_with(ANY, threads=[ANY])
        mock_diskcache.assert_called()
        mock_makedirs.assert_called()
