from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import os

base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, '../test.db')


db = SQLAlchemy(app)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    yes_votes = db.Column(db.Integer, default=0)
    no_votes = db.Column(db.Integer, default=0)
    def is_active(self):
        return self.start_time <= datetime.now() <= self.end_time




@app.route('/show_alert')
def show_alert():
    alert_message = "Please check the time!"
    return render_template('alert.html', message=alert_message)


@app.route('/', methods=['GET', 'POST'])
def vote_management():
    print(',,,,')
    if request.method == 'POST':
        name = request.form['vote-name']
        # start_time = request.form['start-time']
        # end_time = request.form['end-time']
        start_time = datetime.strptime(request.form['start-time'], '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(request.form['end-time'], '%Y-%m-%dT%H:%M')
        if check_later(start_time,end_time):
            vote = Vote(name=name, start_time=start_time, end_time=end_time)
            db.session.add(vote)
            db.session.commit()
            print('this_id',vote.id)
            return redirect(url_for('vote_results', vote_id=vote.id))
        else:
            print("wrong")
            return redirect(url_for('show_alert'))

    return render_template('vote_manage.html')

@app.route('/vote_results/<int:vote_id>', methods=['GET', 'POST'])
def vote_results(vote_id):
    vote = Vote.query.get(vote_id)
    if request.method == 'POST' and vote.is_active():
        print(request.form.get('vote'))

        form_data = request.form.to_dict()
        print(form_data)

        if request.form.get('votingResult') == '1' or 'one':
            print(request.form)
            vote.yes_votes += 1
        else:
            print(request.form)
            vote.no_votes += 1
        db.session.commit()

    votes = Vote.query.all()

    return render_template('vote_result.html', vote=votes)


def check_later(time1,time2):
    return (time2 > time1)

# def check_time(vote):
#     current_time = datetime.now()
#     print(vote.start_time <= current_time <= vote.end_time)
#     return vote.start_time <= current_time <= vote.end_time



if __name__ == '__main__':
    print('run')
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5004)  # 尝试使用5001或其他未被使用的端口