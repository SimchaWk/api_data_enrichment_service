import os

os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

import torch
from transformers import pipeline
import time
import statistics


def run_performance_test(device_type='cpu', num_samples=10):
    device = 0 if device_type == 'gpu' and torch.cuda.is_available() else -1

    # מערך טקסטים לבדיקה
    texts = [
        "A bomb exploded in the city center, causing multiple casualties.",
        "The stock market showed significant growth today.",
        "A peaceful protest was held in the town square.",
        "Scientists discover new species in Amazon rainforest.",
        "An armed group attacked the embassy yesterday."
    ]

    # טעינת המודל
    print(f"\nLoading model on {device_type.upper()}...")
    start_load = time.time()
    classifier = pipeline("zero-shot-classification",
                          model="facebook/bart-large-mnli",
                          device=device)
    load_time = time.time() - start_load
    print(f"Model load time: {load_time:.2f} seconds")

    # מדידת זמני סיווג
    classification_times = []
    for _ in range(num_samples):
        for text in texts:
            start = time.time()
            _ = classifier(text, ["terrorism related", "not terrorism related"])
            classification_times.append(time.time() - start)

    return {
        'load_time': load_time,
        'avg_classification': statistics.mean(classification_times),
        'min_classification': min(classification_times),
        'max_classification': max(classification_times),
        'std_dev': statistics.stdev(classification_times)
    }


if __name__ == '__main__':
    print("=== Performance Comparison ===")

    # בדיקת CPU
    cpu_results = run_performance_test('cpu')

    # בדיקת GPU
    gpu_results = run_performance_test('gpu')

    print("\n=== Results Summary ===")
    print(f"{'Metric':<20} {'CPU':>10} {'GPU':>10} {'Speedup':>10}")
    print("-" * 50)
    print(
        f"Load Time (s):{cpu_results['load_time']:>10.2f}{gpu_results['load_time']:>10.2f}{cpu_results['load_time'] / gpu_results['load_time']:>10.1f}x")
    print(
        f"Avg Class. (s):{cpu_results['avg_classification']:>10.2f}{gpu_results['avg_classification']:>10.2f}{cpu_results['avg_classification'] / gpu_results['avg_classification']:>10.1f}x")
    print(
        f"Min Class. (s):{cpu_results['min_classification']:>10.2f}{gpu_results['min_classification']:>10.2f}{cpu_results['min_classification'] / gpu_results['min_classification']:>10.1f}x")
    print(
        f"Max Class. (s):{cpu_results['max_classification']:>10.2f}{gpu_results['max_classification']:>10.2f}{cpu_results['max_classification'] / gpu_results['max_classification']:>10.1f}x")
    print(f"Std Dev (s):{cpu_results['std_dev']:>10.2f}{gpu_results['std_dev']:>10.2f}")
