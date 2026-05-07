from fdia.signals.sqlite_parser import SQLiteParser


class StructureAnalyzer:
    def __init__(self):
        self.sqlite = SQLiteParser()

    def ascii_ratio(self, data: bytes):
        if not data:
            return 0.0
        printable = sum(1 for b in data if 32 <= b <= 126)
        return printable / len(data)

    def structure_confidence(self, data: bytes):
        score = 0.0
        reasons = []

        data_len = len(data)
        unique_bytes = len(set(data))

        
        sqlite_score, sqlite_reasons = self.sqlite.validate(data)

        if sqlite_score > 0:
            score += sqlite_score * 0.5
        reasons.extend(sqlite_reasons)

        
        if sqlite_score > 0 and len(sqlite_reasons) <= 1:
            score *= 0.6
            reasons.append("Header detected without internal structure")

        
        try:
            from fdia.signals.sqlite_artifact_parser import SQLiteArtifactParser

            parser = SQLiteArtifactParser()
            artifact_score, artifact_reasons = parser.parse(data)

            if artifact_score > 0:
                score += artifact_score * 0.5

            reasons.extend(artifact_reasons)

        except Exception as e:
            reasons.append(f"Artifact parser skipped: {str(e)}")

        
        ascii_ratio = self.ascii_ratio(data)

        if ascii_ratio > 0.9:
            score += 0.7
            reasons.append(f"Strong ASCII structure ({ascii_ratio:.2f})")
        elif ascii_ratio > 0.75:
            score += 0.5
            reasons.append(f"Moderate ASCII structure ({ascii_ratio:.2f})")
        elif ascii_ratio > 0.6:
            score += 0.3
            reasons.append(f"Weak ASCII presence ({ascii_ratio:.2f})")

        
        if data_len < 1024:
            score *= 0.5
            reasons.append("Data too small → incomplete structure")

        if unique_bytes < 20:
            score *= 0.6
            reasons.append("Low byte diversity → artificial structure")

        score = min(score, 1.0)

        return score, reasons