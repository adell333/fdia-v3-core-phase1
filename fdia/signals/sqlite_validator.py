import struct


class SQLiteValidator:
    def validate(self, data: bytes):
        reasons = []

        
        validated_structure_score = 0.0
        page_integrity_score = 0.0
        schema_consistency = 0.0
        artifact_confidence = 0.0

        
        if len(data) < 100:
            reasons.append("File too small for SQLite header")
            return self._output(
                validated_structure_score,
                page_integrity_score,
                schema_consistency,
                artifact_confidence,
                reasons
            )

        
        if data[:16] != b"SQLite format 3\x00":
            reasons.append("Invalid SQLite header")
            return self._output(
                validated_structure_score,
                page_integrity_score,
                schema_consistency,
                artifact_confidence,
                reasons
            )

        validated_structure_score += 0.2
        reasons.append("Valid SQLite header detected")

        
        try:
            page_size = struct.unpack(">H", data[16:18])[0]

           
            if page_size == 1:
                page_size = 65536

            valid_sizes = {512, 1024, 2048, 4096, 8192, 16384, 32768, 65536}

            if page_size not in valid_sizes:
                reasons.append(f"Invalid page size: {page_size}")
                return self._output(
                    validated_structure_score,
                    page_integrity_score,
                    schema_consistency,
                    artifact_confidence,
                    reasons
                )

            validated_structure_score += 0.2
            reasons.append(f"Valid page size: {page_size}")

        except Exception:
            reasons.append("Failed to read page size")
            return self._output(
                validated_structure_score,
                page_integrity_score,
                schema_consistency,
                artifact_confidence,
                reasons
            )

        
        if len(data) % page_size != 0:
            reasons.append("File size not aligned with page size (possible truncation)")
            page_integrity_score = 0.3
        else:
            validated_structure_score += 0.2
            page_integrity_score = 0.6
            reasons.append("File aligned with page size")

        
        valid_pages = 0
        total_pages = len(data) // page_size

        for i in range(total_pages):
            offset = i * page_size
            page = data[offset:offset + page_size]

            if len(page) < 1:
                continue

            page_type = page[0]

            if page_type in (0x02, 0x05, 0x0A, 0x0D):
                valid_pages += 1

        if total_pages > 0:
            ratio = valid_pages / total_pages

            if ratio > 0.7:
                validated_structure_score += 0.2
                page_integrity_score += 0.2
                reasons.append("Majority of pages have valid SQLite types")
            elif ratio > 0.3:
                page_integrity_score += 0.1
                reasons.append("Some valid SQLite pages detected")
            else:
                reasons.append("Page structure mostly invalid")

        
        if b"CREATE TABLE" in data:
            schema_consistency = 0.7
            validated_structure_score += 0.2
            reasons.append("Schema definition detected")
        else:
            reasons.append("No schema definition found")

        
        ascii_count = sum(1 for b in data if 32 <= b <= 126)
        ascii_ratio = ascii_count / len(data)

        if ascii_ratio > 0.3:
            artifact_confidence = 0.6
            reasons.append("Readable content detected")
        else:
            artifact_confidence = 0.2
            reasons.append("Low readable content")

        
        validated_structure_score = min(validated_structure_score, 1.0)
        page_integrity_score = min(page_integrity_score, 1.0)

        return self._output(
            validated_structure_score,
            page_integrity_score,
            schema_consistency,
            artifact_confidence,
            reasons
        )

   
    def _output(self, vs, pi, sc, ac, reasons):
        return {
            "validated_structure_score": round(vs, 3),
            "page_integrity_score": round(pi, 3),
            "schema_consistency": round(sc, 3),
            "artifact_confidence": round(ac, 3),
            "reasons": reasons
        }