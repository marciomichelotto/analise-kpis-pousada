# Análise de KPIs de Pequeno Meio de Hospedagem

Pipeline ETL e dashboard de Business Intelligence para análise de desempenho de uma pousada — modelagem dimensional em SQL Server, transformação em Python e visualização em Power BI.

## Contexto

O setor de hospedagem tem métricas próprias consolidadas pelo mercado — ADR, RevPAR, taxa de ocupação — que exigem uma estrutura de dados bem modelada para serem calculadas com consistência. Este projeto aplica conceitos de Data Warehouse e BI sobre dados fictícios de reservas para demonstrar essa estrutura na prática.

## Modelo de Dados

Modelagem dimensional (esquema estrela):

- **Fato:** `fato_reservas`
- **Dimensões:** `dim_datas`, `dim_quartos`, `dim_canais`, `dim_formas_pagamento`, `dim_hospedes`

## Pipeline ETL

### 1. Criar esquema no SQL Server

```sql
sql/create_dw_schema.sql
```

### 2. Preparar arquivos CSV

Coloque os arquivos em `dados/csv/` com estes nomes:

- `dim_datas.csv`
- `dim_quartos.csv`
- `dim_canais.csv`
- `dim_formas_pagamento.csv`
- `dim_hospedes.csv`
- `fato_reservas.csv`

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar o ETL

```bash
python scripts/etl_csv_to_sqlserver.py \
  --server localhost \
  --database PousadaDW \
  --username sa \
  --password '<SENHA>' \
  --mode replace
```

Também é possível usar autenticação integrada (Windows/Trusted Connection), omitindo usuário e senha.

## KPIs Implementados

| KPI | Descrição |
|-----|-----------|
| Taxa de Ocupação | Proporção de quartos ocupados no período |
| ADR | Diária média (Average Daily Rate) |
| RevPAR | Receita por quarto disponível |
| Receita Total | Soma das receitas no período |
| Ticket Médio | Valor médio por reserva |
| Taxa de Retorno | Proporção de re-hóspedes |
| Receita por Canal | Desempenho por canal de aquisição |
| Receita por Forma de Pagamento | Distribuição por método de pagamento |
| Receita por Quarto | Rentabilidade individual por unidade |
| Permanência Média | Média de diárias por reserva |

## Tecnologias

- **SQL Server** — modelagem dimensional e consultas
- **Python** — ETL de CSV para SQL Server
- **Power BI** — dashboards e medidas DAX
