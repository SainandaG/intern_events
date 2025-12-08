from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.menu_schema import MenuCreate, MenuResponse
from app.models.menu_m import Menu
from app.models.user_m import User
from app.dependencies import get_current_active_user

router = APIRouter(prefix="/menus", tags=["Menus"])

@router.post("/", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
async def create_menu(
    menu: MenuCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    db_menu = db.query(Menu).filter(Menu.code == menu.code).first()
    if db_menu:
        raise HTTPException(status_code=400, detail="Menu code already exists")
    
    new_menu = Menu(**menu.dict(), created_by=current_user.username)
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu

@router.get("/", response_model=List[MenuResponse])
async def get_menus(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    menus = db.query(Menu).filter(Menu.inactive == False).order_by(Menu.sort_order).offset(skip).limit(limit).all()
    return menus

@router.get("/hierarchy", response_model=List[dict])
async def get_menu_hierarchy(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    main_menus = db.query(Menu).filter(
        Menu.parent_id == None,
        Menu.inactive == False
    ).order_by(Menu.sort_order).all()
    
    def build_hierarchy(parent_id):
        children = db.query(Menu).filter(
            Menu.parent_id == parent_id,
            Menu.inactive == False
        ).order_by(Menu.sort_order).all()
        
        result = []
        for child in children:
            menu_dict = {
                "id": child.id,
                "name": child.name,
                "code": child.code,
                "icon": child.icon,
                "route": child.route,
                "menu_type": child.menu_type,
                "children": build_hierarchy(child.id)
            }
            result.append(menu_dict)
        return result
    
    hierarchy = []
    for menu in main_menus:
        menu_dict = {
            "id": menu.id,
            "name": menu.name,
            "code": menu.code,
            "icon": menu.icon,
            "route": menu.route,
            "menu_type": menu.menu_type,
            "children": build_hierarchy(menu.id)
        }
        hierarchy.append(menu_dict)
    
    return hierarchy