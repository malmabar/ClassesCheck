from __future__ import annotations

from typing import Callable
from typing import Optional

from fastapi import Depends, Header, HTTPException

from app.core.config import settings


ADMIN_ROLE = "admin"
OPERATOR_ROLE = "operator"
VIEWER_ROLE = "viewer"
_VALID_ROLES = {ADMIN_ROLE, OPERATOR_ROLE, VIEWER_ROLE}


def _normalize_role(value: str) -> str:
    return value.strip().lower()


def _assert_role_exists(role: str) -> None:
    if role not in _VALID_ROLES:
        allowed_roles = ", ".join(sorted(_VALID_ROLES))
        raise HTTPException(
            status_code=403,
            detail=(
                f"Access denied for role '{role}'. "
                f"Allowed roles: {allowed_roles}."
            ),
        )


def get_current_role(x_mc_role: Optional[str] = Header(default=None, alias="X-MC-Role")) -> str:
    effective = x_mc_role if x_mc_role is not None else settings.mc_default_role
    normalized = _normalize_role(effective)
    _assert_role_exists(normalized)
    return normalized


def require_roles(*roles: str) -> Callable[[str], str]:
    allowed = {_normalize_role(role) for role in roles}
    invalid = sorted(role for role in allowed if role not in _VALID_ROLES)
    if invalid:
        raise ValueError(f"Invalid RBAC configuration roles: {invalid}")

    def dependency(current_role: str = Depends(get_current_role)) -> str:
        if current_role not in allowed:
            allowed_roles = ", ".join(sorted(allowed))
            raise HTTPException(
                status_code=403,
                detail=(
                    f"Role '{current_role}' is not allowed for this action. "
                    f"Allowed roles: {allowed_roles}."
                ),
            )
        return current_role

    return dependency


require_read_access = require_roles(ADMIN_ROLE, OPERATOR_ROLE, VIEWER_ROLE)
require_mutation_access = require_roles(ADMIN_ROLE, OPERATOR_ROLE)
require_admin_access = require_roles(ADMIN_ROLE)
