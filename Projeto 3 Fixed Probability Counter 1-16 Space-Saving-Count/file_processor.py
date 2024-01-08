import re
from unidecode import unidecode
from argparse import ArgumentParser

stopwords = set()

def pt_stopwords():
    with open("stopwords/stopwords_pt.txt", "r", encoding="utf-8") as f:
        for line in f:
            stopwords.add(line.strip().upper())

def en_stopwords():
    with open("stopwords/stopwords_en.txt", "r", encoding="utf-8") as f:
        for line in f:
            stopwords.add(line.strip().upper())

def es_stopwords():
    with open("stopwords/stopwords_es.txt", "r", encoding="utf-8") as f:
        for line in f:
            stopwords.add(line.strip().upper())

def process_line(line: str):
    line = unidecode(line)
    words = line.upper().split()
    words = [word for word in words if word not in stopwords]
    line = " ".join(words)
    line = re.sub(r"[^a-bA-Z]+", '', line)
    return line.strip()

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('-f', '--file', help='File to be processed')
    parser.add_argument('-l', '--language', help='Language of the file')
    args = parser.parse_args()

    if args.language == "pt":
        pt_stopwords()
    elif args.language == "en":
        en_stopwords()
    elif args.language == "es":
        es_stopwords()
    else:
        raise ValueError("Language not supported")

    doc = args.file
    save = False
    
    with open(doc, "r", encoding="utf-8") as f:
        with open("docs_processed/" + doc.split("\\")[-1], "w", encoding="utf-8") as fp:
            for line in f:
                line = line.strip()
                if save:
                    if line.startswith("***"):
                        break
                    if line:
                        fp.write(process_line(line))
                else:
                    if line.startswith("***"):
                        save = True
