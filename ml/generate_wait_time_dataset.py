import random
import pandas as pd


random.seed(42)

rows = []

for _ in range(1000):
    patients_ahead = random.randint(0, 20)
    queue_length = random.randint(1, 30)
    active_doctors = random.randint(1, 5)
    avg_consultation_time = random.uniform(8, 25)
    emergency_load = random.randint(0, 10)
    is_walk_in = random.randint(0, 1)
    hour = random.randint(8, 18)

    waiting_time = (
        patients_ahead * avg_consultation_time
        + queue_length * 0.5
        - active_doctors * 5
        + emergency_load * 2
        + is_walk_in * 3
        + random.uniform(-5, 5)
    )

    waiting_time = max(0, waiting_time)

    rows.append({
        "patients_ahead": patients_ahead,
        "queue_length": queue_length,
        "active_doctors": active_doctors,
        "avg_consultation_time": round(avg_consultation_time, 2),
        "emergency_load": emergency_load,
        "is_walk_in": is_walk_in,
        "hour": hour,
        "waiting_time": round(waiting_time, 2),
    })


df = pd.DataFrame(rows)

df.to_csv(
    "ml/wait_time_dataset.csv",
    index=False
)

print(f"Dataset created: {len(df)} rows")
print(df.head())