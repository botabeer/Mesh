# Bot Mesh - Prometheus Configuration
# Created by: Abeer Aldosari © 2025

global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: []

rule_files: []

scrape_configs:
  # Bot Mesh Application
  - job_name: 'bot-mesh'
    static_configs:
      - targets: ['bot:5000']
    metrics_path: '/metrics'
    scrape_interval: 10s

  # Redis Metrics (if using redis_exporter)
  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']
    scrape_interval: 30s

  # Prometheus self-monitoring
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']
