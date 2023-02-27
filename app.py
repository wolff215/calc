from flask import Flask, render_template, request
from calc import check_activities, athlete_info, athlete_weights, add_weight

app = Flask(__name__)

@app.route('/')
@app.route('/mileage')
def mileage():
    entries = check_activities()
    athlete = athlete_info()
    return render_template('mileage.html', entries=entries, athlete=athlete)

@app.route('/weight')
def weight():
    weights = athlete_weights()
    athlete = athlete_info()
    return render_template('weight.html', athlete=athlete, weights=weights)

@app.route('/add_weight', methods=['POST'])
def add_wgt():
    date = request.form["date"]
    weight = float(request.form["weight"])
    unit = request.form["unit"]
    if unit == "kg":
        weight = kg_to_lbs(weight) # convert to lbs if unit is kg    
    add_weight([1,date,weight])
    return "Weight added successfully"
    
def kg_to_lbs(weight):
    return weight / 0.453592

if __name__ == '__main__':
    app.run(debug=True)
