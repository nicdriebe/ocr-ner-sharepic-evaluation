import os
import time
import psutil
from functools import wraps
from codecarbon import EmissionsTracker

def monitor(full_name="Unnamed Task"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            proc = psutil.Process(os.getpid())
            tracker = EmissionsTracker(project_name=full_name)
            tracker.start()

            start_cpu = proc.cpu_times()
            start_mem = proc.memory_info().rss / (1024 ** 2)
            start_time = time.time()

            result = func(*args, **kwargs)

            end_time = time.time()
            end_cpu = proc.cpu_times()
            end_mem = proc.memory_info().rss / (1024 ** 2)
            emissions = tracker.stop()

            print(f"\n--- Ressourcenbericht für '{full_name}' ---")
            print(f"CPU-Zeit:     {(end_cpu.user - start_cpu.user):.2f} s")
            print(f"RAM genutzt:  {(end_mem - start_mem):.2f} MB")
            print(f"Laufzeit:     {(end_time - start_time):.2f} s")
            print(f"CO₂-Ausstoß:  {emissions:.6f} kg")
            print(f"-------------------------------------------\n")

            return result
        return wrapper
    return decorator
