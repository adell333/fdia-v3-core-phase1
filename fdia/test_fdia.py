import os
from fdia.engine import FDIAEngine

engine = FDIAEngine()

def run_test(name, data):
    print(f"\n=== TEST: {name} ===")
    result = engine.analyze(data)

    for k, v in result.items():
        print(f"{k}: {v}")


random_data = os.urandom(100000)
structured_data = b"Hello World\n" * 10000
corrupted_data = b"\x00" * 50000 + os.urandom(50000)
fake_sqlite = b"SQLite format 3\x00" + os.urandom(99984)

if __name__ == "__main__":
    run_test("Random Data", random_data)
    run_test("Structured Data", structured_data)
    run_test("Corrupted Data", corrupted_data)
    run_test("Fake Structured", fake_sqlite)