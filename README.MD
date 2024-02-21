# JobClassifer_ResearchLab_23-24

## Description
Job advertisement records of description for continuing education opportunites that are not mapped to taxonomy KIdB (Classification of Jobs)

Inorder to avoid manual classification, this project serves the purpose to automatically cluster these unknown into groups to make classification easier.

This repository contains code for a text classifier that performs clustering on German job description data using SpaCy and scikit-learn. The classifier aims to group similar texts together based on their content.

## Usage
The text classifier consists of several Python scripts and functions. Here's an overview of the main components:

`job_classifer.ipynb`: Contains functions for data preprocessing, feature extraction, clustering, and visualization.
german_stopwords_plain.txt: File containing a list of common German stopwords (for preprocessing).
german_stopwords_full.txt: File containing an extended list of German stopwords.
weiterbildung_new_data.db: SQLite database file containing the text data for analysis.
To use the classifier, follow these steps:

Ensure that the SQLite database file `weiterbildung_new_data.db` is available.
Run the `job_classifer.ipynb` script to preprocess the data, perform clustering, and visualize the results.

## Dependency
- Python Version: 3.10.12
- Sqlite Studio

## Installation
```bash
python3 install matplotlib sklearn pandas sqlite3 spacy
```

## API Link
https://andreasfischer1985.github.io/arbeitsagentur-apis/


## Methods
Following methods are used:

### Sentence Embedding
- Tf-IDF

### Clustering
- k-means clustering
- PCA -> t-SNE

## Acknowledgements
This project makes use of SpaCy, scikit-learn, and other open-source libraries. We acknowledge the contributions of the developers and maintainers of these libraries.
