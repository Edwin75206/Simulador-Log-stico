"""add puntos logisticos

Revision ID: 002
Revises: 001
Create Date: 2026-05-18 00:00:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "puntos_logisticos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=160), nullable=False),
        sa.Column("tipo", sa.String(length=40), nullable=False),
        sa.Column("ciudad", sa.String(length=100), nullable=False),
        sa.Column("estado", sa.String(length=100), nullable=False),
        sa.Column("direccion", sa.String(length=255), nullable=False),
        sa.Column("latitud", sa.Float(), nullable=True),
        sa.Column("longitud", sa.Float(), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_puntos_logisticos_id"), "puntos_logisticos", ["id"], unique=False)
    op.create_index(
        op.f("ix_puntos_logisticos_nombre"), "puntos_logisticos", ["nombre"], unique=False
    )
    op.create_index(op.f("ix_puntos_logisticos_tipo"), "puntos_logisticos", ["tipo"], unique=False)

    op.add_column("rutas", sa.Column("origen_id", sa.Integer(), nullable=True))
    op.add_column("rutas", sa.Column("destino_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        "fk_rutas_origen_punto_logistico", "rutas", "puntos_logisticos", ["origen_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_rutas_destino_punto_logistico",
        "rutas",
        "puntos_logisticos",
        ["destino_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint("fk_rutas_destino_punto_logistico", "rutas", type_="foreignkey")
    op.drop_constraint("fk_rutas_origen_punto_logistico", "rutas", type_="foreignkey")
    op.drop_column("rutas", "destino_id")
    op.drop_column("rutas", "origen_id")
    op.drop_index(op.f("ix_puntos_logisticos_tipo"), table_name="puntos_logisticos")
    op.drop_index(op.f("ix_puntos_logisticos_nombre"), table_name="puntos_logisticos")
    op.drop_index(op.f("ix_puntos_logisticos_id"), table_name="puntos_logisticos")
    op.drop_table("puntos_logisticos")
