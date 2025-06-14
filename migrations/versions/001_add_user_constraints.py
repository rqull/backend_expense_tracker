"""add user constraints

Revision ID: 001
Create Date: 2025-06-13
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Add email constraints
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    
    # Add username constraints
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    
    # Add created_at and updated_at defaults
    op.alter_column('users', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_nullable=True)
    
    op.alter_column('users', 'updated_at',
               existing_type=sa.DateTime(timezone=True),
               server_default=sa.text('CURRENT_TIMESTAMP'),
               existing_nullable=True)

def downgrade():
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.alter_column('users', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               server_default=None)
    op.alter_column('users', 'updated_at',
               existing_type=sa.DateTime(timezone=True),
               server_default=None)
