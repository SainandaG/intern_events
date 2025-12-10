from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.organization_m import Organization
from app.models.branch_m import Branch
from app.models.role_m import Role
from app.models.menu_m import Menu
from app.models.user_m import User
from app.models.role_right_m import RoleRight
from app.utils.password_utils import hash_password


def seed_database():
    db = SessionLocal()

    try:
        if db.query(Organization).first():
            print("Database already seeded!")
            return

        # ============================
        # Organization
        # ============================
        org = Organization(
            name="Evination",
            code="EVI",
            email="info@evi.com",
            phone="1234567890",
            created_by="system",
        )
        db.add(org)
        db.flush()

        # ============================
        # Branch
        # ============================
        branch = Branch(
            organization_id=org.id,
            name="Head Office",
            code="HO",
            is_head_office=1,
            city="Bangalore",
            created_by="system",
        )
        db.add(branch)
        db.flush()

        # ============================
        # Roles
        # ============================
        super_admin_role = Role(
            name="Super Admin",
            code="SUPERADMIN",
            description="Full system access",
            created_by="system",
        )

        admin_role = Role(
            name="Admin",
            code="ADMIN",
            created_by="system"
        )

        vendor_role = Role(
            name="Vendor",
            code="VENDOR",
            created_by="system"
        )

        db.add(super_admin_role)
        db.add(admin_role)
        db.add(vendor_role)
        db.flush()

        # ============================
        # Menus
        # ============================
        menus_data = [
            {"name": "Dashboard", "code": "DASHBOARD", "icon": "dashboard", "route": "/dashboard"},
            {"name": "Organization", "code": "ORGANIZATION", "icon": "building", "route": "/organization"},
            {"name": "Branches", "code": "BRANCHES", "icon": "map-pin", "route": "/organization/branches"},
            {"name": "Roles", "code": "ROLES", "icon": "shield", "route": "/organization/roles"},
            {"name": "Users", "code": "USERS", "icon": "users", "route": "/organization/users"},
            {"name": "Vendors", "code": "VENDORS", "icon": "store", "route": "/vendors"},
            {"name": "Events", "code": "EVENTS", "icon": "calendar", "route": "/events"},
            {"name": "Bidding", "code": "BIDDING", "icon": "activity", "route": "/bidding"},
            {"name": "Orders", "code": "ORDERS", "icon": "shopping-cart", "route": "/orders"},
            {"name": "Reports", "code": "REPORTS", "icon": "bar-chart", "route": "/reports"},
        ]

        menu_objects = []
        for data in menus_data:
            menu = Menu(**data, created_by="system")
            db.add(menu)
            menu_objects.append(menu)

        db.flush()

        # ============================
        # Super Admin user
        # ============================
        admin_user = User(
            organization_id=org.id,
            branch_id=branch.id,
            role_id=super_admin_role.id,
            username="admin",
            email="admin@evination.com",
            password_hash=hash_password("admin123"),
            first_name="Super",
            last_name="Admin",
            created_by="system",
        )

        db.add(admin_user)
        db.flush()

        # Assign menus to superadmin (full rights)
        for menu in menu_objects:
            db.add(
                RoleRight(
                    role_id=super_admin_role.id,
                    menu_id=menu.id,
                    can_view=True,
                    can_create=True,
                    can_edit=True,
                    can_delete=True,
                    created_by="system",
                )
            )

        db.commit()

        print("✨ Database seeded successfully!")
        print("👤 Login credentials: admin / admin123")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
