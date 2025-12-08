from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Organization, Branch, Role, Menu, User
from app.database import Base
from app.utils.password_utils import hash_password

def seed_database():
    db = SessionLocal()
    
    try:
        if db.query(Organization).first():
            print("Database already seeded!")
            return
        
        # Create Organization
        org = Organization(
            name="Evination",
            code="EVI",
            email="info@evi.com",
            phone="1234567890",
            created_by="system"
        )
        db.add(org)
        db.flush()
        
        # Create Branch
        branch = Branch(
            organization_id=org.id,
            name="Head Office",
            code="HO",
            is_head_office=1,
            city="Bangalore",
            created_by="system"
        )
        db.add(branch)
        db.flush()
        
        # Create Roles
        roles_data = [
            {"name": "Admin", "code": "ADMIN", "description": "Administrative access"}
        ]
        
        roles = []
        for role_data in roles_data:
            role = Role(**role_data, created_by="system")
            db.add(role)
            roles.append(role)
        db.flush()
        
        # Create Menus
        menus_data = [
            # Main Menus
            {"name": "Dashboard", "code": "DASHBOARD", "icon": "dashboard", "route": "/dashboard", "menu_type": "main", "sort_order": 1},
            {"name": "Users", "code": "USERS", "icon": "users", "route": "/users", "menu_type": "main", "sort_order": 2},
            {"name": "Organizations", "code": "ORGANIZATIONS", "icon": "building", "route": "/organizations", "menu_type": "main", "sort_order": 3},
            {"name": "Branches", "code": "BRANCHES", "icon": "map-pin", "route": "/branches", "menu_type": "main", "sort_order": 4},
            {"name": "Roles", "code": "ROLES", "icon": "shield", "route": "/roles", "menu_type": "main", "sort_order": 5},
            {"name": "Settings", "code": "SETTINGS", "icon": "settings", "route": "/settings", "menu_type": "main", "sort_order": 6},
        ]
        
        for menu_data in menus_data:
            menu = Menu(**menu_data, created_by="system")
            db.add(menu)
        db.flush()
        
        # Create Admin User
        admin_user = User(
            organization_id=org.id,
            branch_id=branch.id,
            role_id=roles[0].id,
            username="admin",
            email="admin@mycompany.com",
            password_hash=hash_password("admin123"),
            first_name="Admin",
            last_name="*",
            phone="9876543210",
            created_by="system"
        )
        db.add(admin_user)
        
        db.commit()
        print("✅ Database seeded successfully!")
        print("👤 Admin credentials: username=admin, password=admin123")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()