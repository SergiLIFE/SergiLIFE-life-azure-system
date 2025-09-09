"""
L.I.F.E Theory Module 5: Real-Time Processing Engine
High-performance real-time processing with adaptive optimization

Copyright 2025 - Sergio Paya Borrull
"""

import concurrent.futures
import logging
import multiprocessing as mp
import queue
import threading
import time
from collections import deque
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np

# Import L.I.F.E Theory core
from lifetheory import AdaptationParameters, CoreLIFEAlgorithm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProcessingMode(Enum):
    """Real-time processing modes"""

    STREAMING = "streaming"
    BATCH = "batch"
    HYBRID = "hybrid"
    ADAPTIVE = "adaptive"
    PARALLEL = "parallel"
    DISTRIBUTED = "distributed"


class PriorityLevel(Enum):
    """Processing priority levels"""

    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    BACKGROUND = 4


class ProcessingState(Enum):
    """Processing engine states"""

    IDLE = "idle"
    PROCESSING = "processing"
    ADAPTING = "adapting"
    OPTIMIZING = "optimizing"
    ERROR = "error"
    SHUTDOWN = "shutdown"


@dataclass
class ProcessingTask:
    """Processing task definition"""

    task_id: str = ""
    data: Any = None
    priority: PriorityLevel = PriorityLevel.NORMAL
    processing_function: Optional[Callable] = None
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    deadline: Optional[datetime] = None
    dependencies: List[str] = field(default_factory=list)
    estimated_duration: float = 1.0

    def __post_init__(self):
        if not self.task_id:
            self.task_id = f"task_{int(time.time() * 1000000)}"


@dataclass
class ProcessingResult:
    """Processing result structure"""

    task_id: str = ""
    success: bool = False
    result_data: Any = None
    processing_time: float = 0.0
    error_message: str = ""
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    adaptation_feedback: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class PerformanceMetrics:
    """Real-time performance metrics"""

    throughput: float = 0.0  # Tasks per second
    latency: float = 0.0  # Average processing time
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    queue_length: int = 0
    error_rate: float = 0.0
    adaptation_score: float = 0.5
    efficiency_ratio: float = 0.0


