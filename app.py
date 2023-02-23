from flask import Flask, render_template
from calc import check_activities, athlete_info, athlete_weights

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

if __name__ == '__main__':
    app.run(debug=True)
