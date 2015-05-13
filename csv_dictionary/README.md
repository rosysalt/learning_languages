### What is it about?

Generate a mini-dictionary Italian-English in CSV-format. User will select the meanings + examples that they want to include.

The dictionary in used here is Collins Dictionary.

### How to run?

0. Put a list of words in `words.txt`. Example:

```
madre
padre
cugino
```

0. You might want to edit value of `DEFAULT_TAG`

0. Run with `python collin_italian.py`

0. The `*.csv` file will be generated. The content of csv file:

* Word: the word that we want to study
* Meaning: meaning of that word
* Phrases: common phrases that we use with that word
* Note: note such as masculine noun/feminine noun/irregular verb, etc.
* Tag: this is optional, you can

0. Then you can add this `*.csv` file to software such as Anki to help you to learn
new words

### Other notes

* Have your internet connection turned on.