from sqlalchemy.orm import Session
from Models import UserModel, RoleModel, UserRoleModel, SessionLocal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_db(db: Session):
    # Seed roles
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

    # Seed users
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

    # Seed user roles (admin gets admin, user gets user)
    user_role_pairs = [
        (user_objs[0], role_objs[0]),  # admin -> admin
        (user_objs[1], role_objs[1])   # user -> user
    ]
    for user, role in user_role_pairs:
        if not db.query(UserRoleModel).filter_by(user_id=user.id, role_id=role.id).first():
            user_role = UserRoleModel(user_id=user.id, role_id=role.id)
            db.add(user_role)
            db.commit()

    print("Database seeded successfully.")
    
if __name__ == "__main__":
    db = SessionLocal()
    seed_db(db)
    db.close()
