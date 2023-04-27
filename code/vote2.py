from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/petertesting/Desktop/group8-main77/test.db'  # 更改为你想要的路径
db = SQLAlchemy(app)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    yes_votes = db.Column(db.Integer, default=0)
    no_votes = db.Column(db.Integer, default=0)

@app.route('/', methods=['GET', 'POST'])
def vote_management():
    print(',,,,')
    if request.method == 'POST':
        print('sadasdsadasdasdasdasd')
        name = request.form['vote-name']
        # start_time = request.form['start-time']
        # end_time = request.form['end-time']
        start_time = datetime.strptime(request.form['start-time'], '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(request.form['end-time'], '%Y-%m-%dT%H:%M')
        vote = Vote(name=name, start_time=start_time, end_time=end_time)
        db.session.add(vote)
        db.session.commit()
        print('this_id',vote.id)
        return redirect(url_for('vote_results', vote_id=vote.id))
    return render_template('vote_manage.html')

@app.route('/vote_results/<int:vote_id>', methods=['GET', 'POST'])
def vote_results(vote_id):
    vote = Vote.query.get(vote_id)
    print(vote)
    if request.method == 'POST':
        print(request.form.get('vote'))
        form_data = request.form.to_dict()
        print(form_data)
        if request.form.get('vote') == 'yes':
            print(request.form)
            vote.yes_votes += 1
        else:
            print(request.form)
            vote.no_votes += 1
        db.session.commit()
    return render_template('vote_result.html', vote=vote)

if __name__ == '__main__':
    print('run')
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5004)  # 尝试使用5001或其他未被使用的端口