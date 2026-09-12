#this is just a benchmark script for extraction using diff models
import json
import time

from llm.extractor import Extractor


TEST_MESSAGES = [
    "hello",
    "Good morning!",
    "thanks",
    "okay, got it",
    "yes",
    "bye",
    "that's great",
    "haha nice",
    "cool",
    "I see",

    "I'm learning machine learning.",
    "I'm studying neural networks.",
    "I'm learning Python for data science.",
    "What is an API?",
    "How does REST work?",
    "How do I use FastAPI?",
    "I'm learning about gradient descent.",
    "I'm studying computer networks.",
    "I'm learning about operating systems.",
    "I'm studying database normalization.",

    "I'm building a chatbot with Python.",
    "I'm implementing a CNN for image classification.",
    "I'm developing a REST API using Flask.",
    "I'm building a healthcare application.",
    "I'm implementing RAG for my project.",
    "I'm working on a robotic arm.",
    "I'm building a mobile app with React Native.",
    "I'm creating a recommendation system.",
    "I'm implementing authentication with JWT.",
    "I'm working on a neural network from scratch.",

    "My Flask API is returning a 500 error.",
    "I'm debugging a memory leak in my C++ program.",
    "My neural network isn't learning properly.",
    "I'm testing my REST API with Postman.",
    "My Arduino motor isn't responding.",
    "I'm fixing a bug in my Python code.",
    "The database connection keeps failing.",
    "I'm debugging an issue with Docker.",
    "My model is overfitting the training data.",
    "I'm trying to fix a CUDA error.",

    "I'm learning karate.",
    "I've started learning Spanish.",
    "I'm training for a marathon.",
    "I'm practicing guitar.",
    "I'm learning photography.",
    "I'm playing football this weekend.",
    "I'm starting a new drawing hobby.",
    "I'm reading a book about psychology.",
    "I'm taking a public speaking course.",
    "I'm practicing meditation."
]


def is_valid_schema(result):

    if not isinstance(result, dict):
        return False

    required_keys = {"topics", "entities", "intent"}

    if set(result.keys()) != required_keys:
        return False

    if not isinstance(result["topics"], list):
        return False

    if not isinstance(result["entities"], list):
        return False

    if not isinstance(result["intent"], str):
        return False

    return True


def run_benchmark():

    extractor = Extractor()

    results = []

    total_start = time.perf_counter()

    for index, message in enumerate(TEST_MESSAGES, start=1):

        start = time.perf_counter()

        try:
            result = extractor.extract(message)

            latency = time.perf_counter() - start

            valid = is_valid_schema(result)

            results.append({
                "number": index,
                "message": message,
                "result": result,
                "valid_json_schema": valid,
                "latency_seconds": round(latency, 3)
            })

            print(f"\n[{index}/50]")
            print(f"Message: {message}")
            print(f"Result: {result}")
            print(f"Latency: {latency:.3f}s")
            print(f"Valid: {valid}")

        except Exception as e:

            latency = time.perf_counter() - start

            results.append({
                "number": index,
                "message": message,
                "result": None,
                "valid_json_schema": False,
                "latency_seconds": round(latency, 3),
                "error": str(e)
            })

            print(f"\n[{index}/50]")
            print(f"Message: {message}")
            print(f"ERROR: {e}")
            print(f"Latency: {latency:.3f}s")

    total_time = time.perf_counter() - total_start

    valid_count = sum(
        result["valid_json_schema"]
        for result in results
    )

    latencies = [
        result["latency_seconds"]
        for result in results
    ]

    average_latency = sum(latencies) / len(latencies)

    print("\n" + "=" * 50)
    print("BENCHMARK SUMMARY")
    print("=" * 50)

    print(f"Total messages: {len(TEST_MESSAGES)}")
    print(f"Valid outputs: {valid_count}/{len(TEST_MESSAGES)}")
    print(
        f"JSON/schema validity: "
        f"{valid_count / len(TEST_MESSAGES) * 100:.2f}%"
    )
    print(f"Average latency: {average_latency:.3f}s")
    print(f"Total time: {total_time:.3f}s")

    with open("benchmark_results.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    print("\nResults saved to benchmark_results.json")


if __name__ == "__main__":
    run_benchmark()