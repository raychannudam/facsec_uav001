from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models import get_db, RoleModel
from Schemas.Role import RoleCreateSchema, RoleUpdateSchema, RoleResponseSchema
from Services.Role import RoleService

router = APIRouter()

# Create Role
@router.post("/roles", response_model=RoleResponseSchema)
def create_role(role: RoleCreateSchema, db: Session = Depends(get_db)):
	new_role = RoleService.create_role(role.dict(), db)
	return RoleResponseSchema(
		id=new_role.id,
		name=new_role.name,
		description=new_role.description,
		created_at=str(new_role.created_at),
		updated_at=str(new_role.updated_at)
	)

# Get all Roles
@router.get("/roles", response_model=list[RoleResponseSchema])
def get_roles(db: Session = Depends(get_db)):
	roles = RoleService.get_roles(db)
	return [RoleResponseSchema(
		id=r.id,
		name=r.name,
		description=r.description,
		created_at=str(r.created_at),
		updated_at=str(r.updated_at)
	) for r in roles]

# Get Role by ID
@router.get("/roles/{role_id}", response_model=RoleResponseSchema)
def get_role(role_id: int, db: Session = Depends(get_db)):
	role = RoleService.get_role_by_id(role_id, db)
	if not role:
		raise HTTPException(status_code=404, detail="Role not found")
	return RoleResponseSchema(
		id=role.id,
		name=role.name,
		description=role.description,
		created_at=str(role.created_at),
		updated_at=str(role.updated_at)
	)

# Update Role
@router.put("/roles/{role_id}", response_model=RoleResponseSchema)
def update_role(role_id: int, role_update: RoleUpdateSchema, db: Session = Depends(get_db)):
	update_data = {k: v for k, v in role_update.dict().items() if v is not None}
	role = RoleService.update_role(role_id, update_data, db)
	if not role:
		raise HTTPException(status_code=404, detail="Role not found")
	return RoleResponseSchema(
		id=role.id,
		name=role.name,
		description=role.description,
		created_at=str(role.created_at),
		updated_at=str(role.updated_at)
	)

# Delete Role
@router.delete("/roles/{role_id}", response_model=RoleResponseSchema)
def delete_role(role_id: int, db: Session = Depends(get_db)):
	role = RoleService.delete_role(role_id, db)
	if not role:
		raise HTTPException(status_code=404, detail="Role not found")
	return RoleResponseSchema(
		id=role.id,
		name=role.name,
		description=role.description,
		created_at=str(role.created_at),
		updated_at=str(role.updated_at)
	)
