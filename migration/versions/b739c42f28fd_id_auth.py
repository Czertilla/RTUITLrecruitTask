"""id auth

Revision ID: b739c42f28fd
Revises: ad2782482558
Create Date: 2024-03-18 23:30:24.435743

"""
from typing import Sequence, Union

from alembic import op
import fastapi_users_db_sqlalchemy
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b739c42f28fd'
down_revision: Union[str, None] = 'ad2782482558'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('user_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False))
    op.add_column('user', sa.Column('oauth_name', sa.String(length=100), nullable=False))
    op.add_column('user', sa.Column('access_token', sa.String(length=1024), nullable=False))
    op.add_column('user', sa.Column('expires_at', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('refresh_token', sa.String(length=1024), nullable=True))
    op.add_column('user', sa.Column('account_id', sa.String(length=320), nullable=False))
    op.add_column('user', sa.Column('account_email', sa.String(length=320), nullable=False))
    op.create_index(op.f('ix_user_account_id'), 'user', ['account_id'], unique=False)
    op.create_index(op.f('ix_user_oauth_name'), 'user', ['oauth_name'], unique=False)
    op.create_unique_constraint(None, 'user', ['username'])
    op.create_foreign_key(None, 'user', 'user', ['user_id'], ['id'], ondelete='cascade')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_index(op.f('ix_user_oauth_name'), table_name='user')
    op.drop_index(op.f('ix_user_account_id'), table_name='user')
    op.drop_column('user', 'account_email')
    op.drop_column('user', 'account_id')
    op.drop_column('user', 'refresh_token')
    op.drop_column('user', 'expires_at')
    op.drop_column('user', 'access_token')
    op.drop_column('user', 'oauth_name')
    op.drop_column('user', 'user_id')
    # ### end Alembic commands ###
