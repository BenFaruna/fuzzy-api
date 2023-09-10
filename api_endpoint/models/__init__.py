from api_endpoint.main import app, engine
from api_endpoint.models.person import Base

with app.app_context():
    Base.metadata.create_all(bind=engine)
