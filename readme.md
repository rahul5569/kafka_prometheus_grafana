# Prometheus and Kafka Integration with Python Producer and Consumer

This project sets up a local environment to monitor Kafka-based applications using Prometheus and Grafana. It includes:

- **Prometheus**: Running locally to scrape metrics.
- **Kafka and Zookeeper**: Running in Docker containers.
- **Python Producer and Consumer**: Interacting with Kafka and exposing Prometheus metrics.
- **Grafana**: For advanced visualization of metrics.

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Project Setup](#2-project-setup)
3. [Installing Prometheus Locally](#3-installing-prometheus-locally)
4. [Setting Up Kafka and Zookeeper with Docker](#4-setting-up-kafka-and-zookeeper-with-docker)
5. [Creating Python Virtual Environment](#5-creating-python-virtual-environment)
6. [Creating Producer and Consumer Scripts](#6-creating-producer-and-consumer-scripts)
7. [Running the Services](#7-running-the-services)
8. [Verifying the Setup](#8-verifying-the-setup)
9. [Setting Up Grafana](#9-setting-up-grafana)
10. [Conclusion](#10-conclusion)

---

## 1. Prerequisites

Ensure that the following software is installed on your Windows machine:

- **Docker Desktop** (includes Docker Compose)
- **Python 3.8+**
- **Git** (optional, for version control)
- **PowerShell** or **Command Prompt**

### 1.1. Installing Docker Desktop

1. **Download Docker Desktop:**
   - Visit [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop) and download the installer.

2. **Install Docker Desktop:**
   - Run the downloaded installer.
   - Follow the on-screen instructions.
   - **Important:** During installation, ensure that the option **"Use WSL 2 instead of Hyper-V"** is selected for better performance (if your system supports it).

3. **Verify Installation:**
   - Open **PowerShell** or **Command Prompt**.
   - Run:
     ```powershell
     docker --version
     ```
     **Expected Output:**
     ```
     Docker version XX.XX.X, build XXXXXXX
     ```

### 1.2. Installing Python

1. **Download Python:**
   - Visit the [official Python website](https://www.python.org/downloads/windows/) and download the latest Python 3.x installer for Windows.

2. **Install Python:**
   - Run the installer.
   - **Important:** Check the box **"Add Python to PATH"** before clicking "Install Now".
   - Follow the on-screen instructions to complete the installation.

3. **Verify Installation:**
   - Open **PowerShell** or **Command Prompt**.
   - Run:
     ```powershell
     python --version
     ```
     **Expected Output:**
     ```
     Python 3.11.X
     ```

### 1.3. Installing Git (Optional)

1. **Download Git:**
   - Visit the [official Git website](https://git-scm.com/downloads) and download the Windows installer.

2. **Install Git:**
   - Run the installer.
   - Follow the on-screen instructions, accepting default settings unless specific configurations are needed.

3. **Verify Installation:**
   - Open **PowerShell** or **Command Prompt**.
   - Run:
     ```powershell
     git --version
     ```
     **Expected Output:**
     ```
     git version 2.X.X
     ```

---

## 2. Project Setup

We'll create a single project directory to organize all configurations and scripts.

1. **Open PowerShell as Administrator.**

2. **Navigate to Your Desired Location:**
   ```powershell
   cd C:\Users\rahul\Documents\GitHub\
   ```

3. **Create a New Project Directory:**
   ```powershell
   mkdir prometheus_kafka_integration
   cd prometheus_kafka_integration
   ```

4. **Initialize a Git Repository (Optional):**
   ```powershell
   git init
   ```

5. **Create Necessary Files:**
   ```powershell
   New-Item -Name "docker-compose.yml" -ItemType "File"
   New-Item -Name "prometheus.yml" -ItemType "File"
   New-Item -Name "producer.py" -ItemType "File"
   New-Item -Name "consumer.py" -ItemType "File"
   New-Item -Name "requirements.txt" -ItemType "File"
   ```

   **Final Directory Structure:**
   ```
   prometheus_kafka_integration/
   ├── docker-compose.yml
   ├── prometheus.yml
   ├── producer.py
   ├── consumer.py
   └── requirements.txt
   ```

---

## 3. Installing Prometheus Locally

We'll install Prometheus directly on your Windows machine without using Docker.

### 3.1. Download Prometheus

1. **Visit the Prometheus Download Page:**
   - Go to [Prometheus Downloads](https://prometheus.io/download/) and download the latest Windows `.zip` archive.

2. **Extract the Archive:**
   - Right-click the downloaded `.zip` file and select **"Extract All..."**.
   - Choose your desired extraction location, e.g., `C:\Prometheus`.

### 3.2. Configure Prometheus

1. **Navigate to Prometheus Directory:**
   ```powershell
   cd C:\Prometheus\prometheus-2.X.X.windows-amd64
   ```

2. **Create Configuration File (`prometheus.yml`):**
   - **Path:** `C:\Prometheus\prometheus-2.X.X.windows-amd64\prometheus.yml`
   - **Content:**
     ```yaml
     global:
       scrape_interval: 15s  # Default scrape interval

     scrape_configs:
       - job_name: 'prometheus'
         static_configs:
           - targets: ['localhost:9090']

       - job_name: 'kafka-producer'
         static_configs:
           - targets: ['localhost:8000']

       - job_name: 'kafka-consumer'
         static_configs:
           - targets: ['localhost:8001']
     ```

   **Explanation:**
   - **`prometheus` job:** Prometheus scrapes itself.
   - **`kafka-producer` job:** Scrapes metrics from the Producer application.
   - **`kafka-consumer` job:** Scrapes metrics from the Consumer application.

3. **Save and Close the File.**

### 3.3. Run Prometheus

1. **Run Prometheus Executable:**
   ```powershell
   .\prometheus.exe --config.file=prometheus.yml
   ```

2. **Verify Prometheus is Running:**
   - Open your web browser and navigate to [http://localhost:9090](http://localhost:9090).
   - You should see the Prometheus dashboard.

3. **(Optional) Run Prometheus as a Windows Service:**
   - To have Prometheus run in the background, consider using a tool like **NSSM (Non-Sucking Service Manager)**.
   - **Download NSSM:** [nssm.cc/download](https://nssm.cc/download)
   - **Install NSSM:**
     - Extract the downloaded archive.
     - Copy `nssm.exe` to a directory in your `PATH`, e.g., `C:\Windows\System32`.
   - **Create a Prometheus Service:**
     ```powershell
     nssm install Prometheus "C:\Prometheus\prometheus-2.X.X.windows-amd64\prometheus.exe" "--config.file=C:\Prometheus\prometheus-2.X.X.windows-amd64\prometheus.yml"
     ```
   - **Start the Service:**
     ```powershell
     nssm start Prometheus
     ```
   - **Verify Service is Running:**
     - Open **Services** (Run `services.msc`).
     - Find **Prometheus** in the list and ensure it's running.

---

## 4. Setting Up Kafka and Zookeeper with Docker

We'll use Docker Compose to run Kafka and Zookeeper containers.

### 4.1. Create Docker Compose File

1. **Navigate to Project Root:**
   ```powershell
   cd C:\Users\rahul\Documents\GitHub\prometheus_kafka_integration
   ```

2. **Edit `docker-compose.yml`:**
   - **Path:** `C:\Users\rahul\Documents\GitHub\prometheus_kafka_integration\docker-compose.yml`
   - **Content:**
     ```yaml
     version: "3.8"
     services:
       zookeeper:
         image: confluentinc/cp-zookeeper:latest
         container_name: zookeeper
         ports:
           - "2181:2181"
         environment:
           ZOOKEEPER_CLIENT_PORT: 2181

       kafka:
         image: confluentinc/cp-kafka:latest
         container_name: kafka
         ports:
           - "9092:9092"
         environment:
           KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
           KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
           KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
           KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1  # Set replication factor to 1
         depends_on:
           - zookeeper
     ```

   **Explanation:**
   - **`zookeeper` Service:** Uses Confluent's Zookeeper image, exposes port `2181`.
   - **`kafka` Service:** Uses Confluent's Kafka image, exposes port `9092`.
     - **Environment Variables:**
       - **`KAFKA_ZOOKEEPER_CONNECT`:** Connects Kafka to Zookeeper.
       - **`KAFKA_ADVERTISED_LISTENERS`:** Advertises Kafka broker to clients.
       - **`KAFKA_LISTENERS`:** Listens on all network interfaces.
       - **`KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR`:** Sets replication factor to `1` for simplicity.

3. **Start Kafka and Zookeeper Containers:**
   ```powershell
   docker-compose up -d
   ```

   **Explanation:**
   - **`up`:** Builds, (re)creates, starts, and attaches to containers.
   - **`-d`:** Runs containers in the background (detached mode).

4. **Verify Containers are Running:**
   ```powershell
   docker-compose ps
   ```

   **Expected Output:**
   ```
   Name                    Command               State                Ports
   --------------------------------------------------------------------------------
   prometheus_kafka_integration_zookeeper_1   /etc/confluent/docker/run   Up      0.0.0.0:2181->2181/tcp
   prometheus_kafka_integration_kafka_1       /etc/confluent/docker/run   Up      0.0.0.0:9092->9092/tcp
   ```

5. **(Optional) Check Logs:**
   ```powershell
   docker-compose logs -f kafka
   docker-compose logs -f zookeeper
   ```
   - Press `Ctrl + C` to stop log streaming.

---

## 5. Creating Python Virtual Environment

We'll set up a single Python virtual environment to manage dependencies for both the **Producer** and **Consumer** applications.

### 5.1. Create Virtual Environment

1. **Navigate to Project Root:**
   ```powershell
   cd C:\Users\rahul\Documents\GitHub\prometheus_kafka_integration
   ```

2. **Create Virtual Environment:**
   ```powershell
   python -m venv env
   ```

   **Explanation:**
   - **`env`**: Name of the virtual environment. You can choose any name you prefer.

### 5.2. Activate Virtual Environment

- **Windows:**
  ```powershell
  .\env\Scripts\Activate.ps1
  ```
  - **Note:** If you encounter an execution policy error, run PowerShell as Administrator and execute:
    ```powershell
    Set-ExecutionPolicy RemoteSigned
    ```
    Then, try activating again.

### 5.3. Install Dependencies

1. **Create `requirements.txt` in Project Root:**
   - **Path:** `C:\Users\rahul\Documents\GitHub\prometheus_kafka_integration\requirements.txt`
   - **Content:**
     ```plaintext
     git+https://github.com/dpkp/kafka-python.git#egg=kafka-python
     prometheus_client
     psutil
     ```

2. **Install Dependencies:**
   ```powershell
   pip install --break-system-packages -r requirements.txt
   ```

3. **Deactivate Virtual Environment (After Installation):**
   ```powershell
   deactivate
   ```

---

## 6. Creating Producer and Consumer Scripts

We'll develop Python scripts that interact with Kafka and expose Prometheus metrics. Both scripts reside in the project root.

### 6.1. Producer Script (`producer.py`)

1. **Create `producer.py`:**
   - **Path:** `C:\Users\rahul\Documents\GitHub\prometheus_kafka_integration\producer.py`

2. **Content:**
   ```python
   # producer.py

   import time
   import psutil
   from kafka import KafkaProducer
   from prometheus_client import start_http_server, Counter, Gauge
   import logging

   # Configure logging
   logging.basicConfig(level=logging.INFO)

   # Prometheus metrics
   MESSAGES_SENT = Counter('kafka_producer_messages_sent_total', 'Total number of messages sent by the producer')
   MEMORY_USAGE = Gauge('app_memory_usage', 'Current memory usage in MB')

   def get_memory_usage():
       process = psutil.Process()
       mem = process.memory_info().rss / (1024 * 1024)  # in MB
       MEMORY_USAGE.set(mem)

   def main():
       # Start Prometheus metrics server
       start_http_server(8000)
       logging.info("Producer metrics server started on port 8000")

       # Initialize Kafka producer
       producer = KafkaProducer(bootstrap_servers='localhost:9092')
       logging.info("Kafka Producer initialized")

       message_number = 0
       try:
           while True:
               message = f"Message {message_number}".encode('utf-8')
               producer.send('test-topic', message)
               producer.flush()
               MESSAGES_SENT.inc()
               get_memory_usage()
               logging.info(f"Produced: {message.decode('utf-8')}")
               message_number += 1
               time.sleep(1)  # Send a message every second
       except KeyboardInterrupt:
           logging.info("Producer stopped")
       finally:
           producer.close()

   if __name__ == "__main__":
       main()
   ```

   **Explanation:**
   - **Kafka Producer:** Sends messages to the `test-topic` Kafka topic every second.
   - **Prometheus Metrics:**
     - **`kafka_producer_messages_sent_total`:** Counts the total number of messages sent.
     - **`app_memory_usage`:** Tracks the current memory usage of the producer.

### 6.2. Consumer Script (`consumer.py`)

1. **Create `consumer.py`:**
   - **Path:** `C:\Users\rahul\Documents\GitHub\prometheus_kafka_integration\consumer.py`

2. **Content:**
   ```python
   # consumer.py

   import time
   import psutil
   from kafka import KafkaConsumer
   from prometheus_client import start_http_server, Counter, Gauge
   import logging

   # Configure logging
   logging.basicConfig(level=logging.INFO)

   # Prometheus metrics
   MESSAGES_CONSUMED = Counter('kafka_consumer_messages_consumed_total', 'Total number of messages consumed by the consumer')
   MEMORY_USAGE = Gauge('app_memory_usage', 'Current memory usage in MB')

   def get_memory_usage():
       process = psutil.Process()
       mem = process.memory_info().rss / (1024 * 1024)  # in MB
       MEMORY_USAGE.set(mem)

   def main():
       # Start Prometheus metrics server
       start_http_server(8001)
       logging.info("Consumer metrics server started on port 8001")

       # Initialize Kafka consumer
       consumer = KafkaConsumer(
           'test-topic',
           bootstrap_servers='localhost:9092',
           auto_offset_reset='earliest',
           enable_auto_commit=True,
           group_id='my-group'
       )
       logging.info("Kafka Consumer initialized")

       try:
           for message in consumer:
               MESSAGES_CONSUMED.inc()
               get_memory_usage()
               logging.info(f"Consumed: {message.value.decode('utf-8')}")
       except KeyboardInterrupt:
           logging.info("Consumer stopped")
       finally:
           consumer.close()

   if __name__ == "__main__":
       main()
   ```

   **Explanation:**
   - **Kafka Consumer:** Listens to the `test-topic` Kafka topic and consumes messages as they arrive.
   - **Prometheus Metrics:**
     - **`kafka_consumer_messages_consumed_total`:** Counts the total number of messages consumed.
     - **`app_memory_usage`:** Tracks the current memory usage of the consumer.

---

## 7. Running the Services

With all configurations and scripts in place, let's start the services.

### 7.1. Start Kafka and Zookeeper Containers

1. **Navigate to Project Root:**
   ```powershell
   cd C:\Users\rahul\Documents\GitHub\prometheus_kafka_integration
   ```

2. **Start Docker Compose Services:**
   ```powershell
   docker-compose up -d
   ```

   **Explanation:**
   - **`up`:** Builds, (re)creates, starts, and attaches to containers.
   - **`-d`:** Runs containers in the background (detached mode).

3. **Verify Containers are Running:**
   ```powershell
   docker-compose ps
   ```

   **Expected Output:**
   ```
   Name                    Command               State                Ports
   --------------------------------------------------------------------------------
   prometheus_kafka_integration_zookeeper_1   /etc/confluent/docker/run   Up      0.0.0.0:2181->2181/tcp
   prometheus_kafka_integration_kafka_1       /etc/confluent/docker/run   Up      0.0.0.0:9092->9092/tcp
   ```

4. **(Optional) Check Logs:**
   ```powershell
   docker-compose logs -f kafka
   docker-compose logs -f zookeeper
   ```
   - Press `Ctrl + C` to stop log streaming.

### 7.2. Run Prometheus Locally

1. **Start Prometheus:**
   - **If Running as a Service:** Ensure the Prometheus service is running via **NSSM**.
   - **If Running Manually:**
     - Open a new **PowerShell** window.
     - Navigate to Prometheus directory:
       ```powershell
       cd C:\Prometheus\prometheus-2.X.X.windows-amd64
       ```
     - Run Prometheus:
       ```powershell
       .\prometheus.exe --config.file=prometheus.yml
       ```
     - **Note:** Keep this window open as it runs Prometheus. To run in the background, consider using the service approach.

2. **Verify Prometheus is Running:**
   - Open your web browser and navigate to [http://localhost:9090](http://localhost:9090).
   - You should see the Prometheus dashboard.

### 7.3. Run Producer and Consumer Applications

We'll run both applications locally, leveraging the single virtual environment for simplicity.

#### 7.3.1. Run Producer

1. **Activate Virtual Environment:**
   ```powershell
   cd C:\Users\rahul\Documents\GitHub\prometheus_kafka_integration
   .\env\Scripts\Activate.ps1
   ```

2. **Run Producer Script:**
   ```powershell
   python producer.py
   ```

   **Expected Output:**
   ```
   INFO:root:Producer metrics server started on port 8000
   INFO:root:Kafka Producer initialized
   INFO:root:Produced: Message 0
   INFO:root:Produced: Message 1
   ...
   ```

3. **(Optional) Run in Background:**
   - **Method 1:** Open a new PowerShell window and run the script there.
   - **Method 2:** Use tools like **Git Bash** or **Windows Subsystem for Linux (WSL)** to run scripts in separate terminals.

#### 7.3.2. Run Consumer

1. **Open a New PowerShell Window.**

2. **Activate Virtual Environment:**
   ```powershell
   cd C:\Users\rahul\Documents\GitHub\prometheus_kafka_integration
   .\env\Scripts\Activate.ps1
   ```

3. **Run Consumer Script:**
   ```powershell
   python consumer.py
   ```

   **Expected Output:**
   ```
   INFO:root:Consumer metrics server started on port 8001
   INFO:root:Kafka Consumer initialized
   INFO:root:Consumed: Message 0
   INFO:root:Consumed: Message 1
   ...
   ```

---

## 8. Verifying the Setup

Let's ensure that all components are functioning correctly.

### 8.1. Access Prometheus Web Interface

1. **Open Your Web Browser.**

2. **Navigate to Prometheus:**
   ```
   http://localhost:9090
   ```

3. **Verify Prometheus is Running:**
   - You should see the Prometheus dashboard.

### 8.2. Check Prometheus Targets

1. **In Prometheus UI, Click on `Status` > `Targets`.**

2. **You Should See Three Scrape Jobs:**
   - **prometheus** (`localhost:9090`) → `UP`
   - **kafka-producer** (`localhost:8000`) → `UP`
   - **kafka-consumer** (`localhost:8001`) → `UP`

   ![Prometheus Targets](https://prometheus.io/assets/img/docs/targets.png)

### 8.3. Access Metrics Endpoints Directly

#### Producer Metrics:

- **URL:**
  ```
  http://localhost:8000/metrics
  ```

- **Expected Output:**
  ```
  # HELP kafka_producer_messages_sent_total Total number of messages sent by the producer
  # TYPE kafka_producer_messages_sent_total counter
  kafka_producer_messages_sent_total 10.0
  # HELP app_memory_usage Current memory usage in MB
  # TYPE app_memory_usage gauge
  app_memory_usage 15.2
  ...
  ```

#### Consumer Metrics:

- **URL:**
  ```
  http://localhost:8001/metrics
  ```

- **Expected Output:**
  ```
  # HELP kafka_consumer_messages_consumed_total Total number of messages consumed by the consumer
  # TYPE kafka_consumer_messages_consumed_total counter
  kafka_consumer_messages_consumed_total 10.0
  # HELP app_memory_usage Current memory usage in MB
  # TYPE app_memory_usage gauge
  app_memory_usage 20.3
  ...
  ```

### 8.4. Monitor Logs for Producer and Consumer

#### Producer Logs:

- **In the PowerShell Window Running Producer:**
  ```
  INFO:root:Producer metrics server started on port 8000
  INFO:root:Kafka Producer initialized
  INFO:root:Produced: Message 0
  INFO:root:Produced: Message 1
  ...
  ```

#### Consumer Logs:

- **In the PowerShell Window Running Consumer:**
  ```
  INFO:root:Consumer metrics server started on port 8001
  INFO:root:Kafka Consumer initialized
  INFO:root:Consumed: Message 0
  INFO:root:Consumed: Message 1
  ...
  ```

### 8.5. Query Metrics in Prometheus

1. **Navigate to Prometheus Web UI:**
   ```
   http://localhost:9090
   ```

2. **Use the "Graph" Tab:**
   - **Example Queries:**
     - **Producer Message Count:**
       ```
       kafka_producer_messages_sent_total
       ```
     - **Producer Memory Usage:**
       ```
       app_memory_usage
       ```
     - **Consumer Message Count:**
       ```
       kafka_consumer_messages_consumed_total
       ```
     - **Consumer Memory Usage:**
       ```
       app_memory_usage
       ```

3. **Execute Queries:**
   - Enter each metric in the query box and click `Execute` to visualize their values and trends.

---

## 9. Setting Up Grafana

Grafana provides advanced visualization capabilities for the metrics collected by Prometheus.

### 9.1. Run Grafana Using Docker

1. **Run Grafana Container:**
   ```powershell
   docker run -d --name=grafana -p 3000:3000 grafana/grafana:latest
   ```

   **Explanation:**
   - **`-d`**: Run container in detached mode.
   - **`--name=grafana`**: Name the container `grafana`.
   - **`-p 3000:3000`**: Map port `3000` of the container to port `3000` on the host.

2. **Verify Grafana is Running:**
   ```powershell
   docker ps
   ```
   **Expected Output:**
   ```
   CONTAINER ID   IMAGE                      COMMAND                  CREATED          STATUS          PORTS                    NAMES
   abcdef123456   grafana/grafana:latest     "/run.sh"                10 seconds ago   Up 9 seconds    0.0.0.0:3000->3000/tcp   grafana
   ```

### 9.2. Access Grafana Web Interface

1. **Open Your Web Browser.**

2. **Navigate to Grafana:**
   ```
   http://localhost:3000/
   ```

3. **Log In to Grafana:**
   - **Default Credentials:**
     - **Username:** `admin`
     - **Password:** `admin`
   - **Note:** You'll be prompted to change the password upon first login.

### 9.3. Add Prometheus as a Data Source

1. **After Logging In, Add Data Source:**
   - Click on the gear icon (⚙️) in the left sidebar.
   - Select **"Data Sources"**.
   - Click **"Add data source"**.

2. **Configure Prometheus Data Source:**
   - **Select Prometheus** from the list.
   - **URL:** `http://host.docker.internal:9090`
   - **Access:** Server (default)
   - Click **"Save & Test"** to verify the connection.

   **Expected Output:**
   ```
   Data source is working
   ```

### 9.4. Create a Sample Dashboard

1. **Create New Dashboard:**
   - Click the **"+"** icon in the left sidebar.
   - Select **"Dashboard"**.
   - Click **"Add new panel"**.

2. **Add Panels for Metrics:**

   - **Producer Message Count:**
     - **Query:**
       ```
       kafka_producer_messages_sent_total
       ```
     - **Visualization:** Choose `Graph`.
     - **Panel Title:** `Producer Message Count`.
     - Click **"Apply"**.

   - **Consumer Message Count:**
     - **Add another panel.**
     - **Query:**
       ```
       kafka_consumer_messages_consumed_total
       ```
     - **Visualization:** Choose `Graph`.
     - **Panel Title:** `Consumer Message Count`.
     - Click **"Apply"**.

   - **Producer Memory Usage:**
     - **Add another panel.**
     - **Query:**
       ```
       app_memory_usage
       ```
     - **Visualization:** Choose `Gauge` or `Graph`.
     - **Panel Title:** `Producer Memory Usage`.
     - Click **"Apply"**.

   - **Consumer Memory Usage:**
     - **Add another panel.**
     - **Query:**
       ```
       app_memory_usage
       ```
     - **Visualization:** Choose `Gauge` or `Graph`.
     - **Panel Title:** `Consumer Memory Usage`.
     - Click **"Apply"**.

3. **Organize and Save Dashboard:**
   - Arrange the panels as desired.
   - Click **"Save dashboard"**.
   - **Name:** `Kafka Monitoring Dashboard`.
   - Click **"Save"**.

   **Your Sample Dashboard Should Now Display:**
   - Total messages sent by the Producer.
   - Total messages consumed by the Consumer.
   - Current memory usage of both Producer and Consumer applications.

---

## 10. Conclusion

You've successfully set up a local environment with **Prometheus**, **Kafka**, and Python-based **Producer** and **Consumer** applications, along with **Grafana** for monitoring and visualization. Here's a quick recap:

1. **Installed Prerequisites:** Docker Desktop, Python, Git.
2. **Created Project Structure:** Organized all files within a single project directory.
3. **Set Up Prometheus Locally:** Installed and configured Prometheus to scrape metrics.
4. **Set Up Kafka and Zookeeper with Docker:** Ran Kafka services using Docker Compose.
5. **Developed Python Producer and Consumer:** Created scripts that interact with Kafka and expose Prometheus metrics.
6. **Configured Prometheus to Scrape Metrics:** Defined scrape targets in `prometheus.yml`.
7. **Ran and Verified Services:** Built and started containers, accessed Prometheus UI, verified metrics.
8. **Set Up Grafana:** Ran Grafana using Docker, added Prometheus as a data source, and created a sample dashboard.

### Next Steps:

- **Implement Alerting:** Set up Prometheus alerting rules to notify you of critical metrics thresholds.
- **Enhance Dashboards:** Customize Grafana dashboards to suit your monitoring needs.
- **Scale Applications:** Add more Producers or Consumers as required.
- **Secure Your Setup:** Implement authentication and encryption for production environments.

Feel free to reach out if you encounter any issues or need further assistance!

---