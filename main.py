from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.config import settings
from backend.database import connect_to_mongo, close_mongo_connection
from backend.routers import auth, health, food, admin, calculators, gamification, pdf_export
import os



# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered personal diet and fitness planner using medical reports"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # Allow all origins for the hackathon to avoid any CORS blockers
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Event handlers
@app.on_event("startup")
async def startup_db_client():
    try:
        await connect_to_mongo()
        print(f"Connected to MongoDB: {settings.MONGODB_URL}")
    except Exception as e:
        print(f"FAILED to connect to MongoDB: {str(e)}")
        print("Backend will continue to run but database operations will fail.")
    
    # Create upload directory
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    print(f"{settings.APP_NAME} v{settings.APP_VERSION} started successfully!")


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()


# API Health Check - MUST be before static files mount
@app.get("/api/health-check")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# Include routers - all API routes
app.include_router(auth.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(food.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(calculators.router, prefix="/api")
app.include_router(gamification.router, prefix="/api")
app.include_router(gamification.router, prefix="/api")
app.include_router(pdf_export.router, prefix="/api")

# Register Outbreak Router
from backend.routers import outbreak
app.include_router(outbreak.router, prefix="/api")

# Register Health Card Router
from backend.routers import health_card
app.include_router(health_card.router, prefix="/api")


# Mount static files LAST (catch-all for frontend)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

if os.path.exists(FRONTEND_DIR):
    # Support direct access to assets like /js/config.js even if not in root
    # app.mount("/css", StaticFiles(directory=os.path.join(FRONTEND_DIR, "css")), name="css")
    # app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND_DIR, "js")), name="js")
    # app.mount("/pages", StaticFiles(directory=os.path.join(FRONTEND_DIR, "pages")), name="pages")
    
    # Mount uploads directory to serve food images and reports
    UPLOAD_DIR_ABS = os.path.abspath(settings.UPLOAD_DIR)
    app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR_ABS), name="uploads")
    
    # app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

@app.get("/")
async def root():
    return {
        "message": "NutriFit AI Backend API is running.",
        "docs": "/docs",
        "frontend": settings.FRONTEND_URL
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
