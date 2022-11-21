from copy import deepcopy
import unittest
import json
import sys
sys.path.append('app/')
import app


API_ENDPOINT = 'http://127.0.0.1:5000/configs'
API_SEARCH_URL = 'http://127.0.0.1:5000/search?'
EXIST_API_ENDPOINT = '{}/datacenter-1'.format(API_ENDPOINT)
NONEXIST_API_ENDPOINT = '{}/datacenter-7'.format(API_ENDPOINT)

class TestApi(unittest.TestCase):

    def setUp(self):
        self.backup_configs = deepcopy(app.tem_db)  # Backup of current temp data
        self.app = app.app.test_client()
        self.app.testing = True


########## Get testcase ##########
        # Get all data
    def test_to_get_all(self):
        response = self.app.get(API_ENDPOINT)
        self.assertEqual(response.status_code, 200)
        # get non existing data
    def test_item_not_exist(self):
        response = self.app.get(NONEXIST_API_ENDPOINT)
        self.assertEqual(response.status_code, 404)
        # get one data
    def test_to_get_one(self):
        response = self.app.get(EXIST_API_ENDPOINT)
        self.assertEqual(response.status_code, 200)


######### POST tastcase ##########
        # post with missung name key & value
    def test_post_missing_name(self):
        item = {"name":"","metadata":{"monitoring":{"enabled":"true"},"limits":{"cpu":{"enabled":"false","value":"300m"}}}}
        response = self.app.post(API_ENDPOINT,data=json.dumps(item),content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # post missing value in json
    def test_post_missing_monitoring_value(self):
        item = {"name":"datacenter-1","metadata":{"monitoring":{"enabled":""},"limits":{"cpu":{"enabled":"false","value":"300m"}}}}
        response = self.app.post(API_ENDPOINT,data=json.dumps(item),content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # post missing value in json
    def test_post_missing_value(self):
        item = {"name":"datacenter-1","metadata":{"monitoring":{"enabled":"true"},"limits":{"cpu":{"enabled":"false","value":""}}}}
        response = self.app.post(API_ENDPOINT,data=json.dumps(item),content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # post new data to validate
    def test_post_accurate_data(self): 
        item = {"name":"datacenter-4","metadata":{"monitoring":{"enabled":"true"},"limits":{"cpu":{"enabled":"false","value":"300m"}}}}
        response = self.app.post(API_ENDPOINT,data=json.dumps(item),content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['name'], 'datacenter-4')
        self.assertEqual(data['metadata']['monitoring']['enabled'], 'true')
        self.assertEqual(data['metadata']['limits']['cpu']['enabled'], 'false')
        self.assertEqual(data['metadata']['limits']['cpu']['value'], '300m')
        # post existing data
    def test_post_existing_data(self):
        item = {"name":"datacenter-1","metadata":{"monitoring":{"enabled":"true"},"limits":{"cpu":{"enabled":"false","value":"300m"}}}}
        response = self.app.post(API_ENDPOINT,data=json.dumps(item),content_type='application/json')
        self.assertEqual(response.status_code, 400)

########## PUT testcase ##########
        # Update existing record with misisng value
    def test_put_for_existing_with_missing_value(self):
        item = {"name":"datacenter-2","metadata":{"monitoring":{"enabled":"true"},"limits":{"cpu":{"enabled":"f","value":"2m"}}}}
        response = self.app.put(EXIST_API_ENDPOINT,data=json.dumps(item),content_type='application/json')
        self.assertEqual(response.status_code, 400)   
        # Update existing record
    def test_put_for_existing_config(self):
        item = {"name":"datacenter-1","metadata":{"monitoring":{"enabled":"true"},"limits":{"cpu":{"enabled":"false","value":"500m"}}}}
        response = self.app.put(EXIST_API_ENDPOINT,data=json.dumps(item),content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['metadata']['limits']['cpu']['value'], "500m")
        self.assertEqual(self.backup_configs[0]['metadata']['limits']['cpu']['value'], "300m")  # old value
       # Update non existing record 
    def test_put_for_non_existing_record(self):
        item = {"name":"datacenter-5","metadata":{"monitoring":{"enabled":"true"},"limits":{"cpu":{"enabled":"false","value":"300m"}}}}
        response = self.app.put(NONEXIST_API_ENDPOINT,data=json.dumps(item),content_type='application/json')
        self.assertEqual(response.status_code, 404) 

######### Search testcase ##########
        # search with bad request
    def test_search_with_bad_value(self):
        response = self.app.get(API_SEARCH_URL + "metadata.monitoring")
        self.assertEqual(response.status_code, 400)
        # search with accurate value
    def test_search_with_accurate_value(self):
        response = self.app.get(API_SEARCH_URL + "metadata.monitoring.enabled=true")
        self.assertEqual(response.status_code, 200)
        # create new record and search 
    def test_search_create_record(self):
        item = {"name":"datacenter-4","metadata":{"monitoring":{"enabled":"false"},"limits":{"cpu":{"enabled":"false","value":"300m"}}}}
        response = self.app.post(API_ENDPOINT,data=json.dumps(item),content_type='application/json')
        response = self.app.get(API_SEARCH_URL + "name=datacenter-4")
        self.assertEqual(response.status_code, 200)
        # search with non existing record
    def test_search_non_existing_value(self):
        response = self.app.get(API_SEARCH_URL + "name=datacenter-8")
        self.assertEqual(response.status_code, 404)       
        # search with mssing key
    def test_search_with_bad_cpu_value(self):
        response = self.app.get(API_SEARCH_URL + "metadata.limits.cpu.value=")
        self.assertEqual(response.status_code, 400)


######### Delete testcase ##########
        ########## delete non existing record #########
    def test_delete_absent_entry(self):
        response = self.app.delete(API_ENDPOINT + "/datacenter-3")
        self.assertEqual(response.status_code, 404)
    def test_delete_present_entry(self):
        ######### Create a new record
        item = {"name":"datacenter-4","metadata":{"monitoring":{"enabled":"true"},"limits":{"cpu":{"enabled":"false","value":"300m"}}}}
        response = self.app.post(API_ENDPOINT,data=json.dumps(item),content_type='application/json')
        self.assertEqual(response.status_code, 201)
        #### Delete new record
        response = self.app.delete(API_ENDPOINT + "/datacenter-4")
        self.assertEqual(response.status_code, 204)
        #### Delete existing record
        response = self.app.delete(API_ENDPOINT + "/datacenter-2")
        self.assertEqual(response.status_code, 204)
        #### test delete wrong endpoint
    def test_delete_absent_entry(self):
        response = self.app.delete(API_ENDPOINT)
        self.assertEqual(response.status_code, 405)
    

if __name__ == "__main__":
    unittest.main()

