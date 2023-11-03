from .__init__ import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name