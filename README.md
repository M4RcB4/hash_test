****************************************************************
****************************************************************
# Testing HashServ
****************************************************************
****************************************************************

<br>

## Run the Tests
This doc assumes you have a local python environment and have run unittests before. Please let me know if there are things that need to be added to the README.

At this time you need to have the service running on ```PORT:8089```. The tests are currently hard coded to ```PORT:8089```. This will be updated in the future as well as containerization and script intiated test run.

__FOR NOW...__
- Set env var ```export PORT=8089```
- Start service and ensure running
- Kick off test at the top level dir with ```python -m unittest discover```.

__Note:__ If you want pylint to work, you may need to update line 21 of pylint with the directory the repo is stored locally.
e.g. ```init-hook='import sys; sys.path.append("/Users/marcusbates/Source Control/Jumpcloud/python_unit_testing")```

<br><br><br>

# Testing Conversation

_Since I don't have any information managment systems to handle this sort of communication, I added this section to the README_

<br>

- __I may not have time to write these valuable tests__
  - Check the avg response time reported by stats against data collected.
  - Concurrent tests involving multiple users(just a couple) processed with acceptable times
  - Concurrent test with shutdown request, with hash requests mid-flight
  - End to end test checking the correct hash round trip(high LOE, badly broken right now so all test would fail)
  - Performance/Load tests involving multiple users(A LOT!) and the associated response times to determine the response degradation point and the full breakdown(less valuable when tested locally)
  - It would also be nice to fix some of the hacky stuff in the functional test related to the stats and shutdown tests.

<br><br>

## Questions

### Topic: Outstanding Work to be Done

_Review the code for ``TODO``s and determine what is still worth writing_

<br><br>

### Topic: Create New Password Hash

>A ​POST​ to ​/hash​ should accept a password. It should return a job identifier immediately. It should then wait 5 seconds and compute the password hash. The hashing algorithm should be SHA512.

- Returns job number immediately -> waits 5 seconds -> returns??? status code???
  - Wait 5-6(???confirm acceptable range for pass fail case???) seconds before completion
  - ??? Currently the job number is returned after processing time then request completion. What is the expected behavior as it doesn't match the requirments? Also, how should the two seperate returns happen? Should there be two calls/request to allow for the jobnum call to complete? Additional clairification needed. 
  - ASSERT job number immediately(???Could be a bad design to respond this way??)
  - ASSERT computes and returns(???A 200, hash, ???) in 5-6(???confirm acceptable range for pass fail case???) seconds
- How will it return a jobID immediately? Will there be two requests: one, for the kickoff and jobID is the response followed by a GET for the hash with the jobID as an input parameter? I would like to know more about how this is intented to behave and its implimetation so I can test it?
- Is this an industry standard way to pass in a password like this? Does it need to be an object like this? Should it be base64 instead of plain text; would that offer any added security?

<br>

### TOPIC: Shutdown Command

- Should this be it's own endpoint?
- Should we have some kind of authentication?

<br>

### TOPIC: Data persistence, JobID, and Returns for In Flight Hash Requests

Everytime the service is shutdown and restarted the job identification numbers reset. When a hash creation job is in flight and a shutdown is intitiated, a response with a job ID only(hash is not returned) is sent. All future requests will be rejected. 

- Without apparent persistence or the ability to lookup the created hash, what is the value of the _"finish requests before shutdown"_ have?

<br>

### TOPIC: Stats Endpoint

- stats endpoint will accept request body, but doesn't seem to be effected by it.

...END...
=========
