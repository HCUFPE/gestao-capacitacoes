from fastapi import Depends, HTTPException, status

from .auth import auth_handler
from ..models import PerfilUsuario

def get_current_user(token: dict = Depends(auth_handler.decode_token)) -> dict:
    """
    Dependency to get the current user's data from the JWT token.
    """
    return token

def is_chefia(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Dependency that checks if the current user has 'Chefia' or 'UDP' profile.
    Raises a 403 Forbidden error if not.
    """
    perfil = current_user.get("perfil")
    if perfil not in [PerfilUsuario.CHEFIA.value, PerfilUsuario.UDP.value]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Requer perfil de Chefia ou superior."
        )
    return current_user

def is_udp(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Dependency that checks if the current user has 'UDP' profile.
    Raises a 403 Forbidden error if not.
    """
    perfil = current_user.get("perfil")
    if perfil != PerfilUsuario.UDP.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Requer perfil de UDP (Administrador)."
        )
    return current_user
