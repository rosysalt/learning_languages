import csv
from datetime import datetime as dt
import urllib, urllib2, cookielib
import pprint
import lxml.html as html

from pdb import set_trace as debugger

WORD_LIST_FILE = "words.txt"

BASE_URL = 'http://www.collinsdictionary.com/dictionary/italian-english/% s'
CLASS_NAME_MEANING = ['sense_list_item level_2', 'cit-type-translation']
CLASS_NAME_PHRASE = 'phrase'
CLASS_NAME_GRAMMAR = 'gramGrp'
CLASS_NAME_IPA = 'pron'
CSV_FILENAME = ''

DEFAULT_TAG = ['bravissimo2_3']

def find_context_by_class(class_name, doc):
    """
        class_name: String object
        doc: Element object (from lxml library)

        Return: Array of text corresponding to the found elements.
    """
    found_elements = []
    final_result = []

    found_elements = doc.find_class(class_name)
    for element in found_elements:
        final_result.append(element.text_content())

    return final_result

def find_meanings(class_names, doc):
    """
        class_names: array of class_name to try on
    """
    found_elements = []
    final_result = []

    for name in class_names:
        if len(final_result) == 0:
            final_result = find_context_by_class(name, doc)

    return final_result

def find_phrases(class_name, doc):
    """
        class_name: String object
        doc: Element object (from lxml library)

        Return: Array of text corresponding to the found elements.

            Separate the original Italian phrases with their English translation

        For example:
            [
                "all'epoca di = at the time of",
                "in epoca bizantina = in the Byzantine era"
            ]
    """
    found_elements = doc.find_class(class_name)
    final_result = []

    phrase_template = '%s ='

    for element in found_elements:
        childrens = element.getchildren()
        if len(childrens) >= 2:
            phrase = phrase_template % (childrens[0].text_content())

            for meaning in childrens[1:]:
                phrase += ' %s' % meaning.text_content()

            final_result.append(phrase)

    return final_result

def create_tag(default_tag, grammar_notes=[]):
    """
        Each tag is separated by white space.
        Return: "tag_1 tag_2"
    """
    tag = " ".join(default_tag)

    if 'irregular' in grammar_notes:
        tag.append('irregular')

    return tag

def build_csv_row(word, meanings, phrases, notes, tag):
    """
    """
    row = []

    selected_meanings = let_user_select(meanings)
    selected_phrases = let_user_select(phrases)

    row.append(word.encode('utf-8'))
    row.append(format_multiple_row_in_cell(selected_meanings).encode('utf-8'))
    row.append(', '.join(notes).encode('utf-8'))
    row.append(format_multiple_row_in_cell(selected_phrases).encode('utf-8'))
    row.append(tag.encode('utf-8'))

    return row

def let_user_select(array_of_text):
    """
        print "Choose the meaning/phrases to include by inputting the number."
        print "For example:"
        print "1 ==> to choose only the line number 1"
        print "1 5 ==> choose lines number 1 and 5."
    """
    print "**********"
    for index, text in enumerate(array_of_text):
        print '%d | %s' % (index, text)

    input_text = raw_input("Choose the number: ")

    # parse input_text
    selected_text = []
    try:
        choosen_numbers = input_text.split(' ')
        for number in choosen_numbers:
            selected_text.append(array_of_text[int(number)])
    except Exception as e:
        print e

    return selected_text

def format_multiple_row_in_cell(array_of_text):
    """
        Since Anki recognize the HTML tag, so I need to convert the \newline
        character to the <br>
    """
    if len(array_of_text) == 0:
        return ""

    string_format = '%d. %s'
    offset = 1
    out_string = string_format % (offset, array_of_text[0])
    offset += 1

    prefix = "<br>"
    for index, value in enumerate(array_of_text[1:]):
        out_string += prefix + string_format % (offset + index, array_of_text[0])

    return out_string

def write_csv_row(file_name, csv_row):
    f = open(file_name, 'a')
    writer = csv.writer(f)
    writer.writerow(csv_row)
    f.close()

def write_csv(file_name, csv_data):
    f = open(file_name, 'w')
    writer = csv.writer(f)
    for row in csv_data:
        writer.writerow(row)
    f.close()

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    # Generate CSV file name
    CSV_FILENAME = 'anki_%s.%s' % (dt.today().strftime('%Y-%m-%d-%H-%M'), 'csv')
    csv_data = []

    # Read the list of words
    words = []
    with open(WORD_LIST_FILE) as file:
        for line in file:
            words.append(line.strip())

    # Download pronunciation for words
    for word in words:
        content = urllib.urlopen(BASE_URL % word).read()

        with open('temp.html', 'w') as out:
            out.write(content)

        try:
            doc = html.fromstring(content)

            root_word = doc.find_class('orth')[0].text

            print "================="
            print root_word
            print "================="

            meanings = find_meanings(CLASS_NAME_MEANING, doc)
            phrases = find_phrases(CLASS_NAME_PHRASE, doc)

            IPA = doc.find_class(CLASS_NAME_IPA)[0].text_content()

            grammar_notes = find_context_by_class('infl_substitute', doc)
            grammar_notes = grammar_notes + find_context_by_class(CLASS_NAME_GRAMMAR, doc)

            tag = create_tag(DEFAULT_TAG, grammar_notes)

            csv_row = build_csv_row(root_word, meanings, phrases, grammar_notes, tag)
            csv_data.append(csv_row)
            write_csv_row(CSV_FILENAME, csv_row)
        except Exception as e:
            print word
            print e

    """
    If you only want to write to CSV file for all the words at one time
    enable this
    """
    # write_csv('words_anki.csv', csv_data)