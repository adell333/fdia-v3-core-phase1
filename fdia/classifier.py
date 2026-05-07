class FDIAClassifier:
    def classify(self, s):
        H = s["entropy"]
        H_var = s["entropy_variance"]
        S = s["structure_confidence"]
        I = s["integrity_score"]
        C = s["contradiction_index"]

        reasons = []

       
        if C >= 0.5:
            reasons.append("High contradiction between signals")
            return self._out("misleading", 0.85, reasons)

        
        if H > 7.2 and S < 0.2 and C < 0.3:
            reasons.append("High entropy with no reliable structure")
            return self._out("encrypted", 0.8, reasons)

        
        if I < 0.5 and (S >= 0.2 or H_var > 5):
            reasons.append("Low integrity with fragmentation indicators")
            return self._out("partial", 0.7, reasons)

        
        if S >= 0.6 and I >= 0.6 and H < 6.5:
            reasons.append("Valid structure and integrity")
            return self._out("usable", 0.85, reasons)

        reasons.append("Weak or ambiguous signals")
        return self._out("undetermined", 0.5, reasons)

    def _out(self, label, confidence, reasons):
        return {
            "classification": label,
            "confidence": confidence,
            "reasons": reasons
        }