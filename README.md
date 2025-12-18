# Streaming Catalog Analysis & Exploration

This is a **self-initiated, personal data analysis project** where I explore publicly available streaming catalog datasets (Netflix, Amazon Prime, Disney+) to improve my skills in Python, data analysis, and project structuring.

I chose this project independently to:
- practice working with real-world, imperfect datasets,
- develop clearer exploratory data analysis (EDA) workflows,
- build reusable cleaning and analysis utilities,
- and gradually turn exploratory notebooks into a more structured, portfolio-ready project.

The project is **iterative and actively evolving** rather than a finished product.

---

## Project Status

✅ Initial exploratory analysis per platform  
✅ Shared data cleaning and helper functions  
🛠️ Ongoing refactor for clarity, reuse, and documentation  
🛠️ Planned: cross-platform comparison & interactive data exploration

---

## What the project explores

The datasets describe streaming catalogs (titles, content type, release year, duration, cast, countries, genres, ratings, etc.).

Some of the questions explored so far:
- How do streaming catalogs differ by platform?
- What do movie runtimes and TV season distributions look like?
- How are genres and cast members distributed?
- Which genres have the broadest range of unique actors?

The emphasis is on **understanding the data**, not just producing plots.

---

## Structure (current)

- `streaming_func.py`  
  Reusable cleaning and analysis utilities shared across notebooks.

- `netflix_analysis.ipynb`  
  Exploratory data analysis of Netflix’s catalog.

- `amazon_prime_analysis.ipynb`  
  Exploratory data analysis of Amazon Prime’s catalog.

- `disney_analysis.ipynb`  
  Exploratory data analysis of Disney+’s catalog.

> The structure is being refined as I improve the project’s organisation and reusability.

---

## How to run

1. Clone the repository:
   ```bash
   git clone https://github.com/JediJoni/streaming_analysis.git
   cd streaming_analysis
