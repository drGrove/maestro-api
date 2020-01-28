from datetime import datetime
import enum

from .. import db

class DeployStatus(enum.Enum):
    UNKNOWN = 'unknown'
    PENDING = 'pending'
    RUNNING = 'running'
    FAILED = 'failed'
    COMPLETED = 'completed'


class Deploy(db.Model):
    __tablename__ = 'deployments'
    id = db.Column(db.Integer, primary_key=True)
    build_number = db.Column(db.Integer)
    repo_id = db.Column(
        db.Integer,
        db.ForeignKey('repositories.id'),
        nullable=False
    )
    config = db.Column(db.Text, index=False, nullable=False)
    env = db.Column(db.String(100), index=True, nullable=False)
    status = db.Column(db.Enum(DeployStatus), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    completed = db.Column(db.DateTime, nullable=True)
    last_updated = db.Column(db.DateTime, onupdate=datetime.now)

    def __repr__(self):
        return f'<Deploy {self.id}>'

    def to_dict(self):
        return {
            "id": self.id,
            "build_number": self.build_number,
            "repo": self.repo,
            "config": self.config,
            "status": self.status,
            "completed": datetime.timestamp(self.completed) or None,
            "created_at": datetime.timestamp(self.created_at),
            "last_updated": datetime.timestamp(self.last_updated)
        }
