import math


class EntropyAnalyzer:
    def __init__(self, block_size=4096):
        self.block_size = block_size

    def shannon_entropy(self, data: bytes):
        if not data:
            return 0.0

        freq = [0] * 256

        for b in data:
            freq[b] += 1

        entropy = 0.0
        length = len(data)

        for count in freq:
            if count == 0:
                continue
            p = count / length
            entropy -= p * math.log2(p)

        return entropy

    def compute(self, data: bytes):
        """
        Returns:
            entropy (float)
            entropy_variance (float)
        """

        if not data:
            return 0.0, 0.0

        
        overall_entropy = self.shannon_entropy(data)

        
        block_size = self.block_size

        if len(data) < block_size:
            block_size = max(64, len(data) // 4)

        
        block_entropies = []

        for i in range(0, len(data), block_size):
            chunk = data[i:i + block_size]

            if len(chunk) < 16:
                continue

            block_entropies.append(self.shannon_entropy(chunk))

        
        if len(block_entropies) <= 1:
            variance = 0.0
        else:
            mean = sum(block_entropies) / len(block_entropies)
            variance = sum((x - mean) ** 2 for x in block_entropies) / len(block_entropies)

        return overall_entropy, variance