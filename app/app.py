import os
from flask import Flask, jsonify
import psycopg

app = Flask(__name__)


def db_status():
    try:
        conn = psycopg.connect(
            host=os.getenv("DB_HOST", "postgres"),
            port=int(os.getenv("DB_PORT", "5432")),
            dbname=os.getenv("DB_NAME", "demo"),
            user=os.getenv("DB_USER", "demo"),
            password=os.environ["DB_PASSWORD"],
            connect_timeout=3,
        )
        with conn.cursor() as cur:
            cur.execute("SELECT current_database(), current_user")
            row = cur.fetchone()
        conn.close()
        return {"status": "SUCCESS", "database": row[0], "user": row[1]}
    except Exception as exc:
        return {"status": "FAILED", "error": str(exc)}


@app.get("/")
def index():
    status = db_status()
    return f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>VMware VKS Secret Store Demo</title>
  <style>
    body {{ font-family: Arial, sans-serif; max-width: 760px; margin: 60px auto; line-height: 1.6; }}
    .card {{ border: 1px solid #ddd; border-radius: 12px; padding: 28px; box-shadow: 0 4px 18px rgba(0,0,0,.06); }}
    .ok {{ color: #16803c; font-weight: 700; }}
    code {{ background: #f4f4f4; padding: 3px 6px; border-radius: 4px; }}
  </style>
</head>
<body>
<div class="card">
  <h1>VMware VKS Secret Store Demo</h1>
  <p><b>Application:</b> Flask</p>
  <p><b>Database:</b> PostgreSQL</p>
  <p><b>DB User:</b> {os.getenv('DB_USER', 'demo')}</p>
  <p><b>DB Password:</b> ********</p>
  <p><b>Connection:</b> <span class="ok">{status['status']}</span></p>
  <hr>
  <p><b>Secret source:</b> VCF Secret Store Service</p>
  <p><b>GitOps:</b> Argo CD</p>
  <p><b>Runtime:</b> VMware VKS</p>
</div>
</body>
</html>
""", 200 if status["status"] == "SUCCESS" else 503


@app.get("/healthz")
def healthz():
    return jsonify(status="ok")


@app.get("/readyz")
def readyz():
    status = db_status()
    return jsonify(status=status), (200 if status["status"] == "SUCCESS" else 503)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
