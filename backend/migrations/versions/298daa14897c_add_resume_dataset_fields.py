
"""Add resume dataset fields

Revision ID: 298daa14897c
Revises: 
Create Date: 2026-11-24 23:42:16.172257

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '298daa14897c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('resumes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dataset_id', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('resume_html', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('category', sa.String(length=100), nullable=True))
        batch_op.alter_column(
            'filename',
            existing_type=mysql.VARCHAR(length=255),
            nullable=True
        )
        batch_op.create_unique_constraint(
            'uq_resumes_dataset_id',
            ['dataset_id']
        )


def downgrade():
    with op.batch_alter_table('resumes', schema=None) as batch_op:
        batch_op.drop_constraint(
            'uq_resumes_dataset_id',
            type_='unique'
        )
        batch_op.alter_column(
            'filename',
            existing_type=mysql.VARCHAR(length=255),
            nullable=False
        )
        batch_op.drop_column('category')
        batch_op.drop_column('resume_html')
        batch_op.drop_column('dataset_id')

