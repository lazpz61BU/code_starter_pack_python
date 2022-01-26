from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



from flask_heroku import Heroku
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

# for Hosting
heroku = Heroku(app)
CORS(app)


# Class where the guide is inheriting from db.model and settign up to be able to send data to the Database using JSON

class Website(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    resource = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)

    def __init__(self, resource, category, url):
        self.resource = resource
        self.category = category
        self.url = url

class WebsiteSchema(ma.Schema):
    class Meta:
        fields = ("id", "resource", "category", "url")

website_schema =  WebsiteSchema()
multiple_website_schema = WebsiteSchema(many=True)


# Endpoints for the API The below endpoint is used to add one website to the database
@app.route("/website/add", methods=["POST"])
def add_website():
    if request.content_type != "application/json":
        return "Error: Data must be sent as JSON."

        post_data = request.get_json()
        resource = post_data.get("resource")
        category = post_data.get("category")
        url = post_data.get("url")

        record = Website(resource, category, url)
        db.session.add(record)
        db.session.commit()

        return jsonify("Resource Addedd Successfully")

# This endpoint is used to add multiple website in the database at once
@app.route("/website/add/multiple", methods=["POST"])
def add_multiple_websites():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")

    post_data = request.get_json()
    for website in post_date:
        record = Website(website["resource"],website["category"],website["url"])
        db.session.add(record)

    db.session.commit()

    return jsonify("All website added")

# This Endpoint is to get all of the websites being stored in the database
@app.route("/website/get", methods=["GET"])
def get_all_websites():
    
    all_websites = db.session.query(Website).all()
    return jsonify(multiple_website_schema.dump(all_websites))

# This is an endpoint to delete a website stored in the database
@app.route("/website/delete/<id>", methods=["DELETE"])
def delete_websites_by_id(id):
    website = db.session.query(Website).filter(Website.id == id).first()
    db.session.delete(website)
    db.session.commit()
    return jsonify("Website Deleted")

# This is allowing the file to run which is just boilerplate code
if __name__ == "__main__":
    app.run(debug=True)


