class IntegrityAnalyzer:
    def __init__(self, block_size=4096):
        self.block_size = block_size

    def zero_ratio(self, data: bytes):
        if not data:
            return 0.0
        return data.count(0) / len(data)

    def block_analysis(self, data: bytes):
        blocks = []
        for i in range(0, len(data), self.block_size):
            chunk = data[i:i + self.block_size]
            if chunk:
                blocks.append(chunk.count(0) / len(chunk))
        return blocks

    def compute(self, data: bytes):
        reasons = []

        if not data:
            return 0.0, ["Empty data"]

        zr = self.zero_ratio(data)
        block_zr = self.block_analysis(data)
        data_len = len(data)
        unique_bytes = len(set(data))

        
        
        if zr > 0.5:
            reasons.append("High zero ratio → missing data")
        elif zr > 0.2:
            reasons.append("Moderate zero ratio → partial corruption")

        
        if block_zr:
            high_zero_blocks = sum(1 for x in block_zr if x > 0.6)
            if high_zero_blocks > len(block_zr) * 0.3:
                reasons.append("Fragmentation detected")

        
        if len(block_zr) > 1:
            mean = sum(block_zr) / len(block_zr)
            variance = sum((x - mean) ** 2 for x in block_zr) / len(block_zr)

            if variance < 0.0001:
                reasons.append("Possible truncation (low variation)")
            elif variance > 0.05:
                reasons.append("Inconsistent data blocks")

       
        if data_len < 512:
            reasons.append("Incomplete extraction")

        if unique_bytes < 10:
            reasons.append("Low byte diversity → synthetic or truncated")

        
        
        score = 1.0

        if zr > 0.5:
            score -= 0.6
        elif zr > 0.2:
            score -= 0.3

        if any("fragmentation" in r.lower() for r in reasons):
            score -= 0.3

        if any("truncation" in r.lower() for r in reasons):
            score -= 0.4

        if any("incomplete" in r.lower() for r in reasons):
            score -= 0.4

        if any("low byte diversity" in r.lower() for r in reasons):
            score -= 0.3

        score = max(0.0, min(1.0, score))

        return score, reasons