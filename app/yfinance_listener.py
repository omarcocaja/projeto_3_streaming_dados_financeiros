from datetime import datetime
from google.cloud import storage
from io import BytesIO
import csv
import json
import multiprocessing
import os
import shutil
import threading
import time
import yfinance as yf

class YFinanceCollector:
    def __init__(self):
        self.CARTEIRA_FILE = "/app/carteira.txt"
        self.GCS_BUCKET_NAME = "bucket-portfolio-projeto-3"
        self.GCS_CREDENTIALS_FILE = "/app/"
        self.ws_process = None
        self.last_tickers = []
    
    def load_tickers(self):
        if os.path.exists(self.CARTEIRA_FILE):
            with open(self.CARTEIRA_FILE, "r") as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        return []

    def upload_to_gcs(self, file_path, subfolder=""):
        client = storage.Client.from_service_account_json(self.GCS_CREDENTIALS_FILE)
        bucket = client.bucket(self.GCS_BUCKET_NAME)

        # Define o caminho do blob com subpasta se informado
        blob_name = f"{subfolder}/{os.path.basename(file_path)}" if subfolder else os.path.basename(file_path)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        print(f"Arquivo {file_path} enviado ao GCS em {blob_name}.")

        # Remove o arquivo ZIP local após o envio
        os.remove(file_path)
        print(f"Arquivo local {file_path} removido após envio.")

    def handle_message(self, message):
        data = {
            'ticker': message['id'],
            'price': message['price'],
            'time': message['time'],
            'exchange': message['exchange'],
            'change_percent': message['change_percent'],
            'change': message['change'],
        }

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        file_name = f"{data['ticker']}_{timestamp}.json"
        gcs_path = f"bronze/yfinance/{file_name}"

        # Converte JSON em bytes para upload direto
        content = json.dumps(data).encode("utf-8")
        client = storage.Client.from_service_account_json(self.GCS_CREDENTIALS_FILE)
        bucket = client.bucket(self.GCS_BUCKET_NAME)
        blob = bucket.blob(gcs_path)
        blob.upload_from_file(BytesIO(content), content_type='application/json')

        print(f"Mensagem enviada diretamente ao GCS: gs://{self.GCS_BUCKET_NAME}/{gcs_path}") # GSUTIL


    def websocket_runner(self, tickers):
        print(f"Subscribed to symbols: {tickers}")
        try:
            with yf.WebSocket() as ws:
                ws.subscribe(tickers)
                print("Listening for messages...")
                ws.listen(self.handle_message)
        except Exception as e:
            print(f"Erro no WebSocket: {e}")

    def start_websocket(self):
        if self.ws_process and self.ws_process.is_alive():
            print("Encerrando WebSocket antigo...")
            self.ws_process.terminate()
            self.ws_process.join()

        tickers = self.load_tickers()
        self.last_tickers = tickers
        self.ws_process = multiprocessing.Process(target=self.websocket_runner, args=(tickers,))
        self.ws_process.start()

    def carteira_monitor(self):
        while True:
            current_tickers = self.load_tickers()
            if current_tickers != self.last_tickers:
                print("Carteira atualizada:", current_tickers)
                self.start_websocket()
            time.sleep(5)

    def start(self):
        threading.Thread(target=self.carteira_monitor, daemon=True).start()
        self.start_websocket()

        while True:
            time.sleep(60)


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    collector = YFinanceCollector()
    collector.start()
