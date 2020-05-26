from datetime import datetime
import requests,os
from flask import Flask, jsonify, make_response
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

# init app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Covid19_Stats')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


# Model
class GlobalData(db.Model):
    __tablename__ = "results"
    id = db.Column(db.Integer, primary_key=True)
    total_cases = db.Column(db.Integer)
    total_recovered = db.Column(db.Integer)
    total_unresolved = db.Column(db.Integer)
    total_deaths = db.Column(db.Integer)
    total_new_cases_today = db.Column(db.Integer)
    total_new_deaths_today = db.Column(db.Integer)
    total_active_cases = db.Column(db.Integer)
    total_serious_cases = db.Column(db.Integer)
    total_affected_countries = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, total_cases, total_recovered, total_unresolved, total_deaths, total_new_cases_today,
                 total_new_deaths_today, total_active_cases, total_serious_cases, total_affected_countries):
        self.total_cases = total_cases
        self.total_recovered = total_recovered
        self.total_unresolved = total_unresolved
        self.total_deaths = total_deaths
        self.total_new_cases_today = total_new_cases_today
        self.total_new_deaths_today = total_new_deaths_today
        self.total_active_cases = total_active_cases
        self.total_serious_cases = total_serious_cases
        self.total_affected_countries = total_affected_countries

    def __repr__(self):
        return '' % self.id


db.create_all()


# Schema
class ResultsSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = GlobalData
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    total_cases = fields.Number(required=True)
    total_recovered = fields.Number(required=True)
    total_unresolved = fields.Number(required=True)
    total_deaths = fields.Number(required=True)
    total_new_cases_today = fields.Number(required=True)
    total_new_deaths_today = fields.Number(required=True)
    total_active_cases = fields.Number(required=True)
    total_serious_cases = fields.Number(required=True)
    total_affected_countries = fields.Number(required=True)


# Model
class RegionalData(db.Model):
    __tablename__ = "regions"
    id = db.Column(db.Integer, primary_key=True)
    iso = db.Column(db.String(20))
    name = db.Column(db.String(100))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, iso, name):
        self.iso = iso
        self.name = name

    def __repr__(self):
        return '' % self.id


db.create_all()


# Schema
class RegionSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = RegionalData
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    iso = fields.String(required=True)
    name = fields.String(required=True)


# Model
class MapData(db.Model):
    __tablename__ = "mapData"
    id = db.Column(db.Integer, primary_key=True)
    countrycode = db.Column(db.String(20))
    date = db.Column(db.Date())
    cases = db.Column(db.String(100))
    deaths = db.Column(db.String(100))
    recovered = db.Column(db.String(100))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, countrycode, date, cases, deaths, recovered):
        self.countrycode = countrycode
        self.date = date
        self.cases = cases
        self.deaths = deaths
        self.recovered = recovered

    def __repr__(self):
        return '' % self.id


db.create_all()


# Schema
class MapSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = RegionalData
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    contrycode = fields.String(required=True)
    date = fields.Date()
    cases = fields.String(required=True)
    deaths = fields.String(required=True)
    recovered = fields.String()


# init all Schema's
result_schema = ResultsSchema()
results_schema = ResultsSchema(many=True)

region_schema = RegionSchema()
regions_schema = RegionSchema(many=True)

map_schema = MapSchema()
maps_schema = MapSchema(many=True)

# API GET request to get data for global stats from public api and store in Database
@app.route('/results', methods=['GET'])
def results():
    r = requests.get('https://thevirustracker.com/free-api?global=stats')
    json_object = r.json()

    total_cases = json_object['results'][0]['total_cases']
    total_recovered = json_object['results'][0]['total_recovered']
    total_unresolved = json_object['results'][0]['total_unresolved']
    total_deaths = json_object['results'][0]['total_deaths']
    total_new_cases_today = json_object['results'][0]['total_new_cases_today']
    total_new_deaths_today = json_object['results'][0]['total_new_deaths_today']
    total_active_cases = json_object['results'][0]['total_active_cases']
    total_serious_cases = json_object['results'][0]['total_serious_cases']
    total_serious_cases = json_object['results'][0]['total_serious_cases']

    new_results = GlobalData(total_cases, total_recovered, total_unresolved, total_deaths, total_new_cases_today,
                             total_new_deaths_today, total_active_cases, total_serious_cases, total_serious_cases)

    db.session.add(new_results)
    db.session.commit()

    return results_schema.jsonify(new_results)


# API GET request to retrieve data from database for global stats
@app.route('/resultsoutput', methods=['GET'])
def resultsoutput():
    get_results = GlobalData.query.all()
    result_schema = ResultsSchema(many=True)
    results = result_schema.dump(get_results)
    return make_response(jsonify({"Results": results}))


# API GET request to get data for regions from public api and store in Database
@app.route('/regions', methods=['GET'])
def regions():
    r = requests.get('https://covid-api.com/api/regions')
    access_json = r.json()

    access_data = access_json['data']

    for data in access_data:
        db.session.add(RegionalData(iso=data['iso'], name=data['name']))
    db.session.commit()


# API GET request to retrieve data from database for regions
@app.route('/regionOutput', methods=['GET'])
def regionoutput():
    get_regions = RegionalData.query.all()
    region_schema = RegionSchema(many=True)
    data = region_schema.dump(get_regions)
    return make_response(jsonify({"Data": data}))


# API GET request to get data for mapData from public api and store in Database
@app.route('/maps', methods=['GET'])
def maps():
    r = requests.get('https://thevirustracker.com/timeline/map-data.json')
    access_json = r.json()

    access_data = access_json['data']

    for data in access_data:
        db.session.add(MapData(countrycode=data['countrycode'],
                               date=datetime.strptime(data['date'], '%m/%d/%y'),
                               cases=data['cases'], deaths=data['deaths'], recovered=data['recovered']))
    db.session.commit()


# API GET request to retrieve data from database for regions
@app.route('/mapOutput', methods=['GET'])
def mapoutput():
    get_mapData = MapData.query.all()
    map_schema = MapSchema(many=True)
    data = map_schema.dump(get_mapData)
    return make_response(jsonify({"Data": data}))


# Run server
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)

