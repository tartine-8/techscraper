FROM python:3.11-slim AS scraper-stage
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*
COPY requirements-scraper.txt .
RUN pip install --no-cache-dir -r requirements-scraper.txt
COPY scraper.py .
COPY utils.py .
ENTRYPOINT ["python", "scraper.py"]

FROM scraper-stage AS full-stage
COPY requirements-analysis.txt .
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements-analysis.txt
RUN python -m spacy download en_core_web_sm
COPY analysis.ipynb .
EXPOSE 8888
ENTRYPOINT []
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]