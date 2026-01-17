# Smart Defect Detection & Observability System 🚀

An automated API monitoring system that categorizes defects (Network vs. Logic vs. Infra) and visualizes real-time health using InfluxDB and Grafana.

##  Features
- **Real-time Monitoring:** Checks API endpoints every 10 seconds.
- **Smart Categorization:** Automatically identifies root causes (HTTP 5xx, 4xx, Timeouts).
- **Time-series Visualization:** Professional Grafana dashboard for MTTD reduction.
- **Containerized:** Easy setup with Docker Compose.

##  Tech Stack
- **Language:** Python 3.x
- **Database:** InfluxDB 2.7
- **Visualization:** Grafana
- **Infrastructure:** Docker & Docker Compose

##  Getting Started
1. Clone this repository.
2. Run infrastructure: `docker-compose -f infrastructure/docker-compose.yml up -d`
3. Install dependencies: `pip install -r requirements.txt`
4. Setup your `.env` file based on `.env.example`.
5. Run monitor: `python3 scripts/api_monitor.py`

##  Dashboard Preview

<img width="1173" height="1059" alt="Screenshot 2569-01-18 at 02 18 05" src="https://github.com/user-attachments/assets/2cfa173e-4d60-45ca-818d-ee8371a646ef" />

<img width="1094" height="865" alt="Screenshot 2569-01-18 at 02 18 27" src="https://github.com/user-attachments/assets/87a60eb7-c5eb-40ac-8063-827875635152" />
