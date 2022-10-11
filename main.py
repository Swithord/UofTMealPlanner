from flask import Flask, render_template, request, flash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

meal_plans = {'A': 5415, 'B': 5620, 'C': 5945, 'D': 6430}

@app.route('/',  methods=('GET', 'POST'))
def index():
    spending = {'required': 0, 'current': 0}
    error = None
    if request.method == 'POST':
        active = True
        if request.form['start_date']:
            try:
                start_date = datetime.strptime(request.form['start_date'], '%d%m%Y').date()
            except ValueError:
                flash('Start date must be a valid string')
                active = False
        else:
            start_date = datetime.strptime('03092022', '%d%m%Y').date()
        if request.form['end_date']:
            try:
                end_date = datetime.strptime(request.form['end_date'], '%d%m%Y').date()
            except ValueError:
                flash('End date must be a valid string')
                active = False
        else:
            end_date = datetime.strptime('28042023', '%d%m%Y').date()
        now_date = datetime.now().date()
        date_modifier = -18
        if not is_float(request.form['current_balance']):
            flash('Current balance must a valid number')
            active = False
        if active:
            current_balance = float(request.form['current_balance'])
            print(request.form)
            start_balance = meal_plans[request.form.get('meal_plan')]
            if start_balance >= current_balance:
                spending = {'required': str(round(money_over_time(current_balance, now_date, end_date, date_modifier), 2)),
                            'current': str(round(money_over_time(start_balance - current_balance, start_date, now_date, 0), 2))}
            else:
                flash('Current balance cannot be greater than meal plan value')

    return render_template('index.html', spending=spending, error=error, data=[{'meal_plan':'A'}, {'meal_plan':'B'}, {'meal_plan':'C'}, {'meal_plan': 'D'}])


def time_difference(start, end, modifier):
  duration = str(end - start)
  return int(duration[0:duration.find(' d')]) + modifier


def money_over_time(money, start, end, modifier):
  return money / time_difference(start, end, modifier)


def is_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
