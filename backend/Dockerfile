FROM python:3.10-slim-bullseye
WORKDIR /backend

COPY req.txt .        
RUN pip install -r req.txt

COPY . .                
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
