"""set case status enum

Revision ID: 5f3c533bff62
Revises: 2ee8f15a9299
Create Date: 2024-04-07 13:34:43.565686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f3c533bff62'
down_revision: Union[str, None] = '2ee8f15a9299'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

new_type = sa.Enum('initiated', 'extended', 'justified', 'convicted', name='casestatus')

tcr = sa.sql.table('testcaseresult',
                   sa.Column('status', new_type, nullable=False))


def upgrade():
    # Create and convert to the "new" status type
    new_type.create(op.get_bind(), checkfirst=False)
    op.execute('ALTER TABLE cases ALTER COLUMN status TYPE casestatus'
               ' USING status::text::casestatus')


def downgrade():
    op.alter_column('cases', 'status',
               existing_type=sa.Enum('initiated', 'extended', 'justified', 'convicted', name='casestatus'),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    new_type.drop(op.get_bind(), checkfirst=False)
