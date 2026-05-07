class SQLiteArtifactParser:
    def __init__(self):
        pass

    def parse(self, data: bytes):
        """
        Returns:
            (score, reasons)
        """

        reasons = []
        score = 0.0

        if not data or len(data) < 100:
            return 0.0, ["Data too small for artifact parsing"]

        
        keywords = [b"table", b"index", b"sqlite_master", b"CREATE", b"INSERT"]
        hits = 0

        for kw in keywords:
            if kw in data:
                hits += 1

        if hits >= 3:
            score += 0.5
            reasons.append(f"Multiple SQLite keywords detected ({hits})")
        elif hits > 0:
            score += 0.2
            reasons.append(f"Partial SQLite keywords detected ({hits})")

        
        if b"(" in data and b")" in data:
            score += 0.2
            reasons.append("Possible table schema structure")

        
        ascii_ratio = sum(1 for b in data if 32 <= b <= 126) / len(data)

        if ascii_ratio > 0.8:
            score += 0.2
            reasons.append("High readable content (likely structured text)")

        
        score = min(score, 1.0)

        return score, reasons