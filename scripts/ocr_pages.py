#!/usr/bin/env python3
"""
ocr_pages.py
============
OCR text extraction from PDF page images.
Requires: tesseract + pytesseract + Japanese language pack

Install requirements:
    pip install pytesseract pillow
    apt install tesseract-ocr tesseract-ocr-jpn

Usage:
    python3 scripts/ocr_pages.py [--lang jpn] [--pages-dir assets/pages] [--out-dir assets/ocr]

If tesseract is not installed, this script will:
  - Document the limitation in BUILD_NOTES.md
  - Exit gracefully without error
"""

import argparse
import os
import sys
import glob

def check_tesseract():
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        return True, pytesseract
    except Exception as e:
        return False, str(e)

def run_ocr(pages_dir, out_dir, lang="jpn"):
    available, pytesseract = check_tesseract()
    if not available:
        msg = f"[SKIP] Tesseract not available: {pytesseract}"
        print(msg)
        # Document in BUILD_NOTES
        try:
            with open("BUILD_NOTES.md", "a", encoding="utf-8") as f:
                f.write(f"\n\n---\n## OCR Status\n\n"
                        f"**Status: SKIPPED**\n\n"
                        f"Reason: {pytesseract}\n\n"
                        f"To enable OCR:\n"
                        f"```bash\n"
                        f"pip install pytesseract pillow\n"
                        f"apt install tesseract-ocr tesseract-ocr-jpn\n"
                        f"python3 scripts/ocr_pages.py --lang jpn\n"
                        f"```\n")
        except Exception:
            pass
        return

    from PIL import Image
    os.makedirs(out_dir, exist_ok=True)
    pages = sorted(glob.glob(os.path.join(pages_dir, "p*.png")))
    print(f"[INFO] OCR: {len(pages)} pages, lang={lang}")
    for i, page_path in enumerate(pages, 1):
        base = os.path.splitext(os.path.basename(page_path))[0]
        out_path = os.path.join(out_dir, f"{base}.txt")
        if os.path.exists(out_path):
            continue
        img = Image.open(page_path)
        text = pytesseract.image_to_string(img, lang=lang)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        if i % 50 == 0 or i == len(pages):
            print(f"  [{i}/{len(pages)}] OCR done")
    print(f"[DONE] OCR text saved to {out_dir}/")

def main():
    parser = argparse.ArgumentParser(description="OCR page images to text")
    parser.add_argument("--lang", default="jpn", help="Tesseract language (default: jpn)")
    parser.add_argument("--pages-dir", default="assets/pages")
    parser.add_argument("--out-dir", default="assets/ocr")
    args = parser.parse_args()
    run_ocr(args.pages_dir, args.out_dir, args.lang)

if __name__ == "__main__":
    main()
