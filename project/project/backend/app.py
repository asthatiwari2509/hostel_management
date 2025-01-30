from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, decode_token
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)  # For simplicity, this allows all origins

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    registration_no = db.Column(db.String(20), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        # Validation for missing fields
        required_fields = ['first_name', 'last_name', 'email', 'registration_no', 'phone', 'password']
        for field in required_fields:
            if field not in data or not data[field].strip():
                return jsonify({'message': f'Missing or empty field: {field}'}), 400

        # Check for duplicate entries                               
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 409
        if User.query.filter_by(phone=data['phone']).first():
            return jsonify({'message': 'Phone number already exists'}), 409
        if User.query.filter_by(registration_no=data['registration_no']).first():
            return jsonify({'message': 'Registration number already exists'}), 409

        # Save password as plain text and create the user
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            registration_no=data['registration_no'],
            phone=data['phone'],
            password=data['password']  # Plain text password
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@app.route('/login', methods=['POST'])
\
def login():
    try:
        data = request.json
        # Find the user by email (using the correct key 'email')
        user = User.query.filter_by(email=data['email']).first()

        # Check if user exists and passwords match
        if user and user.password == data['password']:  # Compare password directly
            return jsonify({'message': 'Login successful!'}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/onboarding', methods=['GET', 'PUT'])
def onboarding():
    try:
        # Handle GET request: Fetch user details based on email
        if request.method == 'GET':
            email = request.args.get('email')  # Get the email from query parameters
            if not email:
                return jsonify({'message': 'Email is required'}), 400

            user = User.query.filter_by(email=email).first()
            if not user:
                return jsonify({'message': 'User not found'}), 404

            return jsonify({
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,  # Ensure email is returned
                'registration_no': user.registration_no,
                'phone': user.phone
            }), 200

        # Handle PUT request: Update user details based on email
        if request.method == 'PUT':
            data = request.json
            email = data.get('email')  # Get the email from the request body
            if not email:
                return jsonify({'message': 'Email is required'}), 400

            user = User.query.filter_by(email=email).first()
            if not user:
                return jsonify({'message': 'User not found'}), 404

            user.first_name = data.get('first_name', user.first_name)
            user.last_name = data.get('last_name', user.last_name)
            user.phone = data.get('phone', user.phone)
            if 'password' in data and data['password'].strip():
                user.password = data['password']  # Update with plain text password
            db.session.commit()
            return jsonify({'message': 'User details updated successfully'}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
