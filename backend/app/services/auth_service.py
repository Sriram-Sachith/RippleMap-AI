"""Authentication service."""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from ..models.user import User, UserRole
from ..schemas.user import UserCreate
from ..security import hash_password, verify_password, create_tokens_pair

logger = logging.getLogger(__name__)


class AuthService:
    """Service for user authentication."""
    
    @staticmethod
    async def create_user(
        db: AsyncSession,
        user_data: UserCreate,
    ) -> User:
        """Create a new user."""
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hash_password(user_data.password),
            full_name=user_data.full_name,
            role=user_data.role,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        logger.info(f"Created new user: {user_data.username}")
        return db_user
    
    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        username: str,
        password: str,
    ) -> User:
        """Authenticate a user by username and password."""
        result = await db.execute(
            select(User).where(User.username == username)
        )
        db_user = result.scalars().first()
        
        if not db_user or not verify_password(password, db_user.hashed_password):
            logger.warning(f"Failed authentication attempt for user: {username}")
            return None
        
        if not db_user.is_active:
            logger.warning(f"Attempt to authenticate inactive user: {username}")
            return None
        
        logger.info(f"Successful authentication for user: {username}")
        return db_user
    
    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
        """Get user by ID."""
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalars().first()
    
    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> User:
        """Get user by username."""
        result = await db.execute(
            select(User).where(User.username == username)
        )
        return result.scalars().first()
    
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User:
        """Get user by email."""
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()
