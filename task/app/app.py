import os
import sys
from flask import Flask, jsonify,abort, make_response, request

app = Flask(__name__)


#####  Temp datastorage #####

tem_db = [
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
  },
  {
    "name": "datacenter-2",
    "metadata": {
      "monitoring": {
        "enabled": "true"
      },
      "limits": {
        "cpu": {
          "enabled": "true",
          "value": "250m"
        }
      }
    }
  }
]
#########check temp_db name #######

def get_temp_db(name):
    for config in tem_db:
        if config['name'] == name:
            return config

#########search in tem_db name #######

def search_config(name):

    result = []
    val = str(name.values())
    key = str(name.keys())
    #print('1',val,file=sys.stderr)
    #print(len(val))
    if len(val) < 18:
        abort(400)
    if "dict_keys(['metadata.limits.cpu.enabled'])" == key:
        flag = 2
    elif "dict_keys(['metadata.monitoring.enabled'])" == key:
        flag = 1
    elif "dict_keys(['name'])" == key:
        flag = 0
    else:
        abort(400)
    val = val.split('\'')[1]
  
   
    for iteam in tem_db:
            
        if iteam['metadata']['limits']['cpu']['enabled'] == val and flag == 2:
            result.append(iteam)
        if iteam['metadata']['monitoring']['enabled'] == val and flag == 1:
            result.append(iteam)   
        if iteam['name'] == val and flag == 0:
            result.append(iteam)

    return result

#########json_validate #####

def json_validate(name):
    monitoring = name['metadata']['monitoring']['enabled']
    cpu_e = name['metadata']['limits']['cpu']['enabled']
    cpu_v = name['metadata']['limits']['cpu']['value']
    return monitoring, cpu_e, cpu_v

#########check existing record in tem_db name #######

def check_record_exists(name):
    for config in tem_db:
        if config['name'] == name:
            return config

######### GET ########

@app.route('/configs', methods=['GET'])
def get_configs():
    return jsonify(tem_db), 200

######### GET LIST ALL ########

@app.route('/configs/<string:name>', methods=['GET'])
def get_config(name):
    config = get_temp_db(name)
    if not config:
            abort(404)
    return jsonify(config), 200

######## POST #############

@app.route('/configs', methods=['POST'])
def create_config():
    #### map json response ####
    monitoring, cpu_e, cpu_v = json_validate(request.json)
    name = request.json['name']
    flag_m = 0
    flag_e = 0
   
   # validate json response #####
    if not request.json or 'name' not in request.json:
        abort(400)
    
    if check_record_exists(name):
        abort(400)
    
    if len(name) == 0:
        abort(400)
    
    if len(cpu_v) == 0:
        #print('3',file=sys.stderr)
        abort(400)
    
    if monitoring == 'true' or monitoring == 'false':
        #print('1',monitoring,file=sys.stderr)
        flag_m = 1 
    if cpu_e == 'true' or cpu_e == 'false':
        flag_e = 1
        #print('2',cpu_e,file=sys.stderr)      
    
    if flag_m == 1 and flag_e == 1:
        tem_db.append(request.json)
        return jsonify(request.json) , 201
    else:
        abort(400)
         


###### PUT #########

@app.route('/configs/<string:name>', methods=['PUT'])
def update_config(name):
    config = get_temp_db(name)
    print(config, file=sys.stderr)
    if config is None:
        abort(404)
    if not request.json:
        abort(400)
    if not check_record_exists(name):
        abort(404)
    #### map json response ####
    name = request.json['name']
    monitoring, cpu_e, cpu_v = json_validate(request.json)
    flag_m = 0
    flag_e = 0

    # validate json response #####
    if len(cpu_v) == 0:
        abort(400)

    if monitoring == 'true' or monitoring == 'false':
        config['metadata']['monitoring']['enabled'] = monitoring
        flag_m = 1
    
    if cpu_e == 'true' or cpu_e == 'false':
        flag_e = 1
    
    if flag_e == 1 and flag_m == 1:
        config['metadata']['limits']['cpu']['enabled'] = cpu_e
        config['metadata']['limits']['cpu']['value'] = cpu_v
        config['name'] = name
        return jsonify(config), 200
    else:
        abort(400)


###### DELETE ########

@app.route('/configs/<string:name>', methods=['DELETE'])
def delete_config(name):
    config = get_temp_db(name)
    if config is None:
        abort(404)
    tem_db.remove(config)
    return jsonify({}), 204      

####### SEARCH ######

@app.route('/search', methods=['GET'])
def get_search():
    #print(request.args,file=sys.stderr)

    args = request.args
    args = args.to_dict()
    
    config = search_config(args)

    #if config is None:
    if len(config) == 0:
        abort(404)

    return jsonify(config), 200


### error messages #####

NOT_FOUND = 'Not Found'
BAD_REQUEST = 'Bad Request'

@app.errorhandler(404)
def not_found(error):
        return make_response(jsonify({'error': NOT_FOUND}), 404)

@app.errorhandler(400)
def bad_request(error):
        return make_response(jsonify({'error': BAD_REQUEST}), 400)

if __name__ == '__main__':
        try:
                if  os.environ['SERVE_PORT']:
                       app.run(debug=True, host='0.0.0.0', port=int(os.environ['SERVE_PORT']))
        except Exception as e:
                print("ERROR: SERVE_PORT not set as an env variable")
