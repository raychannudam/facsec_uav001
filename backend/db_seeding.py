from sqlalchemy.orm import Session
from Models import UserModel, RoleModel, UserRoleModel, ControllerModel, SessionLocal
from passlib.context import CryptContext
from datetime import datetime
from Services.MqttClient import MqttClientService
from Services.StreamingClient import StreamingClientService
from Schemas.MqttClient import MqttClientCreateSchema
from Schemas.StreamingClient import StreamingClientCreateSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed_db(db: Session):
    # --- Seed Roles ---
    roles = [
        {"name": "admin", "description": "Administrator"},
        {"name": "user", "description": "Regular User"}
    ]
    role_objs = []
    for role_data in roles:
        role = db.query(RoleModel).filter_by(name=role_data["name"]).first()
        if not role:
            role = RoleModel(**role_data)
            db.add(role)
            db.commit()
            db.refresh(role)
        role_objs.append(role)

    # --- Seed Users ---
    users = [
        {"username": "admin", "email": "admin@example.com", "password": pwd_context.hash("adminpass"), "fullname": "Admin User", "age": 30, "gender": "other"},
        {"username": "user", "email": "user@example.com", "password": pwd_context.hash("userpass"), "fullname": "Regular User", "age": 25, "gender": "other"}
    ]
    user_objs = []
    for user_data in users:
        user = db.query(UserModel).filter_by(username=user_data["username"]).first()
        if not user:
            user = UserModel(**user_data)
            db.add(user)
            db.commit()
            db.refresh(user)
        user_objs.append(user)

    # --- Seed User Roles ---
    user_role_pairs = [
        (user_objs[0], role_objs[0]),  # admin -> admin
        (user_objs[1], role_objs[1])   # user -> user
    ]
    for user, role in user_role_pairs:
        if not db.query(UserRoleModel).filter_by(user_id=user.id, role_id=role.id).first():
            user_role = UserRoleModel(user_id=user.id, role_id=role.id)
            db.add(user_role)
            db.commit()

    # --- Seed Default Controllers ---
    default_controllers = [
        {
            "name": "Admin Controller 1",
            "description": "Default controller for the admin account",
            "config": {
                "selectedDrone": {},
                "streamingUrls": [],
                "mqttTopics": [],
                "sliders": [],
                "toggles": [],
                "actions": []
            },
            "user": user_objs[0]
        },
        {
            "name": "User Controller 1",
            "description": "Default controller for the regular user",
            "config": {
                "selectedDrone": {},
                "streamingUrls": [],
                "mqttTopics": [],
                "sliders": [],
                "toggles": [],
                "actions": []
            },
            "user": user_objs[1]
        }
    ]

    for ctrl_data in default_controllers:
        existing = (
            db.query(ControllerModel)
            .filter_by(user_id=ctrl_data["user"].id, name=ctrl_data["name"])
            .first()
        )
        if not existing:
            controller = ControllerModel(
                user_id=ctrl_data["user"].id,
                name=ctrl_data["name"],
                description=ctrl_data["description"],
                config=ctrl_data["config"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            db.add(controller)
            db.commit()
            db.refresh(controller)

    # --- Seed Default MQTT Clients ---
    mqtt_clients = [
        {
            "user_id": user_objs[0].id,
            "name": "Admin MQTT Client 1",
            "description": "Default MQTT client for admin user",
            "username": "admin",
            "password": "adminpass",
            "config": {
                "broker": "localhost",
                "port": 1883,
                "qos": 1,
                "keepalive": 60
            },
            "status": True
        },
        {
            "user_id": user_objs[1].id,
            "name": "User MQTT Client 1",
            "description": "Default MQTT client for regular user",
            "username": "user",
            "password": "userpass",
            "config": {
                "broker": "localhost",
                "port": 1883,
                "qos": 1,
                "keepalive": 60
            },
            "status": True
        }
    ]
    
    for mqtt_data in mqtt_clients:
        existing_mqtt = MqttClientService.get_mqtt_clients_by_user(mqtt_data["user_id"], db)
        if not any(client.username == mqtt_data["username"] for client in existing_mqtt):
            mqtt_client_schema = MqttClientCreateSchema(**mqtt_data)
            MqttClientService.create_mqtt_client(mqtt_client_schema, db)

    # --- Seed Default Streaming Clients ---
    streaming_clients = [
        {
            "user_id": user_objs[0].id,
            "name": "Admin Streaming Client 1",
            "description": "Default streaming client for admin user",
            "username": "admin",
            "password": "adminpass",
            "config": {
                "protocol": "rtsp",
                "port": 8554,
                "quality": "high",
                "fps": 30
            },
            "status": True
        },
        {
            "user_id": user_objs[1].id,
            "name": "User Streaming Client 1",
            "description": "Default streaming client for regular user",
            "username": "user",
            "password": "userpass",
            "config": {
                "protocol": "rtsp",
                "port": 8554,
                "quality": "medium",
                "fps": 25
            },
            "status": True
        }
    ]
    
    for streaming_data in streaming_clients:
        existing_streaming = StreamingClientService.get_streaming_clients_by_user(streaming_data["user_id"], db)
        if not any(client.username == streaming_data["username"] for client in existing_streaming):
            streaming_client_schema = StreamingClientCreateSchema(**streaming_data)
            # Pass the correct user object for each streaming client
            user_obj = next((user for user in user_objs if user.id == streaming_data["user_id"]), None)
            if user_obj:
                StreamingClientService.create_streaming_client(streaming_client_schema, db, user_obj)

    print("✅ Database seeded successfully with users, roles, controllers, and clients for both admin and user.")


if __name__ == "__main__":
    db = SessionLocal()
    seed_db(db)
    db.close()