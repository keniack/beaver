# 🦫 Beaver — Smart BibTeX Deduplicator

**Beaver** is a handy Python tool for merging multiple `.bib` (BibTeX) files while detecting and resolving duplicate entries intelligently.

Whether you're managing references for a paper or cleaning up your library, Beaver helps you streamline and clean your citations — without losing anything important.

---

## 🔧 Features

- ✅ Scans all `.bib` files in a folder
- ✅ Detects duplicates **by title**, not just BibTeX keys
- ✅ Automatically removes:
  - Exact duplicates
  - Less-informative `@online` entries if better ones exist
- ✅ Prompts user when manual decision is needed
- ✅ Merges everything into a clean `merged.bib` file

---

## 📦 Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/yourusername/beaver.git
   cd beaver
   ```

2. Install dependencies:
```
pip install bibtexparser
```
