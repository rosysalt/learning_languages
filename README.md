In the ```script.sh``` you can find example on how to run those files.

# Collocation

The website that I use to get collocation is http://www.ozdic.com. From what I understand, this website get their content from the _Oxford Collocations Dictionary for students of English_.

All code are in file ```collocation.py```. This piece of code help downloading the collocation of a list of English words, and put them all in a single _HTML_ file for your convenient.

```python collocation.py input_file [output_html_file]```

In order to run, you need at least one command-line argument, specify the file containing English words that you want to their collocation.

If you leave the 2nd command-line argument empty, the _HTML_ file name will be automatically generated for you. For example, if today is Apr 13, 2015, then the file name will be *./html_files/2015-04-13.html*

It's for my convenient that I put all _HTML_ files in a single folder called ```html_files```. If that is not what you want, then specify the 2nd argument.

# Other notes

I put the sample academic word list in ```./word_lists``` folder. And I downloaded it from: http://www.nottingham.ac.uk/alzsh3/acvocab/wordlists.htm