from crypt import methods
from flask import Flask, render_template, request
from mileage import check_activities, athlete_info
from weight import athlete_weights, add_weight, change_weight, change_date, remove_weight

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
    return "Weight added successfully!"

@app.route('/edit_weight', methods=['POST'])
def edit_weight():
    date = request.form["date"]
    old_weight = str(request.form["old_weight"])
    new_weight = str(request.form["new_weight"])
    unit = request.form["unit"]
    if unit == "kg":
        new_weight = str(kg_to_lbs(weight)) # convert to lbs if unit is kg    
    #change_weight(["1", date, old_weight], ["1", date, new_weight])
    return "Weight edited successfully!"
    
def kg_to_lbs(weight):
    return weight / 0.453592

if __name__ == '__main__':
    app.run(debug=True)
