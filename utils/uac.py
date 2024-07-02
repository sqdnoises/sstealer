import os
import ctypes

__all__ = (
    "AdminStateUnknownError",
    "is_user_admin"
)

class AdminStateUnknownError(Exception):
    """Cannot determine whether the user is an admin."""
    pass

def is_user_admin(fail: bool = False) -> bool:
    """Return True if user has admin privileges.

    Raises:
        AdminStateUnknownError if user privileges cannot be determined.
    """
    
    try:
        return os.getuid() == 0
    except AttributeError:
        pass
    
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except AttributeError:
        if fail:
            raise AdminStateUnknownError