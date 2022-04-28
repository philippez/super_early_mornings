"""initial migration

Revision ID: d10e2f9a748a
Revises: 
Create Date: 2022-04-27 21:40:10.280558

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd10e2f9a748a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('opinion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('opinion_name', sa.String(length=64), nullable=True),
    sa.Column('opinion_factor', sa.Integer(), nullable=True),
    sa.Column('opinion_desc', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('platform',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('platform_name', sa.String(length=64), nullable=True),
    sa.Column('platform_desc', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('super__theme',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('super_theme_name', sa.String(length=64), nullable=True),
    sa.Column('super_theme_desc', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_super__theme_super_theme_name'), 'super__theme', ['super_theme_name'], unique=True)
    op.create_index(op.f('ix_super__theme_timestamp'), 'super__theme', ['timestamp'], unique=False)
    op.create_table('tx__type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tx_type_name', sa.String(length=64), nullable=True),
    sa.Column('tx_type_desc', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('asset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('asset_name', sa.String(length=64), nullable=True),
    sa.Column('asset_currency', sa.String(length=10), nullable=True),
    sa.Column('asset_desc', sa.String(length=200), nullable=True),
    sa.Column('asset_region', sa.String(length=64), nullable=True),
    sa.Column('asset_type', sa.String(length=64), nullable=True),
    sa.Column('super_theme', sa.String(length=64), nullable=True),
    sa.Column('micro_theme', sa.String(length=64), nullable=True),
    sa.Column('bloomberg_ticker', sa.String(length=64), nullable=True),
    sa.Column('sec_ref', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_asset_asset_name'), 'asset', ['asset_name'], unique=True)
    op.create_index(op.f('ix_asset_timestamp'), 'asset', ['timestamp'], unique=False)
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    op.create_table('asset__prices',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('asset_id', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['asset_id'], ['asset.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_asset__prices_date'), 'asset__prices', ['date'], unique=False)
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('asset_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['asset_id'], ['asset.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('type', sa.String(length=64), nullable=True),
    sa.Column('qty', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('asset_id', sa.Integer(), nullable=True),
    sa.Column('platform_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['asset_id'], ['asset.id'], ),
    sa.ForeignKeyConstraint(['platform_id'], ['platform.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transaction_date'), 'transaction', ['date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transaction_date'), table_name='transaction')
    op.drop_table('transaction')
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    op.drop_index(op.f('ix_asset__prices_date'), table_name='asset__prices')
    op.drop_table('asset__prices')
    op.drop_table('followers')
    op.drop_index(op.f('ix_asset_timestamp'), table_name='asset')
    op.drop_index(op.f('ix_asset_asset_name'), table_name='asset')
    op.drop_table('asset')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('tx__type')
    op.drop_index(op.f('ix_super__theme_timestamp'), table_name='super__theme')
    op.drop_index(op.f('ix_super__theme_super_theme_name'), table_name='super__theme')
    op.drop_table('super__theme')
    op.drop_table('platform')
    op.drop_table('opinion')
    # ### end Alembic commands ###
