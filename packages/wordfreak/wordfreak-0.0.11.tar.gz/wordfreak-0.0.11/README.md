# Word Freak

Word Freak is a Python library that extracts word frequencies from files.

![Main Build](https://github.com/joeyagreco/wordfreak/actions/workflows/main-build.yml/badge.svg)
![Last Commit](https://img.shields.io/github/last-commit/joeyagreco/wordfreak)

## Supported File Types

| File Extension | Explanation                       | Supported          |
|----------------|-----------------------------------|--------------------|
| .doc           | Microsoft Word document pre-2007  | :x:                |
| .docx          | Microsoft Word document post-2007 | :heavy_check_mark: |
| .pdf           | Portable Document Format          | :heavy_check_mark: |
| .txt           | Plain text file                   | :heavy_check_mark: |

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install..

```bash
pip install wordfreak
```

## Usage

```python
import wordfreak

# Take a text source and save the word frequencies to JSON.
# Extracts word frequencies from 'inputFile.txt' and saves them to 'outputFile.json'.
wordfreak.extractWordFrequencies("C:\\inputFile.txt", "C:\\outputFile.json")

# Take a saved word frequencies JSON file and converts it to a Python dictionary.
# Loads word frequencies from 'wordFrequencies.json' and saves them to the variable wordFrequencyDict.
wordFrequencyDict = wordfreak.pythonizeWordFrequencies("C:\\wordFrequencies.json")
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)