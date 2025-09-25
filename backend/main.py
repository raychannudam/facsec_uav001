from Models import Base, engine
from Routes.User import router as user_router
from Routes.Role import router as role_router
from Security.jwt import router as security_router
from Security.jwt import require_roles
from fastapi import FastAPI, Depends

app = FastAPI()
app.include_router(user_router, prefix="/api/v1", tags=["users"])
app.include_router(role_router, prefix="/api/v1", tags=["roles"], dependencies=[Depends(require_roles("admin"))])
app.include_router(security_router, prefix="/api/v1", tags=["security"])

Base.metadata.create_all(bind=engine)


