"""create initial tables

Revision ID: 001
Revises:
Create Date: 2026-05-11 00:00:00.000000
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rutas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("origen", sa.String(length=100), nullable=False),
        sa.Column("destino", sa.String(length=100), nullable=False),
        sa.Column("distancia_km", sa.Float(), nullable=False),
        sa.Column("casetas", sa.Float(), nullable=False),
        sa.Column("trafico", sa.Integer(), nullable=False),
        sa.Column("riesgo", sa.Integer(), nullable=False),
        sa.Column("estado_carretera", sa.Integer(), nullable=False),
        sa.Column("inseguridad", sa.Integer(), nullable=False),
        sa.Column("activa", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_rutas_id"), "rutas", ["id"], unique=False)
    op.create_index(op.f("ix_rutas_origen"), "rutas", ["origen"], unique=False)
    op.create_index(op.f("ix_rutas_destino"), "rutas", ["destino"], unique=False)

    op.create_table(
        "transportes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=120), nullable=False),
        sa.Column("tipo", sa.String(length=30), nullable=False),
        sa.Column("costo_km", sa.Float(), nullable=False),
        sa.Column("velocidad_promedio", sa.Float(), nullable=False),
        sa.Column("capacidad_kg", sa.Float(), nullable=False),
        sa.Column("seguridad", sa.Integer(), nullable=False),
        sa.Column("mantenimiento", sa.Float(), nullable=False),
        sa.Column("costo_operativo", sa.Float(), nullable=False),
        sa.Column("consumo_por_km", sa.Float(), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_transportes_id"), "transportes", ["id"], unique=False)
    op.create_index(op.f("ix_transportes_tipo"), "transportes", ["tipo"], unique=False)

    op.create_table(
        "simulaciones",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("origen", sa.String(length=100), nullable=False),
        sa.Column("destino", sa.String(length=100), nullable=False),
        sa.Column("peso_kg", sa.Float(), nullable=False),
        sa.Column("tipo_mercancia", sa.String(length=120), nullable=False),
        sa.Column("prioridad", sa.String(length=30), nullable=False),
        sa.Column("fecha", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_simulaciones_id"), "simulaciones", ["id"], unique=False)
    op.create_index(op.f("ix_simulaciones_origen"), "simulaciones", ["origen"], unique=False)
    op.create_index(op.f("ix_simulaciones_destino"), "simulaciones", ["destino"], unique=False)

    op.create_table(
        "resultados_simulacion",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("simulacion_id", sa.Integer(), nullable=False),
        sa.Column("ruta_id", sa.Integer(), nullable=False),
        sa.Column("transporte_id", sa.Integer(), nullable=False),
        sa.Column("costo_total", sa.Float(), nullable=False),
        sa.Column("tiempo_estimado_horas", sa.Float(), nullable=False),
        sa.Column("puntaje_riesgo", sa.Float(), nullable=False),
        sa.Column("consumo_total", sa.Float(), nullable=False),
        sa.Column("puntaje_total", sa.Float(), nullable=False),
        sa.Column("recomendado", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["ruta_id"], ["rutas.id"]),
        sa.ForeignKeyConstraint(["simulacion_id"], ["simulaciones.id"]),
        sa.ForeignKeyConstraint(["transporte_id"], ["transportes.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_resultados_simulacion_id"), "resultados_simulacion", ["id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_resultados_simulacion_id"), table_name="resultados_simulacion")
    op.drop_table("resultados_simulacion")
    op.drop_index(op.f("ix_simulaciones_destino"), table_name="simulaciones")
    op.drop_index(op.f("ix_simulaciones_origen"), table_name="simulaciones")
    op.drop_index(op.f("ix_simulaciones_id"), table_name="simulaciones")
    op.drop_table("simulaciones")
    op.drop_index(op.f("ix_transportes_tipo"), table_name="transportes")
    op.drop_index(op.f("ix_transportes_id"), table_name="transportes")
    op.drop_table("transportes")
    op.drop_index(op.f("ix_rutas_destino"), table_name="rutas")
    op.drop_index(op.f("ix_rutas_origen"), table_name="rutas")
    op.drop_index(op.f("ix_rutas_id"), table_name="rutas")
    op.drop_table("rutas")
