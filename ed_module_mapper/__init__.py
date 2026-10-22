"""ED Module Mapper data modeling and CSV ingestion package."""

from .inventory import load_module_inventory
from .models import ModuleRecord

__all__ = ["ModuleRecord", "load_module_inventory"]
