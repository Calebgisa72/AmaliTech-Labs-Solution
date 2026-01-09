from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class Customer:
    customer_id: Optional[int]
    name: str
    email: str
    created_at: datetime


@dataclass
class Product:
    product_id: Optional[int]
    name: str
    category: str
    price: float
    stock_quantity: int
    metadata: Dict[str, Any]


@dataclass
class OrderItem:
    order_id: Optional[int]
    product_id: int
    quantity: int
    unit_price: float


@dataclass
class Order:
    order_id: Optional[int]
    customer_id: int
    order_date: datetime
    total_amount: float
    items: List[OrderItem]
