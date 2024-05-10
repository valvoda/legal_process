import numpy as np
import csv
import os
import ast
import re

from translate import Translate

class Preproces:

    def __init__(self):
        self.T = Translate()

    def view_case(self, filename):
        arr = np.loadtxt(filename, delimiter="\t", dtype=str)
        for sent in arr[1:]:
            list_sent = ast.literal_eval(sent[0])
            print(list_sent)

    def article_extractor(self, list_sent):
        """

        Core regex logic to find instances of a section with a reasoning over a single Article.

        :param list_sent:
        :return:
        """
        # print(" ".join(list_sent).lower())
        lower_sent = " ".join(list_sent).lower()
        if 'articles' not in lower_sent and 'protocol' not in lower_sent:
            extraction = re.findall("article", lower_sent)
            if len(extraction) == 1:
                # print(int(re.findall("article (\d{1,2})", lower_sent)[0]))
                return int(re.findall("article (\d{1,2})", lower_sent)[0])

        return None

    def basic_labels(self, arr, articles, art_range):
        sections = []
        articles = []
        section = []

        collect = False
        for sent in arr[1:]:
            list_sent = ast.literal_eval(sent[0])
            list_labels = ast.literal_eval(sent[1])

            if 'ARTICLE' in list_sent or 'ARTICLES' in list_sent or 'L’ARTICLE' in list_sent or 'UNANIMOUSLY' in list_sent:
                # collect previous section
                if collect:
                    sections.append(section)
                    section = []

                article = self.article_extractor(list_sent)
                if article is not None:
                    articles.append(article)
                    collect = True
                else:
                    collect = False

            if collect:
                section.append((list_sent, list_labels))

        # collect section at the end of the case
        if collect:
            sections.append(section)

        return articles, sections

    def get_label(self, filename, art_range, get_outliers=True):
        # print("\n\n" + filename)
        arr = np.loadtxt(filename, delimiter="\t", dtype=str)
        articles = []
        articles, sections = self.basic_labels(arr, articles, art_range)

        return articles, sections

    def process_labels(self, section):
        all_args = []
        for sentence in section:
            all_args += sentence[1]
        return self.clean_labels(all_args)

    def clean_labels(self, all_args):
        clean_args = []
        past = None
        for arg in all_args:
            if arg != 'O':
                # strip  the 'I-' or 'B-' from the label 'I-Subsumtion' -> 'Subsumtion'
                arg = arg[2:]
            if arg != past:
                # translate to english
                clean_args.append(self.T.translate(arg))
            past = arg
        return clean_args

    def save_data(self, casename, art, case):
        directory_path = "LP_Dataset/eng_LP_" + art + "/"
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        writer = csv.writer(open(directory_path + casename + ".csv", 'w'))
        for row in case:
            writer.writerow([row])


def extract_ECtHR(dataset_path):
    """
    Finds labels for each case and splits the case into Article relevant sections.

    :param dataset_path: path to input dataset location
    :return: saves processed dataset under LP_Dataset
    """

    P = Preproces()
    case_names = [dataset_path + i for i in os.listdir(dataset_path)]

    print("Dataset Size: ", len(case_names))

    legal_process_dataset = []
    case_ids = []
    case_articles = []
    art_range = list(range(1, 13))

    malformed = 0

    # process the input files
    for case in case_names:
        names = case.split('/')[-1].split('.')[0]

        # get sections of the case paired with an article
        articles, sections = P.get_label(case, art_range, get_outliers=False)
        if len(articles) == 0:
            print(case)
            malformed += 1

        for article, section in zip(articles, sections):
            case_ids.append(names)
            case_articles.append(article)
            legal_process_dataset.append(P.process_labels(section))

    print("total_malformed: ", malformed)

    # save the dataset
    for name, art, case in zip(case_ids, case_articles, legal_process_dataset):
        P.save_data(str(name), str(art), case)

if __name__ == '__main__':
    dataset_path = './ECtHR/'
    extract_ECtHR(dataset_path)

