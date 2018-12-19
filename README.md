### PythonZestClient

This python client connects with the zest datastore.

### Testing the client:
#### Prerequisites for testing:
In terminal (inside PythonZestClient folder):

* __./setupTest.sh__ (this will deploy zest database server so client could make requests to it)
* __docker logs zest -f__ (this will enable server logs so you can see server responses for client requests e.g. in case if some debugging is needed)

#### Automatic tests:

* In terminal run __./zestClientTest.py__ (these auto tests will check that create/delete/post requests work properly)

#### Manual testing:

Manual tests allows you to write your own create/delete/post/observe requests and see responses from server for each of them.
* In terminal run __python3 ./client.py__ This will bring you to python command line prompt
* In python cmd type a request in the following format: [ request type ] [ content format ] [ uri path ] [ payload(for POST) ] [ observe mode (for OBSERVE) ] [ time out (for OBSERVE) ]. Here are some examples for each of the requests:

  * __POST__: _post json /kv/test/key {"name":"Mike","age":27}_
  * __GET__: _get json /kv/test/key_
  * __DELETE__: _delete json /kv/test/key_
  * __OBSERVE__: _observe json /kv/test/key data 0_
  
### Development of databox was supported by the following funding
EP/N028260/1, Databox: Privacy-Aware Infrastructure for Managing Personal Data

EP/N028260/2, Databox: Privacy-Aware Infrastructure for Managing Personal Data

EP/N014243/1, Future Everyday Interaction with the Autonomous Internet of Things

EP/M001636/1, Privacy-by-Design: Building Accountability into the Internet of Things (IoTDatabox)

EP/M02315X/1, From Human Data to Personal Experience

