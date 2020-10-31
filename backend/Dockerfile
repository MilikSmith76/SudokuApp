FROM python:3.5-alpine

WORKDIR /scr/backend
ENV FLASK_APP app.py
RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY sudoku.py .
COPY app.py .
copy backendTest.py .

ENTRYPOINT ["python"]
CMD ["app.py"]
