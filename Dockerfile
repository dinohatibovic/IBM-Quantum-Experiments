FROM python:3.12-slim

WORKDIR /repo

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY parse_ibm_json.py .
COPY data/ data/

ENTRYPOINT ["python", "parse_ibm_json.py"]
CMD ["--results_dir", "data/results", "--output", "data/quantum_results_verified.csv"]
