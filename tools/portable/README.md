# Consistency Scan Tool

This is a self-contained, portable Node.js tool used to detect potential inconsistencies in how terms are defined across different pieces of study material.

## Usage

```bash
node consistency_scan.mjs <items.json> [glossary.json] [--json]
```

### Inputs

* **items.json** (required): An array of items to scan. It should follow this shape:
  ```json
  [
    {
      "id": "x1",
      "surface": "econ_card_content",
      "ref": "file:row",
      "subject": "economics",
      "text": "Inflation is a general increase in prices..."
    }
  ]
  ```
* **glossary.json** (optional): A JSON object mapping terms to their definitions. If provided, the tool uses these keys as the terms to scan. If omitted, the tool automatically extracts capitalized or repeated multi-word noun phrases from the text.
  ```json
  {
    "inflation": { "def": "..." },
    "demand": { "def": "..." }
  }
  ```
* **--json** (optional): If provided, the output is printed as JSON instead of human-readable text.

### Output

By default, it prints a readable report grouping conflicts by term. With `--json`, it writes `{ conflicts: [{ term, items: [...], reason, overlap }], meta: { terms_scanned, conflicts } }`.

## How it works

1. **Term Indexing**: Gathers terms to scan (either from the glossary or automatically extracted).
2. **Definitional Extraction**: Extracts sentences containing terms matching patterns like "is", "means", "refers to", etc.
3. **Conflict Detection**: Compares definitions of the same term and flags a conflict if:
   * **Low Overlap**: The Jaccard similarity over content words is strictly below the threshold (0.2).
   * **Antonym Match**: It contains an opposing word pair from the built-in antonym list (e.g., increase/decrease, left/right).
   * **Negation**: One definition contains the word "not" or "never" before a content word found in the other definition.
   * **Numeric Mismatch**: Different explicit numbers (or percentages/units) appear across the definitions.

## Thresholds & Constants

* **Jaccard Overlap Threshold**: `0.2` (below this value, definitions are considered to have conflicting/low lexical overlap).
* **Stop Words**: A built-in common list of English stop words is excluded during tokenization and overlap checks.
