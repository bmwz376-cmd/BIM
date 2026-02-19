#!/usr/bin/env python3
"""
build_from_pdf.py
=================
PDF → PNG page images + assets_index.md generator
Usage:
    python3 scripts/build_from_pdf.py [--pdf path/to/file.pdf]
"""

import argparse
import os
import sys
import glob

def find_pdf(cli_path=None):
    if cli_path:
        if os.path.exists(cli_path):
            return cli_path
        else:
            print(f"[ERROR] Specified PDF not found: {cli_path}")
            sys.exit(1)
    # Default locations
    for candidate in ["./input.pdf", "./input/input.pdf"]:
        if os.path.exists(candidate):
            return candidate
    # Search repo root
    found = glob.glob("*.pdf")
    if found:
        return found[0]
    print("[ERROR] No PDF found. Please specify --pdf path/to/file.pdf")
    sys.exit(1)

def convert_pdf_to_png(pdf_path, output_dir, zoom=2.0):
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("[ERROR] PyMuPDF (fitz) is not installed. Run: pip install pymupdf")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    total = len(doc)
    print(f"[INFO] Converting {total} pages at zoom={zoom} ...")

    mat = fitz.Matrix(zoom, zoom)
    generated = []

    for i, page in enumerate(doc):
        page_num = i + 1
        png_name = f"p{page_num:03d}.png"
        out_path = os.path.join(output_dir, png_name)
        if not os.path.exists(out_path):
            pix = page.get_pixmap(matrix=mat)
            pix.save(out_path)
        else:
            print(f"  [SKIP] {png_name} already exists")
        generated.append((page_num, png_name, out_path))
        if page_num % 20 == 0 or page_num == total:
            print(f"  [{page_num}/{total}] done")

    doc.close()
    return generated

def generate_assets_index(generated, output_dir, index_path):
    lines = [
        "# アセットインデックス / Assets Index",
        "",
        "このファイルはすべてのPDFページ画像へのリンクを含む。",
        "This file contains links to all PDF page images.",
        "",
        "| ページ | ファイル | プレビュー |",
        "|--------|----------|------------|",
    ]
    for page_num, png_name, _ in generated:
        rel_path = os.path.join(output_dir, png_name).lstrip("./")
        lines.append(f"| p.{page_num:03d} | [{png_name}]({rel_path}) | ![p{page_num:03d}]({rel_path}) |")

    lines += [
        "",
        "---",
        f"総ページ数 / Total pages: {len(generated)}",
    ]
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[INFO] assets_index.md written → {index_path}")

def main():
    parser = argparse.ArgumentParser(description="PDF → PNG page images pipeline")
    parser.add_argument("--pdf", default=None, help="Path to source PDF")
    parser.add_argument("--zoom", type=float, default=2.0, help="Render zoom factor (default 2.0)")
    parser.add_argument("--pages-dir", default="assets/pages", help="Output directory for page PNGs")
    parser.add_argument("--index", default="assets_index.md", help="Output path for assets_index.md")
    args = parser.parse_args()

    pdf_path = find_pdf(args.pdf)
    print(f"[INFO] Source PDF: {pdf_path}")

    generated = convert_pdf_to_png(pdf_path, args.pages_dir, zoom=args.zoom)
    generate_assets_index(generated, args.pages_dir, args.index)

    print(f"\n[DONE] {len(generated)} PNG images saved to '{args.pages_dir}/'")
    print(f"[DONE] assets_index.md → '{args.index}'")

if __name__ == "__main__":
    main()
