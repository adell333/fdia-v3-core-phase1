import json
from pathlib import Path

from fdia.engine import run_fdia_analysis


DATASET_DIR = Path("datasets/misleading_v1")
RESULTS_DIR = Path("results")
OUTPUT_FILE = RESULTS_DIR / "fdia_v3_core_raw_results.json"



def load_bin_files(dataset_dir: Path):
    return sorted(dataset_dir.glob("*.bin"))


def expected_label_from_filename(file_path: Path):
    name = file_path.name.upper()

    if name.startswith("M1_"):
        return "Misleading"

    if name.startswith("M2_"):
        return "Partial"

    if name.startswith("M3_"):
        return "Misleading"

    return "Unknown"



def run_entropy_baseline(entropy: float) -> str:
    return "Encrypted" if entropy > 7 else "Usable"


def run_structure_baseline(structure_confidence: float) -> str:
    return "Usable" if structure_confidence > 0.6 else "Encrypted"



def generate_reasoning(signals: dict, details: dict):
    reasoning = []

    entropy = signals.get("entropy", 0) or 0
    variance = signals.get("entropy_variance", 0) or 0
    structure = signals.get("structure_confidence", 0) or 0
    integrity = signals.get("integrity_score", 0) or 0
    contradiction = signals.get("contradiction_index", 0) or 0

    sqlite_validation = details.get("sqlite_validation", {}) or {}
    validated_structure = sqlite_validation.get("validated_structure_score", 0) or 0
    page_integrity = sqlite_validation.get("page_integrity_score", 0) or 0

    structure_reasons = details.get("structure", []) or []
    integrity_reasons = details.get("integrity", []) or []
    contradiction_reasons = details.get("contradictions", []) or []
    sqlite_reasons = sqlite_validation.get("reasons", []) or []

    
    if entropy > 7.5:
        reasoning.append("High entropy indicates random or encrypted-like data")

    if entropy < 1.0:
        reasoning.append("Low entropy indicates uniform or artificial structured data")

    if variance > 5:
        reasoning.append("High entropy variance indicates mixed structured and random content")

    if structure > 0.2 and validated_structure < 0.4:
        reasoning.append("Detected structure is not validated by SQLite validation")

    if integrity < 0.7:
        reasoning.append("Integrity score indicates incomplete or truncated data")

    if contradiction >= 0.5:
        reasoning.append("Contradiction index indicates conflicting forensic signals")

    if page_integrity == 0:
        reasoning.append("No valid SQLite page structure detected")

    
    for item in structure_reasons:
        reasoning.append(f"Structure signal: {item}")

    for item in integrity_reasons:
        reasoning.append(f"Integrity signal: {item}")

    for item in sqlite_reasons:
        reasoning.append(f"SQLite validation: {item}")

    for item in contradiction_reasons:
        reasoning.append(f"Contradiction: {item}")

    # Never allow empty reasoning
    if not reasoning:
        reasoning.append("Classification based on combined weak forensic signals")

    return reasoning



def normalise_sqlite_validation(details: dict):
    sqlite_validation = details.get("sqlite_validation", {}) or {}

    return {
        "validated_structure_score": sqlite_validation.get("validated_structure_score", 0),
        "page_integrity_score": sqlite_validation.get("page_integrity_score", 0),
        "schema_consistency": sqlite_validation.get("schema_consistency", 0),
        "artifact_confidence": sqlite_validation.get("artifact_confidence", 0),
        "reasons": sqlite_validation.get("reasons", [])
    }



def process_file(file_path: Path):
    fdia_output = run_fdia_analysis(file_path)

    signals = fdia_output.get("signals", {}) or {}
    details = fdia_output.get("details", {}) or {}

    entropy = signals.get("entropy", 0) or 0
    structure_confidence = signals.get("structure_confidence", 0) or 0

    return {
        "file": str(file_path),
        "expected_label": expected_label_from_filename(file_path),

        "fdia": {
            "classification": fdia_output.get("classification"),
            "confidence": fdia_output.get("confidence")
        },

        "signals": {
            "entropy": signals.get("entropy"),
            "entropy_variance": signals.get("entropy_variance"),
            "structure_confidence": signals.get("structure_confidence"),
            "integrity_score": signals.get("integrity_score"),
            "contradiction_index": signals.get("contradiction_index")
        },

        "details": {
            "structure": details.get("structure", []),
            "integrity": details.get("integrity", []),
            "sqlite_validation": normalise_sqlite_validation(details),
            "contradictions": details.get("contradictions", [])
        },

        "reasoning": generate_reasoning(signals, details),

        "baselines": {
            "entropy": run_entropy_baseline(entropy),
            "structure": run_structure_baseline(structure_confidence)
        }
    }



def save_results(results: list):
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)



def main():
    if not DATASET_DIR.exists():
        raise FileNotFoundError(f"Dataset folder not found: {DATASET_DIR}")

    bin_files = load_bin_files(DATASET_DIR)

    if not bin_files:
        raise FileNotFoundError(f"No .bin files found in {DATASET_DIR}")

    results = [process_file(file_path) for file_path in bin_files]

    save_results(results)

    print("FDIA v3 Core execution complete.")
    print(f"Files processed: {len(results)}")
    print(f"Results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()