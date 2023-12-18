from flask import Flask, request
from flask import jsonify


from supabase import create_client, Client
from werkzeug.security import generate_password_hash , check_password_hash

app = Flask(__name__)

url="https://eookpobfniytgmprafet.supabase.co"
key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVvb2twb2Jmbml5dGdtcHJhZmV0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDI1OTExMzcsImV4cCI6MjAxODE2NzEzN30.RcpPNSGpBC1Ji-iH7HpaXMC9Imkn-cs-MM_aUoBI01k"
supabase: Client = create_client(url, key)



@app.route('/users.signup', methods=['POST'])
def api_users_signup():
    name = request.form.get('name')
    phone_number = request.form.get('phone_number')
    password = request.form.get('password')

    if not name or not phone_number or not password:
        return jsonify({'status': 400, 'message': 'Name, phone number, and password are required'})

    hashed_password = generate_password_hash(password)

    user_exists = supabase.table('users').select("*").like('phone_number', phone_number).execute()
    if user_exists.data:
        return jsonify({'status': 400, 'message': 'User already exists'})

    response = supabase.table('users').insert([{"name": name, "phone_number": phone_number, "password": hashed_password}]).execute()
    if response.status_code != 200:
        return jsonify({'status': 500, 'message': 'Error creating the user'})

    return jsonify({'status': 200, 'message': 'User registered successfully'})


@app.route('/users.signin', methods=['POST'])
def api_users_login():
    phone_number = request.form.get('phone_number')
    password = request.form.get('password')

    if not phone_number or not password:
        return jsonify({'status': 400, 'message': 'Phone number and password are required'})

    user = supabase.table('users').select("*").ilike('phone_number', phone_number).execute().data
    if user and check_password_hash(user[0]['password'], password):
        return jsonify({'status': 200, 'message': 'Login successful', 'data': user[0]})
    else:
        return jsonify({'status': 401, 'message': 'Invalid phone number or password'})

@app.route('/users.signup.auth', methods=['POST'])
def api_users_signup_auth():
    phone_number = request.form.get('phone')  # Change 'email' to 'phone'
    password = request.form.get('password')
    response = supabase.auth.sign_up({"phone_number": phone_number, "password": password})
    print(str(response))
    return str(response)

if __name__ == '__main__':
    app.run(port=8080)


