from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///E:/group8/test.db'  # 更改为你想要的路径
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
    if request.method == 'POST':
        name = request.form['vote-name']
        start_time = request.form['start-time']
        end_time = request.form['end-time']
        vote = Vote(name=name, start_time=start_time, end_time=end_time)
        db.session.add(vote)
        db.session.commit()
        return redirect(url_for('vote_results', vote_id=vote.id))
    return render_template('vote_management.html')

@app.route('/vote_results/<int:vote_id>', methods=['GET', 'POST'])
def vote_results(vote_id):
    vote = Vote.query.get(vote_id)
    if request.method == 'POST':
        if request.form['vote'] == 'yes':
            vote.yes_votes += 1
        else:
            vote.no_votes += 1
        db.session.commit()
    return render_template('vote_results.html', vote=vote)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)  # 尝试使用5001或其他未被使用的端口


