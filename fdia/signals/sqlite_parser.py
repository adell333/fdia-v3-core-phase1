class SQLiteParser:
    def parse_header(self, data: bytes):
        if len(data) < 100:
            return False, "Data too small for SQLite header"

        if not data.startswith(b"SQLite format 3\x00"):
            return False, "Invalid SQLite header"

        page_size = int.from_bytes(data[16:18], "big")

        if page_size not in [512, 1024, 2048, 4096, 8192, 16384, 32768]:
            return False, f"Invalid page size: {page_size}"

        return True, f"Valid SQLite header (page size: {page_size})"

    def check_page_alignment(self, data: bytes, page_size):
        if len(data) % page_size != 0:
            return False, "File size not aligned to page size"

        return True, "Page alignment valid"

    def validate(self, data: bytes):
        reasons = []
        score = 0.0

        
        if data.startswith(b"SQLite format 3"):
            score += 0.2
            reasons.append("SQLite signature present")

        header_valid, header_msg = self.parse_header(data)
        reasons.append(header_msg)

        if not header_valid:
            
            return min(score, 0.3), reasons

        score += 0.4

        page_size = int.from_bytes(data[16:18], "big")

        aligned, align_msg = self.check_page_alignment(data, page_size)
        reasons.append(align_msg)

        if aligned:
            score += 0.3

        if len(data) > page_size:
            score += 0.2
            reasons.append("Multiple pages detected")

        return min(score, 1.0), reasons