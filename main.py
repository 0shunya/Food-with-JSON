from flask import Flask, jsonify, request
import json

app = Flask(__name__)


JSON_FILE_PATH = 'foods.json'


def read_json():
    try:
        with open(JSON_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def write_json(data):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)


foods = read_json()

@app.route('/foods', methods=['GET'])                                 
def get_foods():
    return jsonify(foods)

@app.route('/foods/<int:id>', methods=['GET'])                        
def get_food(id):
    food = next((food for food in foods if food["Id"] == id), None)
    return jsonify(food) if food else ("Food not found", 404)

@app.route('/foods', methods=['POST'])                                
def add_food():
    new_food = request.get_json()
    foods.append(new_food)
    write_json(foods)
    return jsonify(new_food), 201

@app.route('/foods/<int:id>', methods=['PUT'])                        
def update_food(id):
    food = next((food for food in foods if food["Id"] == id), None)
    if food:
        updated_data = request.get_json()
        food.update(updated_data)
        write_json(foods)
        return jsonify(food)
    else:
        return ("Food not found", 404)

@app.route('/foods/<int:id>', methods=['DELETE'])                     
def delete_food(id):
    global foods
    foods = [food for food in foods if food["Id"] != id]
    write_json(foods)
    return "", 204

if __name__ == '__main__':
    app.run(debug=True)
