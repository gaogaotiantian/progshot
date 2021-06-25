import benchmark_cases
import importlib
import os
import sys
import time


class Benchmark:
    def run(self):
        args = sys.argv
        if len(sys.argv) > 1:
            cases = sys.argv[1:]
        else:
            cases = ["case"]
        for file in os.listdir(benchmark_cases.__spec__.submodule_search_locations[0]):
            if file.startswith("case") and file.endswith(".py"):
                case_name = file[:-3]
                for pattern in cases:
                    if pattern in case_name:
                        self.run_case(case_name)

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
        start = time.perf_counter()
        func()
        return time.perf_counter() - start


if __name__ == "__main__":
    bm = Benchmark()
    bm.run()