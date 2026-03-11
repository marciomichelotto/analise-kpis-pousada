#!/usr/bin/env python3
"""ETL pipeline: CSV files to SQL Server (dimensional model)."""

from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


DEFAULT_TABLE_MAP = {
    "dim_datas": "dim_datas.csv",
    "dim_quartos": "dim_quartos.csv",
    "dim_canais": "dim_canais.csv",
    "dim_formas_pagamento": "dim_formas_pagamento.csv",
    "dim_hospedes": "dim_hospedes.csv",
    "fato_reservas": "fato_reservas.csv",
}


def build_engine(server: str, database: str, username: str | None, password: str | None, driver: str) -> Engine:
    """Build SQL Server engine with SQL auth or trusted connection."""
    if username and password:
        conn_str = (
            f"mssql+pyodbc://{username}:{password}@{server}/{database}"
            f"?driver={driver.replace(' ', '+')}&TrustServerCertificate=yes"
        )
    else:
        conn_str = (
            f"mssql+pyodbc://@{server}/{database}"
            f"?driver={driver.replace(' ', '+')}&trusted_connection=yes&TrustServerCertificate=yes"
        )

    return create_engine(conn_str, fast_executemany=True)


def read_csv(csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    return pd.read_csv(csv_path)


def normalize_dates(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["data_checkin", "data_checkout", "data_reserva", "data"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def truncate_table(engine: Engine, table_name: str, schema: str) -> None:
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE [{schema}].[{table_name}];"))


def load_table(engine: Engine, table_name: str, df: pd.DataFrame, schema: str, mode: str) -> None:
    if mode == "replace":
        truncate_table(engine, table_name, schema)

    df.to_sql(
        table_name,
        con=engine,
        schema=schema,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000,
    )


def run_etl(csv_dir: Path, engine: Engine, schema: str, mode: str, table_map: dict[str, str]) -> None:
    order = [
        "dim_datas",
        "dim_quartos",
        "dim_canais",
        "dim_formas_pagamento",
        "dim_hospedes",
        "fato_reservas",
    ]

    for table_name in order:
        csv_name = table_map[table_name]
        csv_path = csv_dir / csv_name
        logging.info("Reading %s", csv_path)
        df = read_csv(csv_path)
        df = normalize_dates(df)
        logging.info("Loading %s rows into %s.%s", len(df), schema, table_name)
        load_table(engine, table_name, df, schema, mode)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Load CSV files into SQL Server.")
    parser.add_argument("--csv-dir", default="dados/csv", help="Directory that contains CSV files.")
    parser.add_argument("--server", default=os.getenv("SQLSERVER_HOST", "localhost"))
    parser.add_argument("--database", default=os.getenv("SQLSERVER_DB", "PousadaDW"))
    parser.add_argument("--username", default=os.getenv("SQLSERVER_USER"))
    parser.add_argument("--password", default=os.getenv("SQLSERVER_PASSWORD"))
    parser.add_argument("--driver", default=os.getenv("SQLSERVER_DRIVER", "ODBC Driver 18 for SQL Server"))
    parser.add_argument("--schema", default=os.getenv("SQLSERVER_SCHEMA", "dbo"))
    parser.add_argument(
        "--mode",
        default="append",
        choices=["append", "replace"],
        help="append = only append rows, replace = truncate then append",
    )
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level), format="%(levelname)s | %(message)s")

    engine = build_engine(
        server=args.server,
        database=args.database,
        username=args.username,
        password=args.password,
        driver=args.driver,
    )

    run_etl(
        csv_dir=Path(args.csv_dir),
        engine=engine,
        schema=args.schema,
        mode=args.mode,
        table_map=DEFAULT_TABLE_MAP,
    )
    logging.info("ETL completed successfully.")


if __name__ == "__main__":
    main()
