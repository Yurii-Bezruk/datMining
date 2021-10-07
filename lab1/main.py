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


def process_count_sizes_of_word(data: list, color) -> float:
    count_of_word_sizes = count_string_sizes_frequency(data)
    average = get_average(count_of_word_sizes)
    values = list(count_of_word_sizes.values())
    minimum = min(values)
    maximum = max(values)
    for i in range(len(values)):
        values[i] = (values[i] - minimum) / (maximum - minimum)
    plots[0, 0].bar(count_of_word_sizes.keys(), values, color=color, alpha=0.5)
    return average


def process_count_of_message_length(rows: list, color) -> float:
    messages = []
    for row in rows:
        messages.append(re.sub(r'\s+', ' ', row).strip())
    count_of_massages_sizes = count_string_sizes_frequency(messages)
    average = get_average(count_of_massages_sizes)
    values = list(count_of_massages_sizes.values())
    minimum = min(values)
    maximum = max(values)
    for i in range(len(values)):
        values[i] = (values[i] - minimum) / (maximum - minimum)
    plots[0, 1].bar(count_of_massages_sizes.keys(), values, color=color, alpha=0.5)
    return average


def get_most_frequent_words(words_dictionary: dict, count: int) -> list:
    frequencies = list(words_dictionary.items())
    frequencies = sorted(frequencies, key=lambda cortege: cortege[1], reverse=True)[:count]
    return frequencies


def process_most_frequent_words(words_dictionary: dict, count: int, plt_num: int):
    most_freq = get_most_frequent_words(words_dictionary, count)
    most_freq_dict = {cortege[0]: cortege[1] for cortege in most_freq}
    values = list(most_freq_dict.values())
    minimum = min(values)
    maximum = max(values)
    for i in range(len(values)):
        values[i] = (values[i] - minimum) / (maximum - minimum)
    plots[1, plt_num - 1].bar(most_freq_dict.keys(), values)


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

spam_words = split_rows(spam_rows)
ham_words = split_rows(ham_rows)
spam_freqs = count_words(spam_words)
ham_freqs = count_words(ham_words)
write_frequencies_to_csv(spam_freqs, 'output\\spam.csv')
write_frequencies_to_csv(ham_freqs, 'output\\ham.csv')
spam_words = list(spam_freqs.keys())
ham_words = list(ham_freqs.keys())

_, plots = plt.subplots(2, 2)

spam_average = process_count_sizes_of_word(spam_words, 'blue')
ham_average = process_count_sizes_of_word(ham_words, 'green')
plots[0, 0].axvline(x=(spam_average + ham_average) / 2, c='red')
plots[0, 0].legend(['average count', 'spam', 'ham'])
plots[0, 0].set_xlabel('word sizes')
plots[0, 0].set_ylabel('count of words')


spam_average = process_count_of_message_length(spam_rows, 'blue')
ham_average = process_count_of_message_length(ham_rows, 'green')
plots[0, 1].axvline(x=(spam_average + ham_average) / 2, c='red')
plots[0, 1].legend(['average count', 'spam', 'ham'])
plots[0, 1].set_xlabel('message sizes')
plots[0, 1].set_ylabel('count of messages')

process_most_frequent_words(spam_freqs, 20, 1)
plots[1, 0].legend(['spam'])
plots[1, 0].set_xlabel('words')
plots[1, 0].set_ylabel('frequency')

process_most_frequent_words(ham_freqs, 20, 2)
plots[1, 1].legend(['ham'])
plots[1, 1].set_xlabel('words')
plots[1, 1].set_ylabel('frequency')

plt.setp(plots[1, 0].get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')
plt.setp(plots[1, 1].get_xticklabels(), rotation=45, ha='right', rotation_mode='anchor')
plt.get_current_fig_manager().window.state('zoomed')
plt.show()
