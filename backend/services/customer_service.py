"""
Customer Service - Handle customer operations
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
import uuid
import sys
import os

# Add parent path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from models import Customer
from database import async_session_maker


class CustomerService:
    """Service for customer management"""
    
    async def get_or_create_customer(
        self,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        name: Optional[str] = None
    ) -> Customer:
        """
        Get existing customer or create new one
        
        Args:
            email: Customer email (primary identifier)
            phone: Customer phone (secondary identifier)
            name: Customer name
            
        Returns:
            Customer object
        """
        async with async_session_maker() as session:
            # Try to find by email first
            if email:
                result = await session.execute(
                    select(Customer).where(Customer.email == email)
                )
                customer = result.scalar_one_or_none()
                
                if customer:
                    # Update name if provided
                    if name and not customer.name:
                        customer.name = name
                    await session.commit()
                    return customer
            
            # Try to find by phone
            if phone:
                result = await session.execute(
                    select(Customer).where(Customer.phone == phone)
                )
                customer = result.scalar_one_or_none()
                
                if customer:
                    # Update email if provided
                    if email and not customer.email:
                        customer.email = email
                    if name and not customer.name:
                        customer.name = name
                    await session.commit()
                    return customer
            
            # Create new customer
            customer = Customer(
                email=email,
                phone=phone,
                name=name
            )
            session.add(customer)
            await session.commit()
            await session.refresh(customer)
            
            return customer
    
    async def get_customer_by_id(self, customer_id: uuid.UUID) -> Optional[Customer]:
        """Get customer by ID"""
        async with async_session_maker() as session:
            result = await session.execute(
                select(Customer).where(Customer.customer_id == customer_id)
            )
            return result.scalar_one_or_none()
    
    async def update_customer(
        self,
        customer_id: uuid.UUID,
        **kwargs
    ) -> Optional[Customer]:
        """Update customer fields"""
        async with async_session_maker() as session:
            result = await session.execute(
                select(Customer).where(Customer.customer_id == customer_id)
            )
            customer = result.scalar_one_or_none()
            
            if customer:
                for key, value in kwargs.items():
                    if hasattr(customer, key):
                        setattr(customer, key, value)
                
                await session.commit()
                await session.refresh(customer)
            
            return customer


# Global customer service instance
customer_service = CustomerService()
