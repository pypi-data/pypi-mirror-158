# Word Freak

Word Freak is a Python library that extracts word frequencies from files.

![Main Build](https://github.com/joeyagreco/wordfreak/actions/workflows/main-build.yml/badge.svg)
![Last Commit](https://img.shields.io/github/last-commit/joeyagreco/wordfreak)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install..

```bash
pip install wordfreak
```

## Usage

```python
import wordfreak

# Extracts word frequencies from 'inputFile.txt' and saves them to 'outputFile.json'
wordfreak.extractWordFrequencies("C:\\inputFile.txt", "C:\\outputFile.json")
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)