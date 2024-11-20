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
