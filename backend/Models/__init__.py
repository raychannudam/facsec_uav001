import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DB_CONNECTION_URL = os.environ.get('DB_CONNECTION_URL')

engine = create_engine(DB_CONNECTION_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from Models.Users import UserModel  # Import User model to ensure it's registered with Base
from Models.Roles import RoleModel  # Import Role model to ensure it's registered with Base
from Models.UsersRoles import UserRoleModel  # Import association table to ensure it's registered with Base
from Models.MqttClients import MqttClientModel  # Import MQTT Client model to ensure it's registered with Base
from Models.MqttTopics import MqttTopicModel  # Import MQTT Topic model to ensure it's registered with Base
from Models.StreamingClients import StreamingClientModel  # Import Streaming Client model to ensure it's registered with Base
from Models.StreamingUrls import StreamingUrlModel  # Import Streaming URL model to ensure it's registered with Base
from Models.Uavs import UavModel  # Import UAV model to ensure it's registered with Base
from Models.Stations import StationModel  # Import Station model to ensure it's registered with Base