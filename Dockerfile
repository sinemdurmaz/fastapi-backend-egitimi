# 1. Aşama: Resmi ve hafif Python çalışma ortamı
FROM python:3.11-slim

# 2. Aşama: Çalışma dizini belirleme
WORKDIR /app

# 3. Aşama: Python çıktı tamponlamasını kapatma (Logları canlı görebilmek için)
ENV PYTHONUNBUFFERED=1

# 4. Aşama: Bağımlılıkları kopyalama ve kurma (Docker Cache avantajı)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Aşama: Proje dosyalarını konteynere kopyalama
COPY . .

# 6. Aşama: 8000 portunu dış dünyaya açma
EXPOSE 8000

# 7. Aşama: Uvicorn sunucusunu başlatma (0.0.0.0 dış ağlardan gelen istekleri dinler)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
