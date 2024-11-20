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
