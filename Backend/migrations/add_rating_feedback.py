 """Add rating and feedback to service requests

Revision ID: xyz123
Revises: previous_revision
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('service_requests', sa.Column('rating', sa.Float(), nullable=True))
    op.add_column('service_requests', sa.Column('feedback', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('service_requests', 'rating')
    op.drop_column('service_requests', 'feedback')