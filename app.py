import os
import urllib.parse as up
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import psycopg2
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)

db_connection_settings = {
    "dbname": "jtpxneqc",
    "user": "jtpxneqc",
    "password": 'tE3eD8jJcOwtZ-wsPsXFbDI9RTFXqN7p',
    "host": "castor.db.elephantsql.com",
    "port": "5432",
}

class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255))
    logo = db.Column(db.String(255))
    resource = db.Column(db.String(255))
    url = db.Column(db.String(255))

    def __init__(self, resource, category, url, logo):
        self.resource = resource
        self.category = category
        self.url = url
        self.logo = logo

class WebsiteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Website

# Class where the guide is inheriting from db.model and setting up to be able to send data to the Database using JSON

class Website(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    resource = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    logo = db.Column(db.String, nullable=False)

    def __init__(self, resource, category, url, logo):
        self.resource = resource
        self.category = category
        self.url = url
        self.logo = logo

class WebsiteSchema(ma.Schema):
    class Meta:
        fields = ("id", "resource", "category", "url", "logo")

website_schema =  WebsiteSchema()
multiple_website_schema = WebsiteSchema(many=True)

conn = psycopg2.connect(**db_connection_settings)

def insert_website(json_data_list):
    try:
        conn =  psycopg2.connect(**db_connection_settings)
        cursor =  conn.cursor()
        # Extract values from JSON data
        for json_data in json_data_list:
            id = json_data.get("id") 
            category = json_data.get("category")
            logo = json_data.get("logo")
            resource = json_data.get("resource")
            url = json_data.get("url")
            

            # SQL command to insert data into the "website" table
            sql_command = """
                INSERT INTO website (id,category, logo, resource, url)
                VALUES (%s, %s, %s, %s, %s)
            """

            # Execute the SQL command with the extracted values
            cursor.execute(sql_command, (id,category, logo, resource, url))

        # Commit the changes
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return {"message": "Website added successfully!"}, 201
    except Exception as e:
        return {"error": str(e)}, 500 

#API for inputting website via JSON
        #Endpoint for sending Website data to create tables in the DB
@app.route("/api/getWebsites", method=["POST"])
def add_websites():
    try:
        json_data_list = request.json
        response, status_code = insert_website(json_data_list)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500







##Everything below is part of an older build of this Python please disregard
# Endpoints for the API The below endpoint is used to add one website to the database
@app.route("/website/add", methods=["POST"])
def add_website():
    if request.content_type != "application/json":
        return "Error: Data must be sent as JSON."

    post_data = request.get_json(force=True)
    resource = post_data.get("resource")
    category = post_data.get("category")
    url = post_data.get("url")
    logo = post_data.get("logo")

    record = Website(resource, category, url, logo)
    db.session.add(record)
    db.session.commit()

    return jsonify("Resource Addedd Successfully")

# This endpoint is used to add multiple website in the database at once
@app.route("/website/add/multiple", methods=["POST"])
def add_multiple_websites():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")

    post_data = request.get_json(force=True)
    for website in post_data:
        record = Website(website["resource"],website["category"],website["url"],website["logo"])
        db.session.add(record)

    db.session.commit()

    return jsonify("All Resources Added Successfully")
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
    return jsonify("Resource Deleted Successfully")

# This is allowing the file to run which is just boilerplate code
if __name__ == "__main__":
    app.run(debug=True)


