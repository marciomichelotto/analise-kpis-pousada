IF DB_ID('PousadaDW') IS NULL
BEGIN
    CREATE DATABASE PousadaDW;
END
GO

USE PousadaDW;
GO

IF OBJECT_ID('dbo.fato_reservas', 'U') IS NOT NULL DROP TABLE dbo.fato_reservas;
IF OBJECT_ID('dbo.dim_hospedes', 'U') IS NOT NULL DROP TABLE dbo.dim_hospedes;
IF OBJECT_ID('dbo.dim_formas_pagamento', 'U') IS NOT NULL DROP TABLE dbo.dim_formas_pagamento;
IF OBJECT_ID('dbo.dim_canais', 'U') IS NOT NULL DROP TABLE dbo.dim_canais;
IF OBJECT_ID('dbo.dim_quartos', 'U') IS NOT NULL DROP TABLE dbo.dim_quartos;
IF OBJECT_ID('dbo.dim_datas', 'U') IS NOT NULL DROP TABLE dbo.dim_datas;
GO

CREATE TABLE dbo.dim_datas (
    data_key INT NOT NULL PRIMARY KEY,
    data DATE NOT NULL,
    ano SMALLINT NOT NULL,
    mes TINYINT NOT NULL,
    nome_mes VARCHAR(20) NOT NULL,
    trimestre TINYINT NOT NULL
);

CREATE TABLE dbo.dim_quartos (
    quarto_key INT NOT NULL PRIMARY KEY,
    numero_quarto VARCHAR(10) NOT NULL,
    tipo_quarto VARCHAR(50) NOT NULL,
    capacidade TINYINT NOT NULL
);

CREATE TABLE dbo.dim_canais (
    canal_key INT NOT NULL PRIMARY KEY,
    canal VARCHAR(80) NOT NULL
);

CREATE TABLE dbo.dim_formas_pagamento (
    forma_pagamento_key INT NOT NULL PRIMARY KEY,
    forma_pagamento VARCHAR(50) NOT NULL
);

CREATE TABLE dbo.dim_hospedes (
    hospede_key INT NOT NULL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL,
    cidade VARCHAR(80) NULL,
    estado CHAR(2) NULL,
    pais VARCHAR(40) NULL,
    cliente_recorrente BIT NOT NULL
);

CREATE TABLE dbo.fato_reservas (
    reserva_key BIGINT NOT NULL PRIMARY KEY,
    data_reserva_key INT NOT NULL,
    data_checkin_key INT NOT NULL,
    data_checkout_key INT NOT NULL,
    quarto_key INT NOT NULL,
    canal_key INT NOT NULL,
    forma_pagamento_key INT NOT NULL,
    hospede_key INT NOT NULL,
    diarias INT NOT NULL,
    valor_total DECIMAL(12,2) NOT NULL,
    qtd_hospedes INT NOT NULL,
    status_reserva VARCHAR(20) NOT NULL,
    FOREIGN KEY (data_reserva_key) REFERENCES dbo.dim_datas(data_key),
    FOREIGN KEY (data_checkin_key) REFERENCES dbo.dim_datas(data_key),
    FOREIGN KEY (data_checkout_key) REFERENCES dbo.dim_datas(data_key),
    FOREIGN KEY (quarto_key) REFERENCES dbo.dim_quartos(quarto_key),
    FOREIGN KEY (canal_key) REFERENCES dbo.dim_canais(canal_key),
    FOREIGN KEY (forma_pagamento_key) REFERENCES dbo.dim_formas_pagamento(forma_pagamento_key),
    FOREIGN KEY (hospede_key) REFERENCES dbo.dim_hospedes(hospede_key)
);
GO
