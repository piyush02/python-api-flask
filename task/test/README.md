### Flask unit test script for checking api endpoint

Below liberary used for testing 
- unittest


### Prerequisites
- python3

### Below API JSON Formate tested 
{
	"name": "datacenter-1",
	"metadata": {
		"monitoring": {
			"enabled": "true"
		},
		"limits": {
			"cpu": {
				"enabled": "false",
				"value": "300m"
			}
		}
	}
} 
###

Key	                        |  Required       |         Type
---			        |  ---        	  |         ---
name				|    Yes	  |	    String
metadata.monitoring.enabled	|    Yes	  |	    Boolean
metadata.limits.cpu.enabled	|    Yes	  |	    Boolean
metadata.limits.cpu.value	|    Yes	  |	    String

### Usage 
Note: Run the test script from task directory
'''
python3 test/flask_unit_test.py -v
test_delete_absent_entry (__main__.TestApi) ... ok
test_delete_present_entry (__main__.TestApi) ... ok
test_item_not_exist (__main__.TestApi) ... ok
test_post_accurate_data (__main__.TestApi) ... ok
test_post_existing_data (__main__.TestApi) ... ok
test_post_missing_monitoring_value (__main__.TestApi) ... ok
test_post_missing_name (__main__.TestApi) ... ok
test_post_missing_value (__main__.TestApi) ... ok
test_put_for_existing_config (__main__.TestApi) ... {'name': 'datacenter-1', 'metadata': {'monitoring': {'enabled': 'true'}, 'limits': {'cpu': {'enabled': 'false', 'value': '300m'}}}}
ok
test_put_for_existing_with_missing_value (__main__.TestApi) ... {'name': 'datacenter-1', 'metadata': {'monitoring': {'enabled': 'true'}, 'limits': {'cpu': {'enabled': 'false', 'value': '500m'}}}}
ok
test_put_for_non_existing_record (__main__.TestApi) ... None
ok
test_search_create_record (__main__.TestApi) ... ok
test_search_non_existing_value (__main__.TestApi) ... ok
test_search_with_accurate_value (__main__.TestApi) ... ok
test_search_with_bad_cpu_value (__main__.TestApi) ... ok
test_search_with_bad_value (__main__.TestApi) ... ok
test_to_get_all (__main__.TestApi) ... ok
test_to_get_one (__main__.TestApi) ... ok

----------------------------------------------------------------------
Ran 18 tests in 0.010s

OK
'''

Test Covered:-

##GET
- GET all records
- GET non existing records
- GET one record

## POST
- POST with missing 'name field' value  
- POST with missing value of metadata.monitoring.enabled 
- POST with missing value of metadata.limits.cpu.value 
- POST with correct record
- POST existing record

## PUT
- PUT update non existing record
- PUT update existing record with missing values
- PUT update existing record

## Search
- Search query with wrong endpoint
- Search query with correct endpoint
- Search create new reacord and query the same
- Search query non existing record
- Search query with missing value in endpoint

## DELETE
- DELETE non existing record
- DELETE create new record and delete the same record, Quey recently deleted record
- DELETE wrong endpoint
