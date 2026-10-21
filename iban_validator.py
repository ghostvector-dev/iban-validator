#!/usr/bin/env python3
"""
iban_validator.py — ISO 13616 / MOD-97 IBAN Validator
Author: Ghost Vector (@ghostvector-dev)
Description: Standalone utility used in DofBank migration pipelines.
"""

import sys
import re

COUNTRY_LENGTHS = {
    "AL": 28, "AD": 24, "AT": 20, "AZ": 28, "BH": 22, "BE": 16,
    "BA": 20, "BR": 29, "BG": 22, "CR": 22, "HR": 21, "CY": 28,
    "CZ": 24, "DK": 18, "DO": 28, "EG": 29, "EE": 20, "FI": 18,
    "FR": 27, "DE": 22, "GB": 22, "GE": 22, "GI": 23, "GR": 27,
    "HU": 28, "IS": 26, "IE": 22, "IL": 23, "IT": 27, "JO": 30,
    "KW": 30, "LV": 21, "LB": 28, "LI": 21, "LT": 20, "LU": 20,
    "MT": 31, "NL": 18, "NO": 15, "PL": 28, "PT": 25, "QA": 29,
    "RO": 24, "SA": 24, "RS": 22, "SK": 24, "SI": 19, "ES": 24,
    "SE": 24, "CH": 21, "TN": 24, "TR": 26, "AE": 23, "UA": 29,
}


def validate_dof_iban(iban: str) -> tuple[bool, str]:
    """Validates both internal DofBank format (DOF-XXXX) and international IBAN."""
    cleaned = iban.strip().upper().replace(" ", "")

    # Check DofBank internal format
    if re.match(r"^DOF-\d{4}$", cleaned):
        return True, "Valid DofBank Internal Account Identifier"

    # International IBAN Check
    if len(cleaned) < 5 or not cleaned[:2].isalpha():
        return False, "Invalid IBAN length or missing country prefix"

    country = cleaned[:2]
    expected_len = COUNTRY_LENGTHS.get(country)
    if expected_len and len(cleaned) != expected_len:
        return False, f"Length mismatch for {country}: expected {expected_len}, got {len(cleaned)}"

    rearranged = cleaned[4:] + cleaned[:4]
    numeric_str = "".join(str(ord(c) - 55) if c.isalpha() else c for c in rearranged)

    if int(numeric_str) % 97 != 1:
        return False, "MOD-97 checksum failed"

    return True, "Valid International IBAN"


if __name__ == "__main__":
    test_iban = sys.argv[1] if len(sys.argv) > 1 else "DOF-0001"
    is_valid, reason = validate_dof_iban(test_iban)
    print(f"[{'PASS' if is_valid else 'FAIL'}] {test_iban} -> {reason}")
