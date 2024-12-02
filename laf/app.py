from flask import Flask, render_template
from blueprints.items_bp import items_bp
from blueprints.post_item_bp import post_item_bp
from blueprints.contact_us_bp import contact_us_bp
from blueprints.admin_bp import admin_bp

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'lafISUCC'

app.register_blueprint(items_bp)
app.register_blueprint(post_item_bp)
app.register_blueprint(contact_us_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about_us')
def about_us():
    return render_template("about_us.html")

if __name__ == "__main__":
    app.run(debug=True)