FROM python:3.10

RUN pip install poetry

COPY . .

RUN poetry install

EXPOSE 8000

ENTRYPOINT ["poetry","run","uvicorn", "--host","0.0.0.0","--port","8000","farmtool.main:app","--reload"]

