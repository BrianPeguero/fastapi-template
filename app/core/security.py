"""_summary_
"""

from passlib.context import CryptContext


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """_summary_

    Args:
        passwrod (str): _description_

    Returns:
        str: _description_
    """

    return PWD_CONTEXT.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """_summary_

    Args:
        plain_password (str): _description_
        hashed_password (str): _description_

    Returns:
        bool: _description_
    """
    
    return PWD_CONTEXT.verify(plain_password, hashed_password)