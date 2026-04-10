import sys
import os

# Add parent directory to Python path to enable imports from database folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from database.models import db, Task, User
from database import config
from datetime import datetime, timezone
import re

def create_app():
    # Configure Flask to look for templates and static files in parent directory
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../static'))
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    # Enable CORS for all routes
    CORS(app)

    # Load configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["SECRET_KEY"] = config.SECRET_KEY

    # Initialize database with app context
    db.init_app(app)

    # ---------- Health & Root ----------
    # Base route - Serve HTML file
    @app.route("/", methods=["GET"])
    def home():
        return render_template('index.html')

    @app.route("/healthz")
    def health():
        # Lightweight health check
        return jsonify({"status": "ok"}), 200

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

    # GET - retrieve all tasks with pagination and search (excluding soft-deleted)
    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        query = request.args.get('query', '', type=str)
        
        # Validate that page and limit are positive integers
        if page < 1 or limit < 1:
            return jsonify({"error": "page and limit must be positive integers"}), 400
        
        # Limit the maximum number of items per page to 100
        if limit > 100:
            limit = 100
        
        # Build query filter - exclude soft-deleted tasks
        task_query = Task.query.filter(Task.deleted_at.is_(None))
        if query:
            task_query = task_query.filter(Task.content.ilike(f"%{query}%"))
        
        paginated_tasks = task_query.paginate(page=page, per_page=limit, error_out=False)
        
        return jsonify({
            "tasks": [task.to_dict() for task in paginated_tasks.items],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": paginated_tasks.total,
                "pages": paginated_tasks.pages,
                "has_next": paginated_tasks.has_next,
                "has_prev": paginated_tasks.has_prev
            },
            "search": {
                "query": query if query else None
            }
        })

    # GET - single task (excluding soft-deleted)
    @app.route("/tasks/<int:task_id>", methods=["GET"])
    def get_task(task_id):
        task = Task.query.filter(Task.id == task_id, Task.deleted_at.is_(None)).first()
        if task:
            return jsonify({"task": task.to_dict()})
        return jsonify({"error": "Task not found"}), 404

    # POST - add a new task
    @app.route("/tasks", methods=["POST"])
    def add_task():
        if not request.is_json or request.json is None:
            return jsonify({"error": "The request body must be valid JSON"}), 400
        data = request.json
        
        # Validate user_id exists
        user_id = data.get("user_id")
        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
        
        user = User.query.get(user_id)
        if not user or user.deleted_at:
            return jsonify({"error": "User not found"}), 404
        
        task = Task(
            user_id=user_id,
            content=data.get("content", "No content"),
            done=data.get("done", False)
        )
        db.session.add(task)
        db.session.commit()
        return jsonify({"message": "Task added!", "task": task.to_dict()}), 201

    # PUT - update a task by ID (excluding soft-deleted)
    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    def update_task(task_id):
        task = Task.query.filter(Task.id == task_id, Task.deleted_at.is_(None)).first()
        if task is None:
            return jsonify({"error": "Task not found"}), 404
        data = request.json
        task.content = data.get("content", task.content)
        
        new_done_value = data.get("done", task.done)
        if not isinstance(new_done_value, bool):
            return jsonify({"error": "The 'done' field must be a boolean (true/false)"}), 400
        task.done = new_done_value
        
        # Update user_id if provided
        if "user_id" in data:
            new_user_id = data.get("user_id")
            if not new_user_id:
                return jsonify({"error": "user_id is required"}), 400
            
            user = User.query.get(new_user_id)
            if not user or user.deleted_at:
                return jsonify({"error": "User not found"}), 404
            
            task.user_id = new_user_id
        
        db.session.commit()
        return jsonify({"message": "Task updated!", "task": task.to_dict()})

    # DELETE - soft delete a task by ID (set deleted_at timestamp)
    @app.route("/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id):
        task = Task.query.filter(Task.id == task_id, Task.deleted_at.is_(None)).first()
        if task is None:
            return jsonify({"error": "Task not found"}), 404
        task_dict = task.to_dict()
        task.deleted_at = datetime.now(timezone.utc)
        db.session.commit()
        return jsonify({"message": "Task deleted!", "task": task_dict})

    # User management routes

    # ========== USER MANAGEMENT CRUD ENDPOINTS ==========
    
    # GET - retrieve all users (non-deleted)
    @app.route("/users", methods=["GET"])
    def get_users():
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        if page < 1 or limit < 1:
            return jsonify({"error": "page and limit must be positive integers"}), 400
        if limit > 100:
            limit = 100
        
        # Get non-deleted users with pagination
        paginated_users = User.query.filter(User.deleted_at.is_(None)).paginate(
            page=page, per_page=limit, error_out=False
        )
        
        return jsonify({
            "users": [user.to_dict() for user in paginated_users.items],
            "pagination": {
                "page": page,
                "limit": limit,
                "total": paginated_users.total,
                "pages": paginated_users.pages,
                "has_next": paginated_users.has_next,
                "has_prev": paginated_users.has_prev
            }
        })
    
    # GET - retrieve single user by ID with their tasks
    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        user = User.query.filter(User.id == user_id, User.deleted_at.is_(None)).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Get user's non-deleted tasks
        tasks = Task.query.filter(
            Task.user_id == user_id,
            Task.deleted_at.is_(None)
        ).all()
        
        user_data = user.to_dict()
        user_data["tasks"] = [task.to_dict() for task in tasks]
        
        return jsonify({"user": user_data})
    
    # POST - create new user with address info
    @app.route("/users", methods=["POST"])
    def create_user():
        if not request.is_json or request.json is None:
            return jsonify({"error": "JSON data is required"}), 400
        
        data = request.json
        name = data.get("name", "").strip()
        
        # Validation
        if not name:
            return jsonify({"error": "name is required"}), 400
        
        # Create user
        user = User(
            name=name,
            lastname=data.get("lastname", "").strip(),
            city=data.get("city", "").strip(),
            country=data.get("country", "").strip(),
            postal_code=data.get("postal_code", "").strip()
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            "message": "User created successfully!",
            "user": user.to_dict()
        }), 201
    
    # PUT - update user by ID
    @app.route("/users/<int:user_id>", methods=["PUT"])
    def update_user(user_id):
        user = User.query.filter(User.id == user_id, User.deleted_at.is_(None)).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if not request.is_json or request.json is None:
            return jsonify({"error": "JSON data is required"}), 400
        
        data = request.json
        
        # Update fields if provided
        if "name" in data:
            name = data["name"].strip()
            if name:
                user.name = name
        
        if "lastname" in data:
            user.lastname = data["lastname"].strip()
        
        if "city" in data:
            user.city = data["city"].strip()
        
        if "country" in data:
            user.country = data["country"].strip()
        
        if "postal_code" in data:
            user.postal_code = data["postal_code"].strip()
        
        db.session.commit()
        
        return jsonify({
            "message": "User updated!",
            "user": user.to_dict()
        })
    
    # DELETE - soft delete user by ID
    @app.route("/users/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        user = User.query.filter(User.id == user_id, User.deleted_at.is_(None)).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        # Soft delete user
        user.deleted_at = datetime.now(timezone.utc)
        db.session.commit()
        
        return jsonify({
            "message": "User deleted!",
            "user": user.to_dict()
        })
    
    # GET - retrieve available users for task assignment (simple list)
    @app.route("/users/available/list", methods=["GET"])
    def get_available_users():
        # Get all non-deleted users in simple format for dropdown/selection
        users = User.query.filter(User.deleted_at.is_(None)).all()
        return jsonify({
            "users": [
                {"id": u.id, "name": f"{u.name} {u.lastname or ''}".strip()}
                for u in users
            ]
        })

    # 2. Start server on port 5000
    return app  

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)