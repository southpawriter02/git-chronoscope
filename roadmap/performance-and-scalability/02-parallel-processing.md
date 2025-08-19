# Parallel Processing

## 1. Feature Description

This feature leverages multiple CPU cores to speed up the time-lapse generation process by parallelizing the work.

## 2. Intended Functionality

- The tool will distribute the rendering of frames across multiple processes or threads.
- Each process/thread will work on a different commit, rendering the frame for that commit.
- The main process will then collect the rendered frames and stitch them together into a video in the correct order.
- The number of parallel workers should be configurable by the user or automatically detected based on the number of available CPU cores.

## 3. Requirements

- The application architecture needs to be designed to support parallelism. This might involve using a task queue or a thread pool.
- Care must be taken to avoid race conditions and other concurrency issues, especially when interacting with the Git repository or the cache.
- The performance benefits of parallelization should be benchmarked to ensure that the overhead of managing the parallel workers does not outweigh the gains.

## 4. Limitations

- Not all parts of the process can be parallelized. For example, checking out commits might need to be done sequentially. The final video encoding is also a sequential process.
- The effectiveness of parallelization will depend on the number of available CPU cores.
- Parallel processing can increase the complexity of the codebase and make debugging more difficult.
- The initial implementation might use a simple multiprocessing approach and may not be optimally tuned.
