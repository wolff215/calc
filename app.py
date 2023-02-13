from flask import Flask, render_template
from calc import check_activities, athlete_info

app = Flask(__name__)

entries = check_activities()
athlete = athlete_info()

@app.route('/')
def index():
    return render_template('index.html', entries=entries, athlete=athlete)

if __name__ == '__main__':
    app.run(debug=True)
