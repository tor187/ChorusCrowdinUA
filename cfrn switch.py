#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from pathlib import Path
import sys
import tkinter as tk
from tkinter import filedialog

def process_file(file_path, mode):
    p = Path(file_path)
    out_path = p.with_name(p.stem + ("_converted.csv" if mode=="cf_to_nl" else "_reverted.csv"))

    try:
        with p.open("r", encoding="utf-8-sig", newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            fieldnames = reader.fieldnames
    except Exception as e:
        print(f"[!] Не вдалося прочитати {p.name}: {e}")
        return

    try:
        with out_path.open("w", encoding="utf-8-sig", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                new_row = row.copy()
                for col in fieldnames:
                    if col in new_row and new_row[col]:
                        val = str(new_row[col])
                        if mode == "cf_to_nl":
                            val = val.replace("<cf>", "\r\n")
                        elif mode == "nl_to_cf":
                            val = val.replace("\r\n", "<cf>").replace("\n", "<cf>").replace("\r", "<cf>")
                        new_row[col] = val
                writer.writerow(new_row)
    except Exception as e:
        print(f"[!] Не вдалося записати {out_path.name}: {e}")
        return

    print(f"[+] Оброблено {p.name} -> {out_path.name}")

def main():
    mode = ""
    while mode not in ("1", "2"):
        print("Оберіть режим:")
        print("1 - <cf> -> новий рядок")
        print("2 - новий рядок -> <cf>")
        mode = input("Введіть 1 або 2: ").strip()
    mode = "cf_to_nl" if mode=="1" else "nl_to_cf"

    if len(sys.argv) > 1:
        file_paths = sys.argv[1:]
    else:
        root = tk.Tk()
        root.withdraw()
        file_paths = filedialog.askopenfilenames(title="Виберіть CSV файли", filetypes=[("CSV files", "*.csv")])
        file_paths = list(file_paths)

    if not file_paths:
        print("Файли не вибрано.")
        return

    # обробка файлів у алфавітному порядку
    for file_path in sorted(file_paths):
        process_file(file_path, mode)

    print("Готово.")

if __name__ == "__main__":
    main()
