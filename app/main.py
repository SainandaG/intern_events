from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings

# DB
from app.database import engine, Base
from app.seeders.seed_data import seed_database
from app.seeders.category_event_type_seeder import seed_categories_and_event_types
# Core Admin Routes
from app.routes import (
    auth_route,
    user_route,
    organization_route,
    branch_route,
    role_route,
    menu_route,
    category_route,  # NEW
    event_type_route,  # NEW
    event_route,  # NEW
    event_manager_route  # NEW
)


# Vendor Routes
from app.routes.vendor_auth_route import router as vendor_auth_router
from app.routes.vendor_profile_route import router as vendor_profile_router
from app.routes.vendor_dashboard_route import router as vendor_dashboard_router

# Admin Bidding Routes (NEW)
from app.routes.admin_bidding_route import router as admin_bidding_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("🚀 Application startup: Running seeders...")
    seed_database()
    seed_categories_and_event_types()

    yield

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Evination FastAPI Application",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)
    
# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Modify later for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# ROUTES REGISTRATION
# -------------------------

# ---- Core Admin APIs ----
app.include_router(auth_route.router, prefix="/api")
app.include_router(user_route.router, prefix="/api")
app.include_router(organization_route.router, prefix="/api")
app.include_router(branch_route.router, prefix="/api")
app.include_router(role_route.router, prefix="/api")
app.include_router(menu_route.router, prefix="/api")

app.include_router(category_route.router, prefix="/api")  # NEW
app.include_router(event_type_route.router, prefix="/api")  # NEW
app.include_router(event_route.router, prefix="/api")  # NEW
app.include_router(event_manager_route.router, prefix="/api")  # NEW

# ---- Vendor APIs ----
app.include_router(vendor_auth_router, prefix="/api")
app.include_router(vendor_profile_router, prefix="/api")
app.include_router(vendor_dashboard_router, prefix="/api")

# ---- Admin Bidding APIs ----
app.include_router(admin_bidding_router, prefix="/api")


# -------------------------
# HEALTH / ROOT
# -------------------------
@app.get("/")
async def root():
    return {
        "message": "Welcome to Evenation API",
        "version": settings.APP_VERSION,
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}
