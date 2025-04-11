import os
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

def load_bib_files(folder):
    all_entries = []
    for filename in os.listdir(folder):
        if filename.endswith(".bib"):
            filepath = os.path.join(folder, filename)
            with open(filepath, "r", encoding="utf-8") as bib_file:
                parser = BibTexParser(common_strings=True)
                parser.ignore_nonstandard_types = False  # ✅ Accept @online and other custom types
                parser.customization = convert_to_unicode
                bib_database = bibtexparser.load(bib_file, parser=parser)
                all_entries.extend(bib_database.entries)
    return all_entries

def group_by_title(entries):
    grouped = {}
    for entry in entries:
        title = entry.get("title", "").strip().lower()
        if not title:
            continue
        grouped.setdefault(title, []).append(entry)
    return grouped

def entries_are_equal(e1, e2):
    keys = set(e1.keys()).union(set(e2.keys()))
    for key in keys:
        if e1.get(key, "").strip() != e2.get(key, "").strip():
            return False
    return True

def resolve_duplicates(grouped_entries):
    resolved = []

    for title, duplicates in grouped_entries.items():
        # Remove exact duplicates
        unique = []
        for entry in duplicates:
            if not any(entries_are_equal(entry, existing) for existing in unique):
                unique.append(entry)

        if len(unique) == 1:
            resolved.append(unique[0])
            continue

        # Remove 'online' entries if there are better options
        non_online = [e for e in unique if e.get("ENTRYTYPE", "").lower() != "online"]
        if len(non_online) == 1:
            resolved.append(non_online[0])
            continue
        elif len(non_online) > 1 and len(non_online) < len(unique):
            unique = non_online

        if len(unique) == 1:
            resolved.append(unique[0])
        else:
            # Prompt user
            print(f"\n❗ Duplicate entries found for title:\n  {title}\n")
            for i, entry in enumerate(unique):
                print(f"Version {i + 1}:")
                for k, v in entry.items():
                    print(f"  {k}: {v}")
                print()
            while True:
                try:
                    choice = int(input(f"Choose which version to keep (1-{len(unique)}): "))
                    if 1 <= choice <= len(unique):
                        resolved.append(unique[choice - 1])
                        break
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Enter a number.")
    return resolved

def write_merged_bib(entries, output_file):
    from bibtexparser.bwriter import BibTexWriter
    writer = BibTexWriter()
    writer.indent = '    '
    writer.order_entries_by = ('ID',)
    bib_database = bibtexparser.bibdatabase.BibDatabase()
    bib_database.entries = entries
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(writer.write(bib_database))

def main():
    folder = input("📁 Enter the path to the folder with .bib files: ").strip()
    all_entries = load_bib_files(folder)
    grouped = group_by_title(all_entries)
    resolved_entries = resolve_duplicates(grouped)

    output_path = os.path.join(folder, "merged.bib")
    write_merged_bib(resolved_entries, output_path)
    print(f"\n✅ Merged .bib file written to: {output_path}")

if __name__ == "__main__":
    main()

