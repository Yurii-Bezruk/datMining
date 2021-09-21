import copy
import re
import pandas
from matplotlib import pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def split_rows(rows: list) -> list:
    arr = []
    for row in rows:
        arr.extend(row.split())
    return arr


def count_words(words: list) -> dict:
    dictionary = {}
    for word in words:
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
    return dictionary


def write_frequencies_to_csv(dictionary: dict, filename: str):
    df = pandas.DataFrame(data={'words': dictionary.keys(), 'count': dictionary.values()})
    df.to_csv(filename, index=False)


def count_string_sizes_frequency(words: list):
    words_sizes = {}
    for word in words:
        length = len(word)
        if length in words_sizes:
            words_sizes[length] += 1
        else:
            words_sizes[length] = 1
    return words_sizes


def get_average(words_freq: dict) -> int:
    summary = 0
    for k, v in words_freq.items():
        summary += k * v
    return summary / sum(words_freq.values())


def process_count_sizes_of_word(data: list, category: str):
    count_of_word_sizes = count_string_sizes_frequency(data)
    average = get_average(count_of_word_sizes)
    gist(count_of_word_sizes.keys(), count_of_word_sizes.values(),
         'word sizes', 'count of words', f'word sizes count: {category}', average)


def process_count_of_message_length(rows: list, category: str):
    messages = []
    for row in rows:
        messages.append(re.sub(r'\s+', ' ', row).strip())
    count_of_massages_sizes = count_string_sizes_frequency(messages)
    average = get_average(count_of_massages_sizes)
    gist(count_of_massages_sizes.keys(), count_of_massages_sizes.values(),
         'message sizes', 'count of messages', f'messages sizes count: {category}', average)


def get_most_frequent_words(words_dictionary: dict, count: int) -> list:
    frequencies = list(words_dictionary.items())
    frequencies = sorted(frequencies, key=lambda cortege: cortege[1], reverse=True)[:count]
    return frequencies


def process_most_frequent_words(words_dictionary: dict, count: int, category: str):
    most_freq = get_most_frequent_words(words_dictionary, count)
    most_freq_dict = {cortege[0]: cortege[1] for cortege in most_freq}
    gist(most_freq_dict.keys(), most_freq_dict.values(),
         'words', 'frequency', f'words biggest frequency: {category}')


def gist(x_values, y_values, x_label, y_label, title, average=None):
    plt.figure(figsize=(10, 5))
    plt.bar(x_values, y_values)
    if average is not None:
        plt.axvline(x=average, c='red')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()


def process(rows: list, category: str):
    words = split_rows(rows)
    freqs = count_words(words)
    write_frequencies_to_csv(freqs, f'output\\{category}.csv')
    words = list(freqs.keys())
    process_count_sizes_of_word(words, category)
    process_count_of_message_length(rows, category)
    process_most_frequent_words(freqs, 20, category)


stop_words = set(stopwords.words('English'))
table = pandas.read_csv(filepath_or_buffer='sms-spam-corpus.csv', encoding='1251')
data = table.v2
stemmer = PorterStemmer()
for i in range(len(data)):
    data[i] = re.sub(r'\s', ' ', re.sub(r'([^\w\s]|\d|_)+', ' ', data[i]).lower())
    for word in data[i].split():
        data[i] = data[i].replace(f' {word} ', f' {stemmer.stem(word)} ')
    for word in data[i].split():
        if word in stop_words:
            data[i] = data[i].replace(f' {word} ', ' ')

spam_rows = []
ham_rows = []
for i in range(table.v1.size):
    if table.v1[i] == 'spam':
        spam_rows.append(table.v2[i])
    else:
        ham_rows.append(table.v2[i])

process(spam_rows, 'spam')
process(ham_rows, 'ham')
