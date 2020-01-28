from datetime import datetime

from .. import db


class Repository(db.Model):
    __tablename__ = 'repositories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    url = db.Column(db.String(1000))
    deployments = db.relationship('Deploy', backref='repositories', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_updated = db.Column(db.DateTime, onupdate=datetime.now)

    def __repr__(self):
        return f'<Repository {self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "created_at": datatime.timestamp(self.created_at),
            "last_updated": datetime.timestamp(self.last_updated)
        }
