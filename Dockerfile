
FROM python:3.13.2-slim
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR app/
RUN git clone https://github.com/jakubmodrzewski/volume-analysis.git .


RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/main.py"]