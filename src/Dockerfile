FROM python:3.12-slim AS base-image

ENV VIRTUAL_VENV=/opt/venv
RUN python3 -m venv $VIRTUAL_VENV
ENV PATH="$VIRTUAL_VENV/bin:$PATH"

COPY requirements.txt .  

RUN pip install -r requirements.txt --no-cache-dir


FROM python:3.12-slim AS runtime-image

COPY --from=base-image /opt/venv /opt/venv 

WORKDIR /app

COPY . .

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8080

CMD [ "uvicorn", "test_api:app", "--host", "0.0.0.0", "--port", "8080" ]