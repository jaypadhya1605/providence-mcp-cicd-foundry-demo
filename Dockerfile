FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY demo ./demo
COPY datasets ./datasets

ENV PORT=8000
ENV MCP_HTTP_PUBLIC_SAFE=true

EXPOSE 8000

CMD ["python", "-m", "demo.mcp_http_server", "--host", "0.0.0.0"]