class LIFERealTimeProcessor:
    """High-performance real-time processor with L.I.F.E adaptation"""

    def __init__(self, max_workers: int = None, buffer_size: int = 10000):
        self.max_workers = max_workers or min(32, (mp.cpu_count() or 1) + 4)
        self.buffer_size = buffer_size

        # Initialize L.I.F.E algorithm for adaptive optimization
        self.life_algorithm = CoreLIFEAlgorithm(
            learning_rate=0.05,
            max_experiences=50000,
            adaptation_params=AdaptationParameters(
                learning_rate=0.05, decay_factor=0.8, threshold=0.25
            ),
        )

        # Processing queues with priority support
        self.task_queues = {
            priority: queue.PriorityQueue(maxsize=buffer_size)
            for priority in PriorityLevel
        }

        # Result storage
        self.result_queue = queue.Queue(maxsize=buffer_size * 2)
        self.completed_tasks = {}

        # Worker management
        self.workers = []
        self.worker_stats = {}
        self.executor = None

        # State management
        self.current_state = ProcessingState.IDLE
        self.state_history = deque(maxlen=1000)

        # Performance tracking
        self.performance_metrics = PerformanceMetrics()
        self.metrics_history = deque(maxlen=10000)
        self.task_completion_times = deque(maxlen=1000)

        # Real-time adaptation
        self.adaptation_frequency = 100  # Adapt every N tasks
        self.tasks_processed = 0
        self.last_adaptation = datetime.now()

        # Threading synchronization
        self.processing_lock = threading.RLock()
        self.metrics_lock = threading.Lock()
        self.shutdown_event = threading.Event()

        # Monitoring thread
        self.monitor_thread = None
        self.monitor_interval = 1.0  # seconds

        # Load balancing
        self.load_balancer = LIFELoadBalancer(self.max_workers)

        logger.info(
            f"L.I.F.E Real-Time Processor initialized with {self.max_workers} workers"
        )

    def start(self):
        """Start the real-time processing engine"""
        try:
            if self.current_state != ProcessingState.IDLE:
                logger.warning("Processor already started")
                return

            self._change_state(ProcessingState.PROCESSING)

            # Start thread pool executor
            self.executor = concurrent.futures.ThreadPoolExecutor(
                max_workers=self.max_workers, thread_name_prefix="LIFEProcessor"
            )

            # Start worker threads
            for i in range(self.max_workers):
                worker = threading.Thread(
                    target=self._worker_loop,
                    args=(i,),
                    name=f"LIFEWorker-{i}",
                    daemon=True,
                )
                worker.start()
                self.workers.append(worker)
                self.worker_stats[i] = {
                    "tasks_processed": 0,
                    "total_processing_time": 0.0,
                    "errors": 0,
                    "last_active": datetime.now(),
                }

            # Start monitoring thread
            self.monitor_thread = threading.Thread(
                target=self._monitor_loop, name="LIFEMonitor", daemon=True
            )
            self.monitor_thread.start()

            # Start result processor
            self.result_processor_thread = threading.Thread(
                target=self._process_results, name="LIFEResultProcessor", daemon=True
            )
            self.result_processor_thread.start()

            logger.info("Real-time processor started successfully")

        except Exception as e:
            logger.error(f"Error starting processor: {str(e)}")
            self._change_state(ProcessingState.ERROR)

    def stop(self):
        """Stop the real-time processing engine"""
        try:
            logger.info("Stopping real-time processor...")

            # Signal shutdown
            self.shutdown_event.set()
            self._change_state(ProcessingState.SHUTDOWN)

            # Wait for workers to finish current tasks
            if self.executor:
                self.executor.shutdown(wait=True, timeout=30.0)

            # Wait for threads to complete
            for worker in self.workers:
                worker.join(timeout=5.0)

            if self.monitor_thread:
                self.monitor_thread.join(timeout=5.0)

            logger.info("Real-time processor stopped")

        except Exception as e:
            logger.error(f"Error stopping processor: {str(e)}")

    def submit_task(self, task: ProcessingTask) -> bool:
        """Submit a task for processing"""
        try:
            if self.current_state not in [
                ProcessingState.PROCESSING,
                ProcessingState.ADAPTING,
            ]:
                logger.warning("Processor not ready for tasks")
                return False

            # Add task to appropriate priority queue
            priority_queue = self.task_queues[task.priority]

            # Create priority tuple (priority value, timestamp, task)
            priority_item = (task.priority.value, task.timestamp.timestamp(), task)

            # Try to add to queue (non-blocking)
            try:
                priority_queue.put_nowait(priority_item)
                logger.debug(
                    f"Task {task.task_id} submitted with priority {task.priority.name}"
                )
                return True
            except queue.Full:
                logger.warning(f"Queue full for priority {task.priority.name}")
                return False

        except Exception as e:
            logger.error(f"Error submitting task {task.task_id}: {str(e)}")
            return False

    def get_result(
        self, task_id: str, timeout: float = None
    ) -> Optional[ProcessingResult]:
        """Get processing result for a task"""
        try:
            # Check completed tasks first
            if task_id in self.completed_tasks:
                return self.completed_tasks[task_id]

            # Wait for result if timeout specified
            if timeout:
                end_time = time.time() + timeout
                while time.time() < end_time:
                    if task_id in self.completed_tasks:
                        return self.completed_tasks[task_id]
                    time.sleep(0.01)  # 10ms polling

            return None

        except Exception as e:
            logger.error(f"Error getting result for task {task_id}: {str(e)}")
            return None

    def process_streaming_data(
        self, data_stream: Any, processing_function: Callable, chunk_size: int = 100
    ) -> List[ProcessingResult]:
        """Process streaming data in real-time"""
        try:
            results = []
            chunk_count = 0

            # Process data in chunks
            while True:
                try:
                    # Get data chunk (implementation depends on stream type)
                    chunk = self._get_data_chunk(data_stream, chunk_size)
                    if chunk is None or len(chunk) == 0:
                        break

                    # Create processing task
                    task = ProcessingTask(
                        task_id=f"stream_chunk_{chunk_count}",
                        data=chunk,
                        processing_function=processing_function,
                        priority=PriorityLevel.HIGH,
                        context={"stream_mode": True, "chunk_index": chunk_count},
                    )

                    # Submit task
                    if self.submit_task(task):
                        # Wait for result with timeout
                        result = self.get_result(task.task_id, timeout=10.0)
                        if result:
                            results.append(result)
                        else:
                            logger.warning(f"Timeout waiting for chunk {chunk_count}")

                    chunk_count += 1

                    # Adaptive delay based on performance
                    if chunk_count % 10 == 0:
                        self._adaptive_streaming_delay()

                except StopIteration:
                    break
                except Exception as e:
                    logger.error(
                        f"Error processing stream chunk {chunk_count}: {str(e)}"
                    )
                    continue

            logger.info(
                f"Streaming processing completed: {len(results)} chunks processed"
            )
            return results

        except Exception as e:
            logger.error(f"Error in streaming processing: {str(e)}")
            return []

    def _worker_loop(self, worker_id: int):
        """Main worker processing loop"""
        logger.debug(f"Worker {worker_id} started")

        while not self.shutdown_event.is_set():
            try:
                # Get next task from priority queues
                task = self._get_next_task(timeout=1.0)

                if task is None:
                    continue

                # Process the task
                result = self._process_task(task, worker_id)

                # Store result
                self.result_queue.put(result)

                # Update worker stats
                with self.metrics_lock:
                    self.worker_stats[worker_id]["tasks_processed"] += 1
                    self.worker_stats[worker_id][
                        "total_processing_time"
                    ] += result.processing_time
                    self.worker_stats[worker_id]["last_active"] = datetime.now()

                    if not result.success:
                        self.worker_stats[worker_id]["errors"] += 1

                # Trigger adaptation if needed
                self.tasks_processed += 1
                if self.tasks_processed % self.adaptation_frequency == 0:
                    self._trigger_adaptation()

            except Exception as e:
                logger.error(f"Error in worker {worker_id}: {str(e)}")
                time.sleep(0.1)  # Brief pause on error

        logger.debug(f"Worker {worker_id} stopped")

    def _get_next_task(self, timeout: float = 1.0) -> Optional[ProcessingTask]:
        """Get next task from priority queues"""
        try:
            # Check queues in priority order
            for priority in PriorityLevel:
                queue_obj = self.task_queues[priority]

                if not queue_obj.empty():
                    try:
                        _, _, task = queue_obj.get_nowait()
                        return task
                    except queue.Empty:
                        continue

            # If no tasks available, wait briefly
            time.sleep(min(timeout, 0.1))
            return None

        except Exception as e:
            logger.error(f"Error getting next task: {str(e)}")
            return None

    def _process_task(self, task: ProcessingTask, worker_id: int) -> ProcessingResult:
        """Process a single task"""
        start_time = time.time()
        result = ProcessingResult(task_id=task.task_id)

        try:
            # Check dependencies
            if task.dependencies:
                if not self._check_dependencies(task.dependencies):
                    result.error_message = "Dependencies not satisfied"
                    result.processing_time = time.time() - start_time
                    return result

            # Execute processing function
            if task.processing_function:
                # Add worker context
                task.context["worker_id"] = worker_id
                task.context["processing_start"] = start_time

                # Call processing function
                result.result_data = task.processing_function(task.data, task.context)
                result.success = True
            else:
                # Default processing (echo)
                result.result_data = task.data
                result.success = True

            # Calculate performance metrics
            processing_time = time.time() - start_time
            result.processing_time = processing_time

            # Performance metrics
            result.performance_metrics = {
                "processing_time": processing_time,
                "worker_id": worker_id,
                "queue_time": (start_time - task.timestamp.timestamp()),
                "memory_delta": self._estimate_memory_usage(),
                "cpu_time": processing_time,  # Simplified
            }

            # L.I.F.E adaptation feedback
            adaptation_input = np.array(
                [
                    processing_time,
                    1.0 if result.success else 0.0,
                    len(str(task.data)) / 1000.0,  # Data size estimate
                    task.priority.value / 4.0,  # Normalized priority
                    worker_id / self.max_workers,  # Worker load
                ]
            )

            life_output = self.life_algorithm.process(adaptation_input, task.context)
            result.adaptation_feedback = life_output

        except Exception as e:
            result.success = False
            result.error_message = str(e)
            result.processing_time = time.time() - start_time
            logger.error(f"Error processing task {task.task_id}: {str(e)}")

        return result

    def _process_results(self):
        """Process completed task results"""
        while not self.shutdown_event.is_set():
            try:
                # Get result from queue
                try:
                    result = self.result_queue.get(timeout=1.0)
                except queue.Empty:
                    continue

                # Store completed result
                self.completed_tasks[result.task_id] = result

                # Update performance metrics
                self._update_performance_metrics(result)

                # Clean old completed tasks
                if len(self.completed_tasks) > 10000:
                    self._cleanup_old_results()

            except Exception as e:
                logger.error(f"Error processing results: {str(e)}")
                time.sleep(0.1)

    def _monitor_loop(self):
        """Monitor system performance and adapt"""
        while not self.shutdown_event.is_set():
            try:
                # Update performance metrics
                self._calculate_system_metrics()

                # Check for adaptation triggers
                self._check_adaptation_triggers()

                # Log performance periodically
                if self.tasks_processed % 1000 == 0 and self.tasks_processed > 0:
                    self._log_performance_summary()

                time.sleep(self.monitor_interval)

            except Exception as e:
                logger.error(f"Error in monitor loop: {str(e)}")
                time.sleep(1.0)

    def _calculate_system_metrics(self):
        """Calculate current system performance metrics"""
        try:
            with self.metrics_lock:
                current_time = time.time()

                # Calculate throughput (tasks per second)
                if len(self.task_completion_times) >= 2:
                    recent_completions = [
                        t
                        for t in self.task_completion_times
                        if current_time - t < 60.0  # Last minute
                    ]
                    self.performance_metrics.throughput = len(recent_completions) / 60.0

                # Calculate average latency
                if self.metrics_history:
                    recent_metrics = list(self.metrics_history)[-100:]  # Last 100 tasks
                    processing_times = [
                        m.processing_time
                        for m in recent_metrics
                        if hasattr(m, "processing_time")
                    ]
                    if processing_times:
                        self.performance_metrics.latency = np.mean(processing_times)

                # Calculate queue lengths
                total_queue_length = sum(q.qsize() for q in self.task_queues.values())
                self.performance_metrics.queue_length = total_queue_length

                # Calculate error rate
                if self.metrics_history:
                    recent_results = list(self.metrics_history)[
                        -1000:
                    ]  # Last 1000 tasks
                    error_count = sum(
                        1
                        for r in recent_results
                        if hasattr(r, "success") and not r.success
                    )
                    self.performance_metrics.error_rate = error_count / max(
                        1, len(recent_results)
                    )

                # Get L.I.F.E adaptation score
                life_metrics = self.life_algorithm.get_performance_metrics()
                self.performance_metrics.adaptation_score = life_metrics.get(
                    "overall_performance", 0.5
                )

                # Calculate efficiency ratio
                if (
                    self.performance_metrics.throughput > 0
                    and self.performance_metrics.latency > 0
                ):
                    self.performance_metrics.efficiency_ratio = (
                        self.performance_metrics.throughput
                        / self.performance_metrics.latency
                    )

                # System resource usage (simplified)
                self.performance_metrics.cpu_usage = min(
                    1.0, total_queue_length / (self.max_workers * 10)
                )
                self.performance_metrics.memory_usage = (
                    len(self.completed_tasks) / 10000.0
                )

        except Exception as e:
            logger.error(f"Error calculating system metrics: {str(e)}")

    def _trigger_adaptation(self):
        """Trigger L.I.F.E adaptation process"""
        try:
            if self.current_state != ProcessingState.PROCESSING:
                return

            self._change_state(ProcessingState.ADAPTING)

            # Perform adaptations based on current performance
            adaptations_made = []

            # Adapt worker count
            if self.performance_metrics.queue_length > self.max_workers * 5:
                if self._can_add_workers():
                    self._add_worker()
                    adaptations_made.append("added_worker")
            elif (
                self.performance_metrics.queue_length < self.max_workers
                and len(self.workers) > 2
            ):
                if self._can_remove_workers():
                    self._remove_worker()
                    adaptations_made.append("removed_worker")

            # Adapt processing frequency
            if self.performance_metrics.error_rate > 0.1:
                self.adaptation_frequency = min(200, self.adaptation_frequency + 10)
                adaptations_made.append("increased_adaptation_frequency")
            elif self.performance_metrics.error_rate < 0.01:
                self.adaptation_frequency = max(50, self.adaptation_frequency - 5)
                adaptations_made.append("decreased_adaptation_frequency")

            # Adapt monitoring interval
            if self.performance_metrics.throughput > 100:
                self.monitor_interval = max(0.5, self.monitor_interval - 0.1)
                adaptations_made.append("increased_monitoring_frequency")
            elif self.performance_metrics.throughput < 10:
                self.monitor_interval = min(5.0, self.monitor_interval + 0.2)
                adaptations_made.append("decreased_monitoring_frequency")

            self.last_adaptation = datetime.now()
            self._change_state(ProcessingState.PROCESSING)

            if adaptations_made:
                logger.info(f"Adaptations made: {', '.join(adaptations_made)}")

        except Exception as e:
            logger.error(f"Error in adaptation: {str(e)}")
            self._change_state(ProcessingState.PROCESSING)

    # Helper methods (simplified implementations)
    def _change_state(self, new_state: ProcessingState):
        """Change processor state"""
        old_state = self.current_state
        self.current_state = new_state
        self.state_history.append((datetime.now(), old_state, new_state))
        logger.debug(f"State changed: {old_state.value} -> {new_state.value}")

    def _get_data_chunk(self, data_stream: Any, chunk_size: int) -> Optional[List]:
        """Get chunk of data from stream (placeholder implementation)"""
        # This would be implemented based on the specific stream type
        if hasattr(data_stream, "__iter__"):
            try:
                chunk = []
                for _ in range(chunk_size):
                    chunk.append(next(data_stream))
                return chunk if chunk else None
            except StopIteration:
                return None
        return None

    def _adaptive_streaming_delay(self):
        """Calculate adaptive delay for streaming processing"""
        if self.performance_metrics.queue_length > self.max_workers * 2:
            time.sleep(0.1)  # Slow down if queues are full
        elif self.performance_metrics.throughput < 10:
            time.sleep(0.01)  # Speed up if throughput is low

    def _check_dependencies(self, dependencies: List[str]) -> bool:
        """Check if task dependencies are satisfied"""
        return all(dep_id in self.completed_tasks for dep_id in dependencies)

    def _estimate_memory_usage(self) -> float:
        """Estimate current memory usage"""
        return len(self.completed_tasks) * 0.001  # Simplified estimate

    def _update_performance_metrics(self, result: ProcessingResult):
        """Update performance metrics with new result"""
        try:
            with self.metrics_lock:
                self.metrics_history.append(result)
                self.task_completion_times.append(time.time())

                # Trim history
                if len(self.metrics_history) > 10000:
                    self.metrics_history = deque(
                        list(self.metrics_history)[-5000:], maxlen=10000
                    )

        except Exception as e:
            logger.error(f"Error updating performance metrics: {str(e)}")

    def _cleanup_old_results(self):
        """Clean up old completed task results"""
        try:
            # Remove results older than 1 hour
            cutoff_time = datetime.now() - timedelta(hours=1)

            old_task_ids = [
                task_id
                for task_id, result in self.completed_tasks.items()
                if result.timestamp < cutoff_time
            ]

            for task_id in old_task_ids:
                del self.completed_tasks[task_id]

            if old_task_ids:
                logger.debug(f"Cleaned up {len(old_task_ids)} old results")

        except Exception as e:
            logger.error(f"Error cleaning up old results: {str(e)}")

    def _check_adaptation_triggers(self):
        """Check if adaptation should be triggered"""
        try:
            # Time-based trigger
            time_since_adaptation = (
                datetime.now() - self.last_adaptation
            ).total_seconds()
            if time_since_adaptation > 60.0:  # Adapt at least every minute
                self._trigger_adaptation()
                return

            # Performance-based triggers
            if self.performance_metrics.error_rate > 0.2:  # High error rate
                self._trigger_adaptation()
            elif (
                self.performance_metrics.queue_length > self.max_workers * 10
            ):  # Queue overflow
                self._trigger_adaptation()
            elif self.performance_metrics.latency > 10.0:  # High latency
                self._trigger_adaptation()

        except Exception as e:
            logger.error(f"Error checking adaptation triggers: {str(e)}")

    def _log_performance_summary(self):
        """Log performance summary"""
        try:
            logger.info(
                f"Performance Summary - "
                f"Throughput: {self.performance_metrics.throughput:.2f} tasks/s, "
                f"Latency: {self.performance_metrics.latency:.3f}s, "
                f"Queue: {self.performance_metrics.queue_length}, "
                f"Error Rate: {self.performance_metrics.error_rate:.3f}, "
                f"Adaptation Score: {self.performance_metrics.adaptation_score:.3f}"
            )
        except Exception as e:
            logger.error(f"Error logging performance summary: {str(e)}")

    def _can_add_workers(self) -> bool:
        """Check if workers can be added"""
        return len(self.workers) < self.max_workers * 2

    def _can_remove_workers(self) -> bool:
        """Check if workers can be removed"""
        return len(self.workers) > 2

    def _add_worker(self):
        """Add a new worker thread"""
        try:
            worker_id = len(self.workers)
            worker = threading.Thread(
                target=self._worker_loop,
                args=(worker_id,),
                name=f"LIFEWorker-{worker_id}",
                daemon=True,
            )
            worker.start()
            self.workers.append(worker)
            self.worker_stats[worker_id] = {
                "tasks_processed": 0,
                "total_processing_time": 0.0,
                "errors": 0,
                "last_active": datetime.now(),
            }
            logger.info(f"Added worker {worker_id}")
        except Exception as e:
            logger.error(f"Error adding worker: {str(e)}")

    def _remove_worker(self):
        """Remove a worker thread (graceful)"""
        # This is a simplified implementation
        # In practice, you'd need more sophisticated worker management
        logger.info("Worker removal requested (simplified implementation)")

    def get_performance_metrics(self) -> PerformanceMetrics:
        """Get current performance metrics"""
        return self.performance_metrics

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive processor status"""
        return {
            "state": self.current_state.value,
            "workers": {
                "active_count": len(self.workers),
                "max_workers": self.max_workers,
                "worker_stats": self.worker_stats,
            },
            "queues": {
                priority.name: self.task_queues[priority].qsize()
                for priority in PriorityLevel
            },
            "tasks": {
                "processed": self.tasks_processed,
                "completed": len(self.completed_tasks),
                "pending_results": self.result_queue.qsize(),
            },
            "performance": {
                "throughput": self.performance_metrics.throughput,
                "latency": self.performance_metrics.latency,
                "error_rate": self.performance_metrics.error_rate,
                "adaptation_score": self.performance_metrics.adaptation_score,
            },
            "adaptation": {
                "frequency": self.adaptation_frequency,
                "last_adaptation": self.last_adaptation.isoformat(),
                "life_performance": self.life_algorithm.get_performance_metrics(),
            },
        }


class LIFELoadBalancer:
    """Load balancer for L.I.F.E processing"""

    def __init__(self, num_workers: int):
        self.num_workers = num_workers
        self.worker_loads = [0.0] * num_workers
        self.worker_capabilities = [1.0] * num_workers
        self.load_history = deque(maxlen=1000)

    def get_optimal_worker(self, task_complexity: float = 1.0) -> int:
        """Get optimal worker for task assignment"""
        try:
            # Calculate worker scores based on load and capability
            scores = []
            for i in range(self.num_workers):
                # Lower load and higher capability = better score
                load_factor = 1.0 / (1.0 + self.worker_loads[i])
                capability_factor = self.worker_capabilities[i]
                complexity_match = 1.0 / (
                    1.0 + abs(task_complexity - capability_factor)
                )

                score = load_factor * capability_factor * complexity_match
                scores.append(score)

            # Return worker with highest score
            return int(np.argmax(scores))

        except Exception as e:
            logger.error(f"Error in load balancing: {str(e)}")
            return 0  # Fallback to first worker

    def update_worker_load(self, worker_id: int, current_load: float):
        """Update worker load information"""
        if 0 <= worker_id < self.num_workers:
            self.worker_loads[worker_id] = current_load
            self.load_history.append((datetime.now(), worker_id, current_load))

    def adapt_worker_capabilities(self, worker_performance: Dict[int, float]):
        """Adapt worker capabilities based on performance"""
        try:
            for worker_id, performance in worker_performance.items():
                if 0 <= worker_id < self.num_workers:
                    # Exponential moving average for capability adaptation
                    alpha = 0.1
                    self.worker_capabilities[worker_id] = (
                        alpha * performance
                        + (1 - alpha) * self.worker_capabilities[worker_id]
                    )
        except Exception as e:
            logger.error(f"Error adapting worker capabilities: {str(e)}")


def create_life_processor(
    max_workers: int = None, buffer_size: int = 10000
) -> LIFERealTimeProcessor:
    """Factory function to create L.I.F.E real-time processor"""
    return LIFERealTimeProcessor(max_workers, buffer_size)


# Example processing functions
def simple_echo_processor(data: Any, context: Dict[str, Any]) -> Any:
    """Simple echo processor for testing"""
    time.sleep(0.01)  # Simulate processing time
    return f"Processed: {data}"


def mathematical_processor(data: Any, context: Dict[str, Any]) -> Dict[str, Any]:
    """Mathematical processing function"""
    try:
        if isinstance(data, (list, np.ndarray)):
            data_array = np.array(data)
            return {
                "sum": float(np.sum(data_array)),
                "mean": float(np.mean(data_array)),
                "std": float(np.std(data_array)),
                "max": float(np.max(data_array)),
                "min": float(np.min(data_array)),
            }
        elif isinstance(data, (int, float)):
            return {
                "square": data**2,
                "sqrt": np.sqrt(abs(data)),
                "log": np.log(abs(data) + 1),
            }
        else:
            return {"error": "Unsupported data type"}
    except Exception as e:
        return {"error": str(e)}


# Example usage and testing
def test_life_real_time_processor():
    """Test L.I.F.E real-time processor"""
    print("Testing L.I.F.E Real-Time Processor...")

    # Create processor
    processor = create_life_processor(max_workers=4, buffer_size=1000)

    try:
        # Start processor
        processor.start()
        print("Processor started")

        # Submit test tasks
        print("\nSubmitting test tasks...")
        test_data = [
            ([1, 2, 3, 4, 5], PriorityLevel.HIGH),
            ([10, 20, 30], PriorityLevel.NORMAL),
            ([100, 200], PriorityLevel.LOW),
            (42, PriorityLevel.CRITICAL),
            ([1, 1, 2, 3, 5, 8], PriorityLevel.NORMAL),
        ]

        submitted_tasks = []
        for i, (data, priority) in enumerate(test_data):
            task = ProcessingTask(
                task_id=f"test_task_{i}",
                data=data,
                priority=priority,
                processing_function=mathematical_processor,
                context={"test_run": True},
            )

            if processor.submit_task(task):
                submitted_tasks.append(task.task_id)
                print(f"  Submitted task {task.task_id} with priority {priority.name}")

        # Wait for results
        print("\nWaiting for results...")
        time.sleep(2.0)

        # Get results
        results = []
        for task_id in submitted_tasks:
            result = processor.get_result(task_id, timeout=5.0)
            if result:
                results.append(result)
                print(
                    f"  Task {task_id}: Success={result.success}, Time={result.processing_time:.3f}s"
                )
                if result.success:
                    print(f"    Result: {result.result_data}")

        # Test streaming processing
        print("\nTesting streaming processing...")

        def data_generator():
            for i in range(10):
                yield [i, i * 2, i * 3]

        stream_results = processor.process_streaming_data(
            data_generator(), mathematical_processor, chunk_size=1
        )

        print(f"Streaming results: {len(stream_results)} chunks processed")

        # Get performance metrics
        metrics = processor.get_performance_metrics()
        print(f"\nPerformance Metrics:")
        print(f"  Throughput: {metrics.throughput:.2f} tasks/s")
        print(f"  Latency: {metrics.latency:.3f}s")
        print(f"  Queue length: {metrics.queue_length}")
        print(f"  Error rate: {metrics.error_rate:.3f}")
        print(f"  Adaptation score: {metrics.adaptation_score:.3f}")

        # Get status
        status = processor.get_status()
        print(f"\nProcessor Status:")
        print(f"  State: {status['state']}")
        print(f"  Active workers: {status['workers']['active_count']}")
        print(f"  Tasks processed: {status['tasks']['processed']}")
        print(f"  Completed tasks: {status['tasks']['completed']}")

        # Test with high load
        print("\nTesting high load scenario...")
        high_load_tasks = []
        for i in range(50):
            task = ProcessingTask(
                task_id=f"load_test_{i}",
                data=np.random.randn(100),
                processing_function=mathematical_processor,
                priority=PriorityLevel.NORMAL,
            )
            if processor.submit_task(task):
                high_load_tasks.append(task.task_id)

        # Wait for high load processing
        time.sleep(5.0)

        # Check completion rate
        completed_high_load = 0
        for task_id in high_load_tasks:
            if processor.get_result(task_id):
                completed_high_load += 1

        completion_rate = completed_high_load / len(high_load_tasks)
        print(
            f"High load completion rate: {completion_rate:.2f} ({completed_high_load}/{len(high_load_tasks)})"
        )

        # Final metrics
        final_metrics = processor.get_performance_metrics()
        print(f"\nFinal Performance:")
        print(f"  Throughput: {final_metrics.throughput:.2f} tasks/s")
        print(f"  Error rate: {final_metrics.error_rate:.3f}")
        print(f"  Adaptation score: {final_metrics.adaptation_score:.3f}")

    finally:
        # Stop processor
        processor.stop()
        print("\nProcessor stopped")

    return processor, results


if __name__ == "__main__":
    # Run tests
    processor, results = test_life_real_time_processor()
    print("\nL.I.F.E Real-Time Processor testing completed successfully!")
