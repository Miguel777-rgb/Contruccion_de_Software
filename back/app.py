from flask import Flask, request, jsonify
import re

# 1. Initialize Flask application (Vital for @app to work)
app = Flask(__name__)

tasks = []  # store tasks in memory
users = []  # store users in memory
next_task_id = 0  # variable to assign unique IDs to tasks

# Function to validate postal code
def validate_postal_code(postal_code):
    """Validates that the postal code has exactly 5 digits"""
    return bool(re.match(r'^\d{5}$', postal_code))

@app.route("/about")
def about():
    return "This is the About page"

@app.route("/hello/<name>")
def hello(name):
    if name == "Igor":
        return "By the way, my name is Igor!"
    return f"Hello {name}!"

# Base route - To avoid 404 error when entering localhost
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Tasks API", 
        "instructions": "Use the /tasks route to view, create, edit or delete tasks."
    })

# GET - retrieve all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks})

# GET - single task
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        return jsonify({"task": task})
    return jsonify({"error": "Task not found"}), 404

# POST - add a new task
@app.route("/tasks", methods=["POST"])
def add_task():
    global next_task_id
    if not request.is_json or request.json is None:
        return jsonify({"error": "The request body must be valid JSON"}), 400
    data = request.json
    task = {
        "id": next_task_id, 
        "content": data.get("content", "No content"),
        "done": data.get("done", False)
    }
    tasks.append(task)
    next_task_id += 1
    return jsonify({"message": "Task added!", "task": task}), 201

# PUT - update a task by ID
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    if task_id >= len(tasks) or task_id < 0:
        return jsonify({"error": "Task not found"}), 404
    data = request.json
    tasks[task_id]["content"] = data.get("content", tasks[task_id]["content"])
    new_done_value = data.get("done", tasks[task_id].get("done", False))
    if not isinstance(new_done_value, bool):
        return jsonify({"error": "The 'done' field must be a boolean (true/false)"}), 400
    tasks[task_id]["done"] = new_done_value
    return jsonify({"message": "Task updated!", "task": tasks[task_id]})

# DELETE - delete a task by ID
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id >= len(tasks) or task_id < 0:
        return jsonify({"error": "Task not found"}), 404
    removed = tasks.pop(task_id)
    return jsonify({"message": "Task deleted!", "task": removed})

# User management routes

# GET - retrieve all users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify({"users": users})

# GET - retrieve single user by ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    # Search for user matching the ID
    user = next((u for u in users if u["id"] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": user})

# POST - create new user with address validation
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    
    # Validates that there is data
    if not data:
        return jsonify({"error": "JSON data is required"}), 400
    
    # Extract address only once
    address_data = data.get("address", {})
    postal_code = address_data.get("postal_code", "")
    
    # Validates postal code
    if postal_code and not validate_postal_code(postal_code):
        return jsonify({"error": "The postal code must contain exactly 5 digits"}), 400
    
    # Builds the address object
    address = {
        "city": address_data.get("city", ""),
        "country": address_data.get("country", ""),
        "postal_code": postal_code
    }
    
    # Generate a safe ID (finds highest ID and adds 1)
    new_id = 1 if not users else max(u["id"] for u in users) + 1
    
    user = {
        "id": new_id,
        "name": data.get("name", ""),
        "lastname": data.get("lastname", ""),
        "address": address
    }
    users.append(user)
    return jsonify({"message": "User created successfully!", "user": user}), 201

# PUT - update user by ID 
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
        
    data = request.json
    
    # Updates only the fields that come in the request
    user["name"] = data.get("name", user["name"])
    user["lastname"] = data.get("lastname", user["lastname"])
    
    # If a new address was sent, update it
    if "address" in data:
        user["address"] = data["address"]
        
    return jsonify({"message": "User updated!", "user": user})

# DELETE - delete user by ID
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users 
    user = next((u for u in users if u["id"] == user_id), None)
    if user is None:
        return jsonify({"error": "User not found"}), 404
        
    # Restructure list to exclude the deleted user
    users = [u for u in users if u["id"] != user_id]
    
    return jsonify({"message": "User deleted!", "user": user})

# 2. Start server on port 5000
if __name__ == "__main__":
    app.run(debug=True, port=5000)