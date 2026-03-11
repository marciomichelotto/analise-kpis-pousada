# 📊 Projeto de Análise de KPIs de Pequeno Meio de Hospedagem

Este projeto simula a análise de desempenho de uma pousada utilizando dados fictícios de reservas. O objetivo é aplicar conhecimentos de Análise de Dados e Business Intelligence para a criação de dashboards e indicadores úteis à gestão de pequenos meios de hospedagem.

## 🎯 Objetivo do Projeto

- Criar uma estrutura de dados modelada (Data Warehouse)
- Medir os principais KPIs do setor hoteleiro
- Facilitar a tomada de decisão com base em dados
- Aplicar boas práticas de engenharia de dados com SQL, DAX e Power BI

## 🧱 Estrutura do Projeto

- **Modelo de Dados**: Tabela fato (`fato_reservas`) + tabelas dimensão (`dim_datas`, `dim_quartos`, `dim_canais`, `dim_formas_pagamento`, `dim_hospedes`)
- **Ferramentas Utilizadas**:
  - SQL Server (modelagem e consultas)
  - Python (ETL de CSV para SQL Server)
  - Power BI (dashboards e DAX)

## ⚙️ Pipeline ETL CSV → SQL Server

### 1) Criar esquema no SQL Server

Execute o script:

```sql
sql/create_dw_schema.sql
```

### 2) Preparar arquivos CSV

Coloque os arquivos em `dados/csv/` com estes nomes:

- `dim_datas.csv`
- `dim_quartos.csv`
- `dim_canais.csv`
- `dim_formas_pagamento.csv`
- `dim_hospedes.csv`
- `fato_reservas.csv`

### 3) Instalar dependências

```bash
pip install -r requirements.txt
```

### 4) Rodar ETL

```bash
python scripts/etl_csv_to_sqlserver.py \
  --server localhost \
  --database PousadaDW \
  --username sa \
  --password '<SENHA>' \
  --mode replace
```

Também é possível usar autenticação integrada (Windows/Trusted Connection), omitindo usuário e senha.

## 📌 KPIs Implementados

- Taxa de Ocupação
- ADR (Diária Média)
- RevPAR (Receita por Quarto Disponível)
- Receita Total
- Ticket Médio
- Taxa de Retorno (re-hóspedes)
- Receita por Canal
- Receita por Forma de Pagamento
- Receita por Quarto
- Permanência Média
