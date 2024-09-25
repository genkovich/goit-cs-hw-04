import multiprocessing
from collections import defaultdict
from pathlib import Path
import os
import timeit


def search_in_file(file_path, keywords, results_queue):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            for keyword in keywords:
                if keyword in content:
                    results_queue.put((keyword, file_path))
    except Exception as e:
        print(f"Error in {file_path}: {e}")



def process_task(files, keywords, results_queue):
    for file in files:
        search_in_file(file, keywords, results_queue)


def main_multiprocessing(file_paths, keywords):
    start_time = timeit.default_timer()
    num_processes = os.cpu_count() or 4

    processes = []
    results_queue = multiprocessing.Queue()
    results = defaultdict(list)
    for i in range(num_processes):
        process_files = file_paths[i::num_processes]
        if  process_files:
            process = multiprocessing.Process(target=process_task, args=(process_files, keywords, results_queue))
            processes.append(process)
            process.start()

    for process in processes:
        process.join()

    while not results_queue.empty():
        keyword, file_path = results_queue.get()
        results[keyword].append(file_path)

    end_time = timeit.default_timer()
    print(f"Execution time: {end_time - start_time} seconds")
    return results


if __name__ == '__main__':
    file_paths = list(Path("files").glob("*.txt"))
    print(f"File paths: {file_paths}\n")
    keywords = ['porta', 'diam', 'dictum']
    results = main_multiprocessing(file_paths, keywords)
    print(results)
