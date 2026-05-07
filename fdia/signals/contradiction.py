class ContradictionEngine:
    def compute(self, signals, details):
        conflicts = []
        score = 0.0

        entropy = signals.get("entropy", 0)
        variance = signals.get("entropy_variance", 0)
        structure = signals.get("structure_confidence", 0)
        integrity = signals.get("integrity_score", 0)

        structure_reasons = details.get("structure", [])
        integrity_reasons = details.get("integrity", [])

        reasons_text = " ".join(structure_reasons + integrity_reasons).lower()


        if entropy > 7.0 and structure > 0.05:
            conflicts.append("High entropy contradicts structure")
            score += 0.25

        
        if variance > 0.5:
            conflicts.append("High entropy variance (mixed data)")
            score += 0.30

        
        if any(x in reasons_text for x in ["invalid", "malformed", "failed"]):
            conflicts.append("Invalid structure signature")
            score += 0.25

        
        if structure > 0.2 and integrity < 0.5:
            conflicts.append("Structure but low integrity")
            score += 0.20

        
        if structure > 0.6 and any(x in reasons_text for x in ["truncation", "low variation", "too small"]):
            conflicts.append("Structured but incomplete")
            score += 0.35

        score = min(score, 1.0)

        return round(score, 3), conflicts