# 1. ベースイメージとしてPython 3.9（または任意のバージョン）を使用
FROM python:3.11-slim

# 2. 作業ディレクトリを設定
WORKDIR /app

# 3. Chromeブラウザと関連依存パッケージをインストール
RUN apt update && apt install -y \
    wget \
    unzip \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && apt clean

# 4. ローカルのファイルをコンテナにコピー
COPY ./requirements.txt /app/requirements.txt
COPY ./main.py /app/main.py
COPY ./lib /app/lib

# 5. 依存パッケージのインストール
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# 6. ChromeDriverのインストール
RUN pip install webdriver-manager

# 7. UvicornでFastAPIを実行
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
