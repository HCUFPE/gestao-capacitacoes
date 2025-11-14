
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Response, Request, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from starlette.concurrency import run_in_threadpool

from ..auth.auth import auth_handler, JWT_EXP_HOURS, REFRESH_TOKEN_EXP_DAYS
from ..resources.database import get_app_db_session
from ..controllers import usuario_controller # Import the new controller
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/api", tags=["Authentication"])

@router.post("/login")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    remember_me: bool = Form(False),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Logs in a user, synchronizes their data, returns a JWT access token, 
    and optionally sets an HttpOnly refresh token cookie.
    """
    try:
        # 1. Authenticate against Active Directory
        user_ad_info = await run_in_threadpool(auth_handler.authenticate_user, form_data.username, form_data.password)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {e}")

    # 2. Synchronize user data with the local database
    db_user = await usuario_controller.sincronizar_usuario(db, user_ad_info)

    # 3. Prepare data for JWT, including the profile from our database
    jwt_data = user_ad_info.copy()
    jwt_data["perfil"] = db_user.perfil.value # Add profile to the token payload

    access_token_expires = timedelta(minutes=15) if remember_me else timedelta(hours=JWT_EXP_HOURS)
    access_token = auth_handler.create_access_token(
        data=jwt_data,
        expires_delta=access_token_expires
    )

    if remember_me:
        refresh_token = await auth_handler.create_refresh_token(user_id=jwt_data["username"], groups=jwt_data.get("groups", []), db=db)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="lax",
            secure=True, # Should be True in production with HTTPS
            max_age=REFRESH_TOKEN_EXP_DAYS * 24 * 60 * 60 # Convert days to seconds
        )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token/refresh")
async def refresh_token(request: Request, response: Response, db: AsyncSession = Depends(get_app_db_session)):
    """
    Refreshes the access token using a valid refresh token from an HttpOnly cookie.
    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not found")

    token_obj = await auth_handler.verify_refresh_token(refresh_token, db)

    # 1. Get user's profile from the local database
    db_user = await usuario_controller.get_user_by_username(db, token_obj.user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found in local database after refresh token verification.")
    
    if not db_user.perfil:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User profile not found in local database.")

    # 2. Prepare data for JWT using information from the refresh token and local DB
    try:
        jwt_data = {
            "username": token_obj.user_id,
            "groups": token_obj.groups,
            "perfil": db_user.perfil.value,
            "displayName": db_user.nome,
            "email": db_user.email or "" # Ensure email is always a string
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error preparing JWT data: {e}")

    # Invalidate the old refresh token (implement rotation for better security)
    await auth_handler.invalidate_refresh_token(refresh_token, db)

    # Create a new access token (short-lived)
    try:
        new_access_token = auth_handler.create_access_token(
            data=jwt_data,
            expires_delta=timedelta(minutes=15)
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating new access token: {e}")

    # Create a new refresh token and set it as a new HttpOnly cookie
    new_refresh_token = await auth_handler.create_refresh_token(
        user_id=jwt_data["username"],
        groups=jwt_data["groups"],
        db=db
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        samesite="lax",
        secure=True, # Should be True in production with HTTPS
        max_age=REFRESH_TOKEN_EXP_DAYS * 24 * 60 * 60
    )

    return {"access_token": new_access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(response: Response, request: Request, db: AsyncSession = Depends(get_app_db_session)):
    """
    Logs out the user by invalidating the refresh token and clearing the HttpOnly cookie.
    """
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        await auth_handler.invalidate_refresh_token(refresh_token, db)
    
    response.delete_cookie(key="refresh_token", httponly=True, samesite="lax", secure=True)
    return {"message": "Logged out successfully"}

@router.get("/users/me")
async def read_users_me(
    current_user: dict = Depends(auth_handler.decode_token),
    db: AsyncSession = Depends(get_app_db_session)
):
    """
    Returns the current user's information from the local database.
    """
    username = current_user.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username not found in token.")

    db_user = await usuario_controller.get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found in local database.")

    # Construct a dictionary that matches the frontend's User interface
    user_info = {
        "username": db_user.id,
        "displayName": db_user.nome,
        "email": db_user.email,
        "perfil": db_user.perfil.value,
        "department": [db_user.lotacao] if db_user.lotacao else [],
        "title": [db_user.cargo] if db_user.cargo else [],
        "employeeNumber": [db_user.matricula] if db_user.matricula else [],
        "userPrincipalName": [db_user.email] if db_user.email else [],
        "givenName": [db_user.nome.split(' ')[0]] if db_user.nome else [],
    }
    
    # Merge groups from the token, as they are not stored in the Usuario model
    if "groups" in current_user:
        user_info["groups"] = current_user["groups"]

    return user_info



