import os
import time
from google.cloud import pubsub_v1

# Point to our local Docker Pub/Sub emulator
os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"

PROJECT_ID = "career-copilot-local"
TOPIC_ID = "resume-analysis-topic"
SUBSCRIPTION_ID = "resume-analysis-sub"

def callback(message):
    print(f"📥 Received analysis task: {message.data.decode('utf-8')}")
    # Here we can trigger background processing
    message.ack()
    print("✅ Task processed and acknowledged.")

def start_worker():
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    
    # Ensure topic & subscription exist for local testing
    try:
        publisher.create_topic(request={"name": topic_path})
    except Exception:
        pass
        
    try:
        subscriber.create_subscription(request={"name": subscription_path, "topic": topic_path})
    except Exception:
        pass

    print(f"🚀 Pub/Sub Worker listening on {subscription_path}...")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()

if __name__ == "__main__":
    start_worker()