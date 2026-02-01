import re
import json
from pathlib import Path

PATTERNS = {
    # This regex is used to find email addresses
    'emails': (r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b", 0),
    # This regex is used to find URLs
    'urls': (r"https?://[^\s]+", re.IGNORECASE),
    # This finds phone numbers
    'phones': (r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", 0),
    # This finds credit card numbers (simple pattern)
    'credit_cards': (r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", 0),
    # This regex finds exact times 
    'times': (r"\b\d{1,2}:\d{2}(?:\s?[AP]M)?\b", re.IGNORECASE),
    # This regex finds currency amounts 
    'currency': (r"\$\d{1,3}(?:,\d{3})*(?:\.\d{2})?", 0),
}


class DataExtractor:
    def __init__(self):
        self.patterns = {k: re.compile(p, flags) for k, (p, flags) in PATTERNS.items()}

    def validate_input(self, text: str):
        if len(text) > 1_000_000:
            return False, ["Input exceeds maximum length"]
        if "\x00" in text:
            return False, ["Null byte detected"]
        warnings = []
        if re.search(r"<script", text, re.IGNORECASE):
            warnings.append("Script tag detected")
        if "../" in text or "..\\" in text:
            warnings.append("Path traversal pattern detected")
        return True, warnings

    @staticmethod
    def mask_credit_card(card: str) -> str:
        digits = re.sub(r"[-\s]", "", card)
        return "**** **** **** " + digits[-4:]

    def extract(self, text: str) -> dict:
        is_valid, warnings = self.validate_input(text)
        base = {k: [] for k in PATTERNS.keys()}
        base['security_warnings'] = warnings
        if not is_valid:
            return base

        for name, pattern in self.patterns.items():
            matches = pattern.findall(text)
            seen = {}
            for m in matches:
                seen.setdefault(m, True)
            base[name] = list(seen.keys())

        base['credit_cards'] = [self.mask_credit_card(c) for c in base.get('credit_cards', [])]
        return base


def print_summary(results: dict) -> None:
    # print("=" * 60)
    print("DATA EXTRACTION RESULTS")
    # print("=" * 60)

    for key in ['emails', 'urls', 'phones', 'credit_cards', 'times', 'currency']:
        items = results.get(key, [])
        print(f"\n{key.capitalize()} found: {len(items)}")
        for it in items:
            print(f"  - {it}")

    if results.get('security_warnings'):
        print("\nSecurity Warnings:")
        for w in results['security_warnings']:
            print(f"  ! {w}")
    else:
        print("\nNo security issues detected.")

    # print("\n" + "=" * 60)


def main() -> None:
    p = Path('input.txt')
    text = p.read_text(encoding='utf-8') if p.exists() else ''
    extractor = DataExtractor()
    results = extractor.extract(text)
    print_summary(results)
    Path('output.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    print("Results saved to output.json")


if __name__ == '__main__':
    main()