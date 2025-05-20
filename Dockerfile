FROM bitnami/spark:3.4.1

USER root

# Instala dependências Python necessárias para o projeto
RUN pip install --no-cache-dir pyspark==3.4.1 google-cloud-storage==2.14.0 google-auth==2.28.1 google-api-python-client==2.117.0 delta-spark requests yfinance 

# Mantém o container rodando para interatividade
CMD ["tail", "-f", "/dev/null"]
