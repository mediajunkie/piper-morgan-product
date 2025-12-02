#!/usr/bin/env python3
"""Generate SQL DDL from SQLAlchemy models"""

from sqlalchemy.schema import CreateTable
from services.database.models import Base

# Generate DDL for all tables
for table in Base.metadata.sorted_tables:
    ddl = str(CreateTable(table).compile(compile_kwargs={'literal_binds': True}))
    print(ddl)
    print("\n")
