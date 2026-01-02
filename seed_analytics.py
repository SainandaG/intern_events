import sys
import os
from datetime import datetime, timedelta
import random

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal
from app.models.base_model import Base
from app.models.user_m import User
from app.models.vendor_m import Vendor
from app.models.event_m import Event
from app.models.vendor_order_m import VendorOrder
from app.models.vendor_bid_m import VendorBid
from app.models.organization_m import Organization
from app.models.category_m import Category
from app.models.event_type_m import EventType
from sqlalchemy import text

db = SessionLocal()

def seed_analytics_data():
    print("🌱 Bootstrapping Roles...")
    db.execute(text("INSERT IGNORE INTO roles (id, name, code) VALUES (1, 'Admin', 'ADMIN'), (2, 'Vendor', 'VENDOR'), (3, 'Customer', 'CUSTOMER')"))
    db.commit()

    print("🌱 Creating master data...")
    org = db.query(Organization).filter_by(name="Default Org").first()
    if not org:
        org = Organization(name="Default Org", code="DEF-ORG", email="info@evination.com")
        db.add(org)
        db.commit()

    cats = [
        {"name": "Weddings", "code": "CAT-WED"},
        {"name": "Corporate", "code": "CAT-CORP"},
        {"name": "Birthdays", "code": "CAT-BIRT"},
        {"name": "Conferences", "code": "CAT-CONF"}
    ]
    cat_objs = []
    for c in cats:
        cat = db.query(Category).filter_by(name=c["name"]).first()
        if not cat:
            cat = Category(name=c["name"], code=c["code"])
            db.add(cat)
        cat_objs.append(cat)
    db.commit()

    types = [
        {"name": "Gala", "code": "TYPE-GALA"},
        {"name": "Seminar", "code": "TYPE-SEMI"},
        {"name": "Party", "code": "TYPE-PART"},
        {"name": "Reception", "code": "TYPE-RECE"}
    ]
    type_objs = []
    for t in types:
        et = db.query(EventType).filter_by(name=t["name"]).first()
        if not et:
            et = EventType(name=t["name"], code=t["code"], category_id=cat_objs[0].id)
            db.add(et)
        type_objs.append(et)
    db.commit()

    user = db.query(User).filter(User.email == 'admin@evination.com').first()
    if not user:
        user = User(
            username='admin_seed_' + str(random.randint(100,999)),
            email='admin@evination.com',
            password_hash='$2b$12$LQv3c1yqBWVHxkd0Lpue8.S7N3m6N59.6W/8vj.9d.6m7q8e.f.g.',
            first_name='Admin',
            last_name='User',
            role_id=1,
            organization_id=org.id
        )
        db.add(user)
        try:
            db.commit()
        except:
            db.rollback()
            user = db.query(User).filter(User.email == 'admin@evination.com').first()
    
    vendor = db.query(Vendor).filter(Vendor.user_id == user.id).first()
    if not vendor:
        vendor = Vendor(
            user_id=user.id,
            company_name="Elegant Caterers",
            offered_services=[],
            status="approved"
        )
        db.add(vendor)
        db.commit()

    print(f"🌱 Using Vendor ID: {vendor.id}")
    print("🌱 Seeding Events & Orders via RAW SQL...")
    
    for i in range(50):
        days_ago = random.randint(0, 365)
        dt = datetime.utcnow() - timedelta(days=days_ago)
        dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')
        
        status = "COMPLETED" if days_ago > 30 else "CONFIRMED"
        cat_id = random.choice(cat_objs).id
        type_id = random.choice(type_objs).id
        name = f"Event {i+1} - {random.choice(['Gala', 'Summit', 'Bash'])}"
        
        # Insert event
        sql = text("""
            INSERT INTO events (organization_id, name, category_id, event_type_id, event_date, status, required_services, created_at)
            VALUES (:org_id, :name, :cat_id, :type_id, :dt, :status, '[]', :dt)
        """)
        db.execute(sql, {"org_id": org.id, "name": name, "cat_id": cat_id, "type_id": type_id, "dt": dt_str, "status": status})
        db.commit()
        
        # Get last ID
        event_id = db.execute(text("SELECT LAST_INSERT_ID()")).scalar()
        
        if vendor:
            amount = float(random.randint(10000, 100000))
            order = VendorOrder(
                vendor_id=vendor.id,
                event_id=event_id,
                order_ref=f"ORD-SEED-{i}-{random.randint(10000,99999)}",
                amount=amount,
                status="confirmed",
                confirmed_at=dt,
                created_at=dt - timedelta(days=5)
            )
            db.add(order)
            
            bid = VendorBid(
                vendor_id=vendor.id,
                event_id=event_id,
                total_amount=amount,
                status="selected" if status == "COMPLETED" else "submitted",
                submitted_at=dt - timedelta(days=7),
                selected_at=dt
            )
            db.add(bid)

    db.commit()
    print("✅ Seeded 50 Events, Orders, and Bids.")

if __name__ == "__main__":
    try:
        seed_analytics_data()
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        db.close()
