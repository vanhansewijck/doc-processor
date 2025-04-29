import asyncio
from bullmq import Worker, Job
import signal
import os
from dotenv import load_dotenv
from process_doc import process_document

load_dotenv()

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_password = os.getenv("REDIS_PASSWORD", "")
queue_name = os.getenv("QUEUE_NAME", "doc-processor")

async def process_document_async(input_path, chunks_path, markdown_path):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, process_document, input_path, chunks_path, markdown_path)

async def process(job:Job, job_token:str):
    print("Processing job:", job_token)
    input_path = job.data["inputFilePath"]
    chunks_path = job.data["chunkedJsonOutputFilePath"]
    markdown_path = job.data["markdownOutputFilePath"]

    await process_document_async(input_path, chunks_path, markdown_path)

    print("Job completed:", job_token)

async def main():
    # Create an event that will be triggered for shutdown
    shutdown_event = asyncio.Event()

    def signal_handler(signal, frame):
        print("Signal received, shutting down.")
        shutdown_event.set()

    # Assign signal handlers to SIGTERM and SIGINT
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Feel free to remove the connection parameter, if your redis runs on localhost
    redis = {"host": redis_host, "port": redis_port, "password": redis_password}
    worker = Worker(queue_name, process, {"connection": redis})
    print("Worker started")

    # Wait until the shutdown event is set
    await shutdown_event.wait()

    # close the worker
    print("Cleaning up worker...")
    await worker.close()
    print("Worker shut down successfully.")

if __name__ == "__main__":
    asyncio.run(main())