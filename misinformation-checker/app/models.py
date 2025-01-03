from app import db
from datetime import datetime

class MisinformationResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    misinformation_score = db.Column(db.Float, nullable=False)
    classification = db.Column(db.String(50), nullable=False)
    fact_check_results = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
