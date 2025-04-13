import sqlalchemy as sa
from alembic import op

# Идентификатор этой миграции
revision = "8cd738c20faa"
# ID предыдущей миграции (замени на актуальный или None)
down_revision = "8ae01480f0cb"

def upgrade():
    # Удаляем старую таблицу
    op.drop_table('deleted_articles')
    # Создаём новую с id
    op.create_table(
        'deleted_articles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('article_id', sa.Integer, nullable=False),
        sa.Column('deleted_at', sa.DateTime, nullable=False, server_default=sa.func.now())
    )

def downgrade():
    # Удаляем новую таблицу
    op.drop_table('deleted_articles')
    # Восстанавливаем старую (без id)
    op.create_table(
        'deleted_articles',
        sa.Column('article_id', sa.Integer, nullable=False),
        sa.Column('deleted_at', sa.DateTime, nullable=False, server_default=sa.func.now())
    )
