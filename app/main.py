from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.routes import auth_route, user_route, organization_route, branch_route, role_route, menu_route

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Evination FastAPI Application",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_route.router, prefix="/api")
app.include_router(user_route.router, prefix="/api")
app.include_router(organization_route.router, prefix="/api")
app.include_router(branch_route.router, prefix="/api")
app.include_router(role_route.router, prefix="/api")
app.include_router(menu_route.router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI MVP",
        "version": settings.APP_VERSION,
        "docs": "/api/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.APP_VERSION}