from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserRead, UserLogin
from app.db.models import User
from app.db.session import get_db
from app.core.security import hash_password, verify_password,create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    # 1. Check if user already exists
    existing_user = db.query(User).filter(
        User.email == user_in.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # 2. Hash password
    hashed_pw = hash_password(user_in.password)

    # 3. Create ORM user
    user = User(
        email=user_in.email,
        hashed_password=hashed_pw
    )

    # 4. Save to DB
    db.add(user)
    db.commit()
    db.refresh(user)

    # 5. Return user (FastAPI → UserRead)
    return user

@router.post("/login")
def login_user(
    user_in : UserLogin,
    db : Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email"
        )
    
    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid password"
        )
    
    access_token = create_access_token(
        data= {"sub":str(user.id)}
    )

    return {
        "access_token":access_token,
        "token_type":"bearer"
    }
    

