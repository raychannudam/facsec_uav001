from Models import Base, engine
from Routes.User import router as user_router
from Routes.Role import router as role_router
from Routes.MqttClient import router as mqtt_client_router
from Routes.MqttTopic import router as mqtt_topic_router
from Routes.StreamingClient import router as streaming_client_router
from Routes.StreamingUrl import router as streaming_url_router
from Routes.Station import router as station_router
from Routes.Uav import router as uav_router
from Security.jwt import router as security_router
from Security.jwt import require_roles
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # You can restrict later to e.g. ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router, prefix="/api/v1", tags=["users"])
app.include_router(role_router, prefix="/api/v1", tags=["roles"], dependencies=[Depends(require_roles("admin"))])
app.include_router(mqtt_client_router, prefix="/api/v1", tags=["mqtt_clients"])
app.include_router(mqtt_topic_router, prefix="/api/v1", tags=["mqtt_topics"])
app.include_router(streaming_client_router, prefix="/api/v1", tags=["streaming_clients"])
app.include_router(streaming_url_router, prefix="/api/v1", tags=["streaming_urls"])
app.include_router(station_router, prefix="/api/v1", tags=["stations"])
app.include_router(uav_router, prefix="/api/v1", tags=["uavs"])
app.include_router(security_router, prefix="/api/v1", tags=["security"])

Base.metadata.create_all(bind=engine)


