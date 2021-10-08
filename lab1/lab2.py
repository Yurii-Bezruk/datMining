import re
import pandas
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


def split_rows(rows: list) -> list:
    arr = []
    for row in rows:
        arr.extend(row.split())
    return arr



def _filter(messages):
    for i in range(len(messages)):
        messages[i] = re.sub(r'\s', ' ', re.sub(r'([^\w\s]|\d|_)+', ' ', messages[i]).lower())
        for word in messages[i].split():
            messages[i] = messages[i].replace(f' {word} ', f' {stemmer.stem(word)} ')
        for word in messages[i].split():
            if word in stop_words:
                messages[i] = messages[i].replace(f' {word} ', ' ')
    return messages


def count_words(words: list) -> dict:
    dictionary = {}
    for word in words:
        if word in dictionary:
            dictionary[word] += 1
        else:
            dictionary[word] = 1
    return dictionary


# global objects using for filtering. Instantiating their only once
stop_words = set(stopwords.words('English'))
stemmer = PorterStemmer()

table = pandas.read_csv(filepath_or_buffer='sms-spam-corpus.csv', encoding='1251')
data = _filter(table.v2)

spam_rows = []
ham_rows = []
for i in range(table.v1.size):
    if table.v1[i] == 'spam':
        spam_rows.append(data[i])
    else:
        ham_rows.append(data[i])

spam_messages_count = len(spam_rows)
ham_messages_count = len(ham_rows)
all_messages_count = spam_messages_count + ham_messages_count

spam_words = split_rows(spam_rows)
ham_words = split_rows(ham_rows)

spam_freqs = count_words(spam_words)
ham_freqs = count_words(ham_words)

spam_probability = spam_messages_count / all_messages_count
ham_probability = ham_messages_count / all_messages_count

print(spam_rows)