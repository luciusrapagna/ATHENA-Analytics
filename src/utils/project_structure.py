from pathlib import Path
from datetime import datetime


def create_project_structure(base_name="athena_project"):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    root = Path(
        f"outputs/{base_name}_{timestamp}"
    )

    folders = [
        "01_raw_data",
        "02_processed_data",
        "03_tables",
        "04_figures",
        "05_reports",
        "06_logs"
    ]

    for folder in folders:
        (root / folder).mkdir(
            parents=True,
            exist_ok=True
        )

    return root