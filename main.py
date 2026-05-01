from fastapi import FastAPI
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Gauge, Histogram, start_http_server

app = FastAPI()

# Prometheus metrikalari uchun kengaytirilgan funksiyalar
class PrometheusMetrics:
    def __init__(self):
        self.requests_total = Counter('requests_total', 'Jami talablar soni')
        self.response_time = Histogram('response_time', 'Talablar davomiyligi')
        self.successful_requests = Gauge('successful_requests', 'Muvaffaqiyatli talablar soni')

    def increment_requests_total(self):
        self.requests_total.inc()

    def record_response_time(self, response_time):
        self.response_time.observe(response_time)

    def increment_successful_requests(self):
        self.successful_requests.inc()

metrics = PrometheusMetrics()

# FastAPI uchun endpoint
@app.get("/")
async def read_root():
    metrics.increment_requests_total()
    response_time = 0.5  # Davomiyligi 0.5 soniya qilib ko'rsatish uchun
    metrics.record_response_time(response_time)
    metrics.increment_successful_requests()
    return JSONResponse(content={"message": "Salom, dunyo!"}, media_type="application/json")

# Prometheus uchun endpoint
@app.get("/metrics")
async def read_metrics():
    metrics.increment_requests_total()
    return JSONResponse(content=metrics.requests_total._value, media_type="text/plain")

# Prometheus serverni boshlash uchun funksiya
def start_prometheus_server():
    start_http_server(8000)

if __name__ == "__main__":
    start_prometheus_server()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

Bu kodda FastAPI uchun endpoint yaratilgan bo'lib, u har safar talab qilinganda Prometheus metrikalari uchun kengaytirilgan funksiyalarni ishlatadi. Prometheus uchun endpoint ham yaratilgan bo'lib, u har safar talab qilinganda talablar sonini keltiradi. Prometheus serverni boshlash uchun funksiya ham yaratilgan bo'lib, u 8000 portida ishlaydi. FastAPI serveri 8001 portida ishlaydi.
