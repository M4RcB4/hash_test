import unittest
import random
import string
import json
from src.app.api_helper import *

class FunctionalApiTest(unittest.TestCase):

    # TODO: (P2) Add setup() that ensures the service is up and running, ideall in a container
    # TODO: (???) RESEARCH What header/request/payload information should I be messing with to check for edge cases
    
    def tearDown(self):
        print("finished running " + self._testMethodName)

    def test_responds_with_jobnum(self):
        # ---Setup
        tdata = '{"password":"angrymonkey"}'
        # ---Act
        resp = req_password(tdata)
        jobnum = resp.text
        # ---Assert
        self.assertTrue(1 <= int(jobnum) <= 1000)
        self.assertTrue(resp.status_code == 200)

    def test_handles_invalid_inputs(self):
        # TODO: (???) Review the expected response codes. Anything that won't result in a sucessful attempt should return 400
        # TODO: (???) Try to identify more cases to be tested.
        # ---Setup
        tdata = [
            (1, '{"password":""}', 400),
            (2, '{"password":!@#$%^&*()}', 400),
            (4, False, 400)
        ]
        # ---Act
        for case, password, expected in tdata:
            with self.subTest(line=case):
                res = req_password(password)
                # ---Assert
                self.assertEqual(res.status_code, expected)

    def test_handles_massive_passwords(self):
        # ---Setup
        tdata = [
            (50, 200),
            (100, 200),
            (200, 200),
            (1000, 200),
            (10000, 200)
        ]
        # ---Act
        for passlength,expected in tdata:
            with self.subTest(line=passlength):
                massivepass = ''.join(random.choices(string.ascii_uppercase
                    + string.digits, k = passlength))
                wrappedpass = '{"password":"' + massivepass + '"}'
                res = req_password(wrappedpass)
                # ---Assert
                self.assertEqual(res.status_code, expected)

    def test_returns_b64_hash_for_valid_job(self):
        # ---Setup
        jobnum = 1
        # ---Act
        resp = lookup_pass_hash(jobnum)
        # ---Assert
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.ok, True)
        # Based upon some quick experiements I did, the results should always be 172 for a b64 encoded SHA512 digest
        self.assertEqual(len(resp.text), 172)

    def test_handles_invalid_jobnums(self):
        # ...These cases are admittadely a little silly...
        # ---Setup
        tdata = [
            (0, 400, 'Hash not found'),
            (-1, 400, 'Hash not found'),
            (145, 400, 'Hash not found'),
            ('word', 400, 'strconv.Atoi: parsing "word": invalid syntax'),
            ('$', 400, 'strconv.Atoi: parsing "$": invalid syntax')
        ]
        # ---Act
        for jobnum,ecode,emsg in tdata:
            with self.subTest(line=jobnum):
                resp = lookup_pass_hash(jobnum)
                # ---Assert
                self.assertEqual(resp.status_code, ecode)
                self.assertIn(emsg, resp.text)

    def test_1_stats_report_expected(self):
        # ...Hacky but it makes the test more resilient without low LOE...
        # Test name starts with 1 so other requests don't make the number undeterministic
        # ---Setup
        jobcount = int(req_password('{"password":"good enough"}').text)
        # ---Act
        resp = json.loads(get_stats(self).text)
        # ---Assert
        self.assertEqual(resp["TotalRequests"], jobcount,
        f'Expected:{jobcount} Actual:{resp["TotalRequests"]}')
        # TODO: ??? Verify expected response window???
        self.assertTrue(5000 <= resp["AverageTime"] <= 6000 ,
        f'The value was expected to be between 5000-6000ms, actual={resp["AverageTime"]}')
        # TODO: FUTURE check reported avg response time against collected response time.

    def test_zzzz_shutdown_works(self):
        # ... Hacky...test name starts with zzzz so that it runs last
        # ---Act
        resp = req_shutdown(self)
        # ---Assert
        self.assertTrue(resp is not None, 'No response was returned:{resp}')
        self.assertEqual(resp.status_code, 200)
