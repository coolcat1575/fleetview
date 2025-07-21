FROM python:3.11-slim

WORKDIR /app
COPY app.py requirements.txt ./templates /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install ssh --no-install-recommends -y

ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
