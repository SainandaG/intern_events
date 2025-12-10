from .base_model import BaseModel
from .organization_m import Organization
from .branch_m import Branch
from .department_m import Department
from .user_m import User
from .role_m import Role
from .role_right_m import RoleRight
from .menu_m import Menu
from .attachment_m import Attachment
from .audit_log_m import AuditLog
from .settings_m import Settings

# EVENT + Category must be imported here
from .category_m import Category
from .event_m import Event
from .event_category_m import EventCategory

# DO NOT IMPORT vendor models here !!
# They auto-register because routes import them and SQLAlchemy discovers them.

__all__ = [
    "BaseModel",
    "Organization",
    "Branch",
    "Department",
    "User",
    "Role",
    "RoleRight",
    "Menu",
    "Attachment",
    "AuditLog",
    "Settings",
    "Category",
    "Event",
    "EventCategory",
]
