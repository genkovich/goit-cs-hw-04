import threading
import timeit
from collections import defaultdict
from pathlib import Path
import os


def search_in_file(file_path, keywords, results):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    results[keyword].append(file_path)
    except Exception as e:
        print(f"Error in {file_path}: {e}")


def thread_task(files, keywords, results):
    for file in files:
        search_in_file(file, keywords, results)


def main_threading(file_paths, keywords):
    start_time = timeit.default_timer()

    num_threads = os.cpu_count() or 4
    threads = []
    results = defaultdict(list)
    for i in range(num_threads):
        thread_files = file_paths[i::num_threads]
        thread = threading.Thread(target=thread_task, args=(thread_files, keywords, results))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = timeit.default_timer()
    print(f"Execution time: {end_time - start_time} seconds")
    return results


if __name__ == '__main__':
    file_paths = list(Path("files").glob("*.txt"))
    print(f"File paths: {file_paths}\n")
    keywords = ['porta', 'diam', 'dictum']
    results = main_threading(file_paths, keywords)
    print(results)
