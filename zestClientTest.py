import pythonzestclient
import unittest

zestEndpoint="tcp://127.0.0.1:5555"
zestDealerEndpoint="tcp://127.0.0.1:5556"
CORE_STORE_KEY="vl6wu0A@XP?}Or/&BR#LSxn>A+}L)p44/W[wXL3<"
tokenString=b"secrete"

class WriteReadTestCase(unittest.TestCase):
    def setUp(self):
        self.zc = pythonzestclient.PyZestClient(CORE_STORE_KEY,zestEndpoint,zestDealerEndpoint)

    def testKVWrite(self):
        print('----------------------\n|       testKVWrite   |\n ----------------------')
        payLoad='{"name":"testuser2","age":38}'
        path='/kv/test/key1'
        contentFormat='JSON'
        print("\t*posted: " + payLoad)
        response = self.zc.post(path, payLoad, contentFormat,tokenString)
        self.assertEqual(response,"")

    def testKVRead(self):
        print('----------------------\n|       testKVRead    |\n ----------------------')
        expected='{"name":"testuser3","age":39}'
        path='/kv/test/key1'
        contentFormat='JSON'
        print("\t*posted: " + expected)
        response = self.zc.post(path, expected, contentFormat,tokenString)
        self.assertEqual(response,"")

        response = self.zc.get(path, contentFormat,tokenString)
        print("\t*read: " + response)
        self.assertEqual(response,expected)

    def testKVDelete(self):
        print('''-----------------------\n|       testKVDelete  |\n ----------------------''')
        payLoad='{"name":"testuser5","age":33}'
        path='/kv/test/key1'
        contentFormat='JSON'

        response = self.zc.post(path, payLoad, contentFormat,tokenString)
        self.assertEqual(response,"")
        print("\t*posted: " + payLoad)

        response = self.zc.get(path, contentFormat,tokenString)
        print("\t*read: " + response)
        self.assertEqual(response, payLoad)

        expected = '{}'
        response = self.zc.delete(path, contentFormat,tokenString)
        print("\t*deleted: " + payLoad)
        self.assertEqual(response, "")

        response = self.zc.get(path, contentFormat,tokenString)
        print("\t*read: " + response)
        self.assertEqual(response,'{}')


if __name__ == '__main__':
    unittest.main()
