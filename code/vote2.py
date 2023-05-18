from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import os

base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, '../test.db')
app.config['SECRET_KEY'] = 'some-secret-key'

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


# def voting_control()



@app.route('/', methods=['GET', 'POST'])
def vote_management():
    print(',,,,')
    try:
        if request.method == 'POST':
            name = request.form['vote-name']
            print('copy')
            start_time = datetime.strptime(request.form['start-time'], '%Y-%m-%dT%H:%M')
            end_time = datetime.strptime(request.form['end-time'], '%Y-%m-%dT%H:%M')
            if check_later(start_time,end_time) and check_later(start_time,datetime.now()):
                active_votes = Vote.query.filter(Vote.start_time <= datetime.now(), Vote.end_time >= datetime.now()).all()
                # print(active_votes[0].id)
                if len(active_votes) < 3:
                    vote = Vote(name=name, start_time=start_time, end_time=end_time)
                    db.session.add(vote)
                    db.session.commit()
                    print('this_id',vote.id)
                    return redirect(url_for('vote_results', vote_id=vote.id))
                else:
                    flash("You can not have more than 3 active votes!")
                    return redirect(url_for('vote_management'))
            else:
                print("wrong")
                return redirect(url_for('show_alert'))

    except Exception as e:
        print(str(e))

        flash("Wrong data formation")
    return render_template('vote_manage.html')

@app.route('/get_vote/<int:index>', methods=['GET', 'POST'])

def get_vote(index):
    try:
        active_votes = Vote.query.filter(Vote.start_time <= datetime.now(), Vote.end_time >= datetime.now()).all()
        vote = active_votes[index-1]
        if request.method == 'POST' and vote.is_active():
            print(request.form.get('votingResult'))

            form_data = request.form.to_dict()
            print(form_data)

            if request.form.get('votingResult') == '1' or request.form.get('votingResult') == 'one':
                print(request.form)

                vote.yes_votes += 1
            else:
                print('?????')
                print(request.form)
                print(vote.no_votes)
                vote.no_votes += 1
            db.session.commit()

        # votes = Vote.query.all()
        # render_template('vote_result.html', vote=votes)
        # return 'cnm'
        return  '''<?xml version="1.0"?>
<vxml version="2.0" xmlns="http://www.w3.org/2001/vxml">
   <form>
      <block>
         <prompt>Thank you! Goodbye!</prompt>
      </block>
   </form>
</vxml>''', 200
    except Exception as e:
        print(str(e))
        print(str('The index should be no bigger than 3.'))


@app.route('/vote_results/<int:vote_id>', methods=['GET', 'POST'])
def vote_results(vote_id):
    # vote = Vote.query.get(vote_id)

    votes = Vote.query.all()
    # render_template('vote_result.html', vote=votes)
    # return 'cnm'
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
    app.run(host='0.0.0.0',debug=True, port=5004)