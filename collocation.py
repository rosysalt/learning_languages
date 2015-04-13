import datetime, json, sys, urllib
import lxml.html as html

import pdb

def generate_filename(prefix = "", extension = ""):
    """
    return the string in the form "2015-03-24"
    """
    base_filename = datetime.date.strftime(datetime.date.today(), "%Y-%m-%d")
    return "%s%s.%s" % (prefix, base_filename, extension)

if __name__ == '__main__':
    PREFIX = "./html_files/"

    if len(sys.argv) == 1:
        sys.exit()
    elif len(sys.argv) == 2:
        input_file = sys.argv[1]
        output_file = generate_filename(prefix = PREFIX, extension = "html")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    words = []

    with open(input_file) as f:
        for line in f:
            words.append(line.strip())

    for word in words:
        raw_url = "http://www.ozdic.com/collocation-dictionary/%s"
        url = raw_url % (word)
        content = urllib.urlopen(url).read()
        doc = html.fromstring(content)

        word_html = doc.body.find_class("main-wrap")[0]

        # only keep div with class "item"
        children = word_html.getchildren()
        children_to_be_removed_later = []

        for child in children:
            if isinstance(child, html.HtmlElement) and len(child.find_class("item")) != 0:
                pass
            else:
                children_to_be_removed_later.append(child)

        for child in children_to_be_removed_later:
            word_html.remove(child)

        with open(output_file, "a") as output:
            word_html.append(html.fromstring("<hr>"))
            text = html.tostring(word_html)
            output.write(text)

