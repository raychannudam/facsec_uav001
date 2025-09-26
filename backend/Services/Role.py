
from sqlalchemy.orm import Session
from Models import RoleModel

class RoleService:
	@staticmethod
	def create_role(role_data: dict, db: Session):
		role = RoleModel(**role_data)
		db.add(role)
		db.commit()
		db.refresh(role)
		return role

	@staticmethod
	def get_roles(db: Session):
		return db.query(RoleModel).all()

	@staticmethod
	def get_role_by_id(role_id: int, db: Session):
		return db.query(RoleModel).filter(RoleModel.id == role_id).first()

	@staticmethod
	def update_role(role_id: int, update_data: dict, db: Session):
		role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
		if not role:
			return None
		for key, value in update_data.items():
			setattr(role, key, value)
		db.commit()
		db.refresh(role)
		return role

	@staticmethod
	def delete_role(role_id: int, db: Session):
		role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
		if not role:
			return None
		db.delete(role)
		db.commit()
		return role
