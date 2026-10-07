import os
import random
import pandas as pd


OUTPUT_PATH = "data/electrical_data.csv"

random.seed(42)


def generate_normal():
    return {
        "voltage": round(random.uniform(225, 240), 2),
        "current": round(random.uniform(3.5, 6.0), 2),
        "frequency": round(random.uniform(49.8, 50.2), 2),
        "power_factor": round(random.uniform(0.93, 0.99), 2),
        "temperature": round(random.uniform(28, 38), 2),
        "fault": "Normal",
    }


def generate_overload():
    return {
        "voltage": round(random.uniform(215, 230), 2),
        "current": round(random.uniform(7.0, 12.0), 2),
        "frequency": round(random.uniform(49.5, 50.2), 2),
        "power_factor": round(random.uniform(0.70, 0.86), 2),
        "temperature": round(random.uniform(40, 60), 2),
        "fault": "Overload",
    }


def generate_overvoltage():
    return {
        "voltage": round(random.uniform(245, 270), 2),
        "current": round(random.uniform(3.0, 6.0), 2),
        "frequency": round(random.uniform(49.8, 50.3), 2),
        "power_factor": round(random.uniform(0.85, 0.94), 2),
        "temperature": round(random.uniform(32, 45), 2),
        "fault": "Overvoltage",
    }


def generate_undervoltage():
    return {
        "voltage": round(random.uniform(185, 215), 2),
        "current": round(random.uniform(3.5, 6.5), 2),
        "frequency": round(random.uniform(49.5, 50.2), 2),
        "power_factor": round(random.uniform(0.85, 0.95), 2),
        "temperature": round(random.uniform(32, 45), 2),
        "fault": "Undervoltage",
    }


def generate_phase_imbalance():
    return {
        "voltage": round(random.uniform(220, 240), 2),
        "current": round(random.uniform(7.0, 11.0), 2),
        "frequency": round(random.uniform(49.0, 51.0), 2),
        "power_factor": round(random.uniform(0.70, 0.84), 2),
        "temperature": round(random.uniform(40, 55), 2),
        "fault": "Phase_Imbalance",
    }


def generate_dataset():
    rows = []

    generators = [
        generate_normal,
        generate_overload,
        generate_overvoltage,
        generate_undervoltage,
        generate_phase_imbalance,
    ]

    for generator in generators:
        for _ in range(200):
            rows.append(generator())

    random.shuffle(rows)

    data = pd.DataFrame(rows)

    data.insert(0, "id", range(1, len(data) + 1))

    os.makedirs("data", exist_ok=True)
    data.to_csv(OUTPUT_PATH, index=False)

    print(f"Dataset created successfully: {len(data)} rows")
    print("\nClass distribution:")
    print(data["fault"].value_counts())


if __name__ == "__main__":
    generate_dataset()