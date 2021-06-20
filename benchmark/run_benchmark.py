import benchmark_cases
import importlib
import os
import time
from watchpoints import watch
from progshot import _pshot


class Benchmark:
    def run(self):
        for file in os.listdir(benchmark_cases.__spec__.submodule_search_locations[0]):
            if file.startswith("case") and file.endswith(".py"):
                self.run_case(file[:-3])

    def run_case(self, module_name):
        m = importlib.import_module(f"benchmark_cases.{module_name}")
        if hasattr(m, "do_init"):
            m.do_init()
        baseline_time = self.timeit(m.do_baseline)
        experiment_time = self.timeit(m.do_experiment)
        films = m.do_dump()
        pshot_size = os.stat("out.pshot").st_size
        os.remove("out.pshot")
        print(f"=============== {module_name} ===============")
        print(f"= Baseline   - {baseline_time}")
        print(f"= Experiment - {experiment_time}")
        print(f"= Overhead   - {experiment_time / baseline_time}")
        print(f"= Pshot Size - {pshot_size}")
        print(f"= Films      - {films}")
        print(f"= Byte/Film  - {pshot_size / films}")

    def timeit(self, func):
        start = time.time()
        func()
        return time.time() - start


if __name__ == "__main__":
    bm = Benchmark()
    bm.run()