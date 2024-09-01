from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os
from deepface import DeepFace

app = Flask(__name__)

# הגדרת נתיב לתמונות
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# מאגר נתונים בזיכרון
users = {}
posts = []

# עמוד רישום
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob_day = request.form['dob_day']
        dob_month = request.form['dob_month']
        dob_year = request.form['dob_year']
        birth_date = f"{dob_day}/{dob_month}/{dob_year}"
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        image = request.files['image']

        # הדפסת פרטי המשתמש
        print("Received registration details:")
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Date of Birth: {birth_date}")
        print(f"Email: {email}")

        if image:
            image_filename = os.path.join(app.config['UPLOAD_FOLDER'], email + '.' + image.filename.split('.')[-1])
            image.save(image_filename)
            users[email] = {
                'first_name': first_name,
                'last_name': last_name,
                'birth_date': birth_date,
                'password': password,
                'image': image_filename
            }
            print(f"Image saved as: {image_filename}")

        return redirect(url_for('login'))

    return render_template('register.html')

# עמוד כניסה
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users.get(email)

        if user and check_password_hash(user['password'], password):
            return redirect(url_for('home'))
        else:
            return "Invalid credentials, please try again."

    return render_template('login.html')

# עמוד בית עם אפשרות להוסיף פוסט
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        occupation = request.form['occupation']
        description = request.form['description']
        image = request.files['image']

        # שמירת התמונה בתיקיית uploads
        if image:
            image_filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_filename)
            print(f"Post image saved as: {image_filename}")

        # שמירת פוסט
        posts.append({
            'name': name,
            'age': age,
            'city': city,
            'occupation': occupation,
            'description': description,
            'image': image_filename
        })

        return redirect(url_for('home'))

    return render_template('home.html', posts=posts)

# ניתוח תמונה לזיהוי פנים
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return "No image uploaded."

    image = request.files['image']
    
    # שמירת התמונה בתיקייה
    if image:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)

        # ניתוח התמונה עם DeepFace
        try:
            result = DeepFace.analyze(image_path, actions=['gender'])
            if result:
                gender_result = result[0]['gender']
                
                # עיגול התוצאות לשתי ספרות אחרי הנקודה
                formatted_gender_result = {k: f"{v:.2f}" for k, v in gender_result.items()}
                
                return f"Gender probabilities: {formatted_gender_result}"
            else:
                return "No face detected or analysis failed."
        except Exception as e:
            return f"An error occurred: {e}"

    return "Failed to process the image."

# הרצת השרת
if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
