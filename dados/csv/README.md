# CSV files expected by ETL

Place the following files in this folder before running the pipeline:

- `dim_datas.csv`
- `dim_quartos.csv`
- `dim_canais.csv`
- `dim_formas_pagamento.csv`
- `dim_hospedes.csv`
- `fato_reservas.csv`

The ETL script reads these files and loads them in this exact order to satisfy foreign key constraints.
