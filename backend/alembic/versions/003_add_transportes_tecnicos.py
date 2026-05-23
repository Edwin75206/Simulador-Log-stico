"""add transportes tecnicos

Revision ID: 003
Revises: 002
Create Date: 2026-05-19 00:00:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("transportes", sa.Column("categoria", sa.String(length=30), nullable=True))
    op.add_column("transportes", sa.Column("subcategoria", sa.String(length=80), nullable=True))
    op.add_column("transportes", sa.Column("tipo_mercancia", sa.String(length=30), nullable=True))
    op.add_column("transportes", sa.Column("refrigerado", sa.Boolean(), nullable=True))
    op.add_column("transportes", sa.Column("combustible", sa.String(length=40), nullable=True))
    op.add_column("transportes", sa.Column("rendimiento_km_litro", sa.Float(), nullable=True))
    op.add_column("transportes", sa.Column("factor_caseta", sa.Float(), nullable=True))
    op.add_column("transportes", sa.Column("costo_combustible_litro", sa.Float(), nullable=True))
    op.add_column("transportes", sa.Column("descripcion", sa.Text(), nullable=True))
    op.add_column("transportes", sa.Column("uso_recomendado", sa.Text(), nullable=True))
    op.create_index(op.f("ix_transportes_categoria"), "transportes", ["categoria"], unique=False)
    op.create_index(
        op.f("ix_transportes_tipo_mercancia"), "transportes", ["tipo_mercancia"], unique=False
    )

    op.add_column("resultados_simulacion", sa.Column("costo_combustible", sa.Float(), nullable=True))
    op.add_column("resultados_simulacion", sa.Column("casetas_ajustadas", sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column("resultados_simulacion", "casetas_ajustadas")
    op.drop_column("resultados_simulacion", "costo_combustible")
    op.drop_index(op.f("ix_transportes_tipo_mercancia"), table_name="transportes")
    op.drop_index(op.f("ix_transportes_categoria"), table_name="transportes")
    op.drop_column("transportes", "uso_recomendado")
    op.drop_column("transportes", "descripcion")
    op.drop_column("transportes", "costo_combustible_litro")
    op.drop_column("transportes", "factor_caseta")
    op.drop_column("transportes", "rendimiento_km_litro")
    op.drop_column("transportes", "combustible")
    op.drop_column("transportes", "refrigerado")
    op.drop_column("transportes", "tipo_mercancia")
    op.drop_column("transportes", "subcategoria")
    op.drop_column("transportes", "categoria")
