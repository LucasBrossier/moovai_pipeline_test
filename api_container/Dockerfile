FROM python:3.9

COPY ./requirements.txt /app/
COPY ./moovitamix_fastapi/* /app/

WORKDIR /app
RUN cd /app && python -m pip install -r requirements.txt
CMD ["python", "-m", "fastapi", "run", "main.py", "--port", "80"]