"""Initial migration

Revision ID: f749532b613d
Revises:
Create Date: 2024-09-03 10:49:06.008683

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f749532b613d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Drop tables if they exist
    op.drop_table('book')
    op.drop_table('author')

    # Create 'author' table
    op.create_table(
        'author',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('birth_date', sa.String(length=10), nullable=True),
        sa.Column('date_of_death', sa.String(length=10), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Create 'book' table
    op.create_table(
        'book',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('isbn', sa.String(length=13), nullable=True),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('publication_year', sa.Integer(), nullable=True),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['author.id'], name='fk_book_author'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Drop tables if they exist
    op.drop_table('book')
    op.drop_table('author')

    # Recreate 'author' table with original schema
    op.create_table(
        'author',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Recreate 'book' table with original schema
    op.create_table(
        'book',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('author_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['author_id'], ['author.id'], name='fk_book_author'),
        sa.PrimaryKeyConstraint('id')
    )
