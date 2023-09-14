from api_endpoint.models.person import Base
from api_endpoint.main import app, engine

with app.app_context():
    Base.metadata.create_all(bind=engine)
