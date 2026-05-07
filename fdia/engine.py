from fdia.signals.entropy import EntropyAnalyzer
from fdia.signals.structure import StructureAnalyzer
from fdia.signals.integrity import IntegrityAnalyzer
from fdia.signals.contradiction import ContradictionEngine
from fdia.signals.sqlite_validator import SQLiteValidator


class FDIAEngine:
    def __init__(self):
        self.entropy = EntropyAnalyzer()
        self.structure = StructureAnalyzer()
        self.integrity = IntegrityAnalyzer()
        self.contradiction = ContradictionEngine()
        self.sqlite_validator = SQLiteValidator()

    def analyze(self, data: bytes):
        
        entropy, variance = self.entropy.compute(data)
        structure_conf, structure_reasons = self.structure.structure_confidence(data)
        integrity_score, integrity_reasons = self.integrity.compute(data)
        sqlite_validation = self.sqlite_validator.validate(data)

        signals = {
            "entropy": entropy,
            "entropy_variance": variance,
            "structure_confidence": structure_conf,
            "integrity_score": integrity_score,
        }

        details = {
            "structure": structure_reasons,
            "integrity": integrity_reasons,
            "sqlite_validation": sqlite_validation,
        }

        
        contradiction_index, conflicts = self.contradiction.compute(signals, details)

        signals["contradiction_index"] = contradiction_index
        details["contradictions"] = conflicts

        
        decision = self.classify(signals, details)

        return {
            "signals": signals,
            "details": details,
            "decision": decision,
        }

    def classify(self, signals, details):
        entropy = signals["entropy"]
        structure = signals["structure_confidence"]
        integrity = signals["integrity_score"]
        contradiction = signals["contradiction_index"]

        
        validation = details.get("sqlite_validation", {})
        validated_structure = validation.get("validated_structure_score", 0)
        page_integrity = validation.get("page_integrity_score", 0)

        
        if contradiction >= 0.5:
            return {
                "classification": "Misleading",
                "confidence": 0.85,
                "reasons": ["High contradiction between signals"]
            }

        
        if structure > 0.5 and validated_structure < 0.4:
            return {
                "classification": "Misleading",
                "confidence": 0.85,
                "reasons": ["Detected structure failed validation (fake structure)"]
            }

       
        if page_integrity < 0.5:
            return {
                "classification": "Partial",
                "confidence": 0.75,
                "reasons": ["Invalid or incomplete page structure"]
            }

        
        if entropy > 7.2 and validated_structure < 0.2:
            return {
                "classification": "Encrypted",
                "confidence": 0.8,
                "reasons": ["High entropy, no valid structure"]
            }

        
        if (
            validated_structure > 0.7
            and page_integrity > 0.7
            and integrity > 0.8
            and entropy > 1.0
            and contradiction < 0.3
        ):
            return {
                "classification": "Usable",
                "confidence": 0.9,
                "reasons": ["Validated structure and consistent data"]
            }

       
        return {
            "classification": "Undetermined",
            "confidence": 0.5,
            "reasons": ["Ambiguous signal interaction"]
        }



def run_fdia_analysis(file_path):
    with open(file_path, "rb") as f:
        data = f.read()

    engine = FDIAEngine()
    result = engine.analyze(data)

    decision = result["decision"]

    return {
        "classification": decision["classification"],
        "confidence": decision["confidence"],
        "signals": result["signals"],
        "details": result["details"]
    }