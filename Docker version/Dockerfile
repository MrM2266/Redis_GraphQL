FROM python:3.10.1
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8001

CMD ["uvicorn", "gql:app", "--host", "0.0.0.0", "--port", "8000"]