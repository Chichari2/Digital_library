"""Create initial schema

Revision ID: e255476337a3
Revises: e9cbd5a77c91
Create Date: 2024-09-03 13:26:42.788312

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e255476337a3'
down_revision = 'e9cbd5a77c91'
branch_labels = None
depends_on = None


def upgrade():
  # ### команды автоматически сгенерированные Alembic - пожалуйста, при необходимости измените! ###
  op.drop_table('_alembic_tmp_author')

  with op.batch_alter_table('author', schema=None) as batch_op:
    batch_op.add_column(sa.Column('birth_date', sa.String(length=10), nullable=True))
    batch_op.add_column(sa.Column('date_of_death', sa.String(length=10), nullable=True))
    batch_op.alter_column('name',
                          existing_type=sa.VARCHAR(length=128),
                          type_=sa.String(length=100),
                          existing_nullable=False)

  with op.batch_alter_table('book', schema=None) as batch_op:
    batch_op.add_column(sa.Column('isbn', sa.String(length=13), nullable=True))
    batch_op.add_column(sa.Column('publication_year', sa.Integer(), nullable=True))
    batch_op.add_column(sa.Column('author_id', sa.Integer(), nullable=False))
    batch_op.alter_column('title',
                          existing_type=sa.VARCHAR(length=128),
                          type_=sa.String(length=100),
                          existing_nullable=False)
    batch_op.create_foreign_key('fk_author_id', 'author', ['author_id'], ['id'])

  # ### конец команд Alembic ###


def downgrade():
  # ### команды автоматически сгенерированные Alembic - пожалуйста, при необходимости измените! ###
  with op.batch_alter_table('book', schema=None) as batch_op:
    batch_op.drop_constraint('fk_author_id', type_='foreignkey')
    batch_op.alter_column('title',
                          existing_type=sa.String(length=100),
                          type_=sa.VARCHAR(length=128),
                          existing_nullable=False)
    batch_op.drop_column('author_id')
    batch_op.drop_column('publication_year')
    batch_op.drop_column('isbn')

  with op.batch_alter_table('author', schema=None) as batch_op:
    batch_op.alter_column('name',
                          existing_type=sa.String(length=100),
                          type_=sa.VARCHAR(length=128),
                          existing_nullable=False)
    batch_op.drop_column('date_of_death')
    batch_op.drop_column('birth_date')

  op.create_table('_alembic_tmp_author',
                  sa.Column('id', sa.INTEGER(), nullable=False),
                  sa.Column('name', sa.VARCHAR(length=100), nullable=False),
                  sa.Column('birth_date', sa.VARCHAR(length=10), nullable=True),
                  sa.Column('date_of_death', sa.VARCHAR(length=10), nullable=True),
                  sa.PrimaryKeyConstraint('id')
                  )
  # ### конец команд Alembic ###
