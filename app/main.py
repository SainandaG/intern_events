from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base

from app.routes import (
    auth_route,
    user_route,
    organization_route,
    branch_route,
    role_route,
    menu_route,
)

# Vendor
from app.routes.vendor_auth_route import router as vendor_auth_router
from app.routes.vendor_profile_route import router as vendor_profile_router
from app.routes.vendor_dashboard_route import router as vendor_dashboard_router

# Category
from app.routes.category_route import router as category_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Evination FastAPI Application",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # allow frontend later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core
app.include_router(auth_route.router, prefix="/api")
app.include_router(user_route.router, prefix="/api")
app.include_router(organization_route.router, prefix="/api")
app.include_router(branch_route.router, prefix="/api")
app.include_router(role_route.router, prefix="/api")
app.include_router(menu_route.router, prefix="/api")

# Vendor
app.include_router(vendor_auth_router, prefix="/api")
app.include_router(vendor_profile_router, prefix="/api")
app.include_router(vendor_dashboard_router, prefix="/api")

# Category
app.include_router(category_router, prefix="/api")


@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI API",
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}
from app.routes.event_route import router as event_router
app.include_router(event_router)
