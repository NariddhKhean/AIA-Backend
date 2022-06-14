FROM python:3.8-buster

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-t", "120", "-w", "5", "-b", ":5000", "main:app"]
