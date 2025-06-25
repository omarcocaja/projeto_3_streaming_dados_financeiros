# Streaming de Dados Financeiros com Kafka, Spark e BigQuery

Este projeto simula uma arquitetura de streaming de dados financeiros em tempo real. O pipeline captura cotações da bolsa usando a API do Yahoo Finance, publica os dados em um tópico Kafka e os consome com o **Apache Spark Structured Streaming**, escrevendo os resultados na camada **Silver** do data lake, armazenada no **Google Cloud Storage** (GCS) ou **BigQuery**.

---

## 🗂 Estrutura do Projeto

```
projeto_3_streaming_dados_financeiros/
│
├── app/
│   ├── yfinance_listener.py           # Publicador Kafka que escuta cotações via Yahoo Finance
│   ├── gcs_silver_layer_writer.py     # Spark Streaming Consumer que grava no GCS
│   ├── gcs_reader.py                  # Leitor para leitura e debug da camada silver
│   ├── carteira.txt                   # Lista de ativos a serem monitorados
│   └── requirements.txt               # Dependências da aplicação Python
│
├── jars/
│   └── gcs-connector-*.jar            # Conector do GCS para o Spark
│
├── docker-compose.yaml                # Sobe a infraestrutura com Kafka, Spark, etc.
├── Dockerfile                         # Container para execução da aplicação
└── README.md                          # Este arquivo
```

---

## ⚙️ Como Executar

### 1. Baixe o conector GCS (necessário)

Link para download do JAR: https://repo1.maven.org/maven2/com/google/cloud/bigdataoss/gcs-connector/hadoop3-2.2.5/gcs-connector-hadoop3-2.2.5-shaded.jar

Salve o `.jar` na pasta `jars/`.

### 2. Suba a infraestrutura
```bash
docker-compose up -d
```

### 3. Execute o produtor (YFinance → Kafka)
```bash
docker exec -it app python app/yfinance_listener.py
```

### 4. Execute o consumidor (Kafka → GCS/BigQuery)
```bash
docker exec -it app spark-submit   --jars jars/gcs-connector-hadoop3-2.2.5-shaded.jar   app/gcs_silver_layer_writer.py
```

> Os dados são salvos de forma particionada e com suporte a **modo append**, respeitando a estrutura de streaming.

---

## 📦 Tecnologias Utilizadas

- **Apache Kafka**
- **Apache Spark Structured Streaming**
- **Google Cloud Storage (GCS)**
- **BigQuery (opcional)**
- **Docker & Docker Compose**
- **Python 3.10+**
- **Yahoo Finance API (via yfinance)**

---

## 📄 Licença

Este projeto está licenciado sob a licença **MIT** e é livre para uso educacional e profissional.

---

## 📬 Contato

- [LinkedIn](https://www.linkedin.com/in/marco-caja)  
- [Instagram](https://www.instagram.com/omarcocaja)

