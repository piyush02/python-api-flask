import os
from flask import Flask, jsonify, abort, request, g
import sqlite3

app = Flask(__name__)

DATABASE = 'config_database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

class ConfigDatabase:
    def __init__(self):
        self.create_table()

    def create_table(self):
        with app.app_context():
            cursor = get_db().cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS configs (
                    name TEXT PRIMARY KEY,
                    monitoring_enabled TEXT,
                    cpu_enabled TEXT,
                    cpu_value TEXT
                )
            ''')
            get_db().commit()

    def get_all_configs(self):
        with app.app_context():
            cursor = get_db().cursor()
            cursor.execute('SELECT * FROM configs')
            return cursor.fetchall()

    def get_config(self, name):
        with app.app_context():
            cursor = get_db().cursor()
            cursor.execute('SELECT * FROM configs WHERE name = ?', (name,))
            return cursor.fetchone()

    def create_config(self, config):
        with app.app_context():
            cursor = get_db().cursor()
            cursor.execute('INSERT INTO configs VALUES (?, ?, ?, ?)', 
                           (config['name'], config['metadata']['monitoring']['enabled'],
                            config['metadata']['limits']['cpu']['enabled'], config['metadata']['limits']['cpu']['value']))
            get_db().commit()

    def update_config(self, config):
        with app.app_context():
            cursor = get_db().cursor()
            cursor.execute('''
                UPDATE configs
                SET monitoring_enabled = ?, cpu_enabled = ?, cpu_value = ?
                WHERE name = ?
            ''', (config['metadata']['monitoring']['enabled'], config['metadata']['limits']['cpu']['enabled'],
                  config['metadata']['limits']['cpu']['value'], config['name']))
            get_db().commit()

    def delete_config(self, name):
        with app.app_context():
            cursor = get_db().cursor()
            cursor.execute('DELETE FROM configs WHERE name = ?', (name,))
            get_db().commit()

config_db = ConfigDatabase()

@app.route('/configs', methods=['GET'])
def get_configs():
    return jsonify(config_db.get_all_configs()), 200

@app.route('/configs/<string:name>', methods=['GET'])
def get_config(name):
    config = config_db.get_config(name)
    if not config:
        abort(404)
    return jsonify(config), 200

@app.route('/configs', methods=['POST'])
def create_config():
    config = request.json
    if not config or 'name' not in config:
        abort(400)
    
    existing_config = config_db.get_config(config['name'])
    if existing_config:
        abort(400)
    
    config_db.create_config(config)
    return jsonify(config), 201

@app.route('/configs/<string:name>', methods=['PUT'])
def update_or_create_config(name):
    existing_config = config_db.get_config(name)

    if not request.json:
        abort(400)

    new_config_data = request.json
    new_config_data['name'] = name  # Ensure the name is set correctly

    if existing_config:
        # If the configuration already exists, update it
        config_db.update_config(new_config_data)
        return jsonify(new_config_data), 200
    else:
        # If the configuration doesn't exist, create a new one
        config_db.create_config(new_config_data)
        return jsonify(new_config_data), 201

@app.route('/configs/<string:name>', methods=['DELETE'])
def delete_config(name):
    config = config_db.get_config(name)
    if not config:
        abort(404)
    
    config_db.delete_config(name)
    return jsonify({}), 204

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('SERVE_PORT', 5000)))
