import math
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


def count_word_not_in_category(words: list, category: dict):
    counter = 0
    for word in words:
        if word in category.keys():
            counter += 1
    return counter


def tested_message_in_category_probability(message_words: list, category_words: dict, category_size: int) -> float:
    probability = 0
    count_of_words_not_in_category = count_word_not_in_category(message_words, category_words)
    for word in message_words:
        count = category_words.get(word)
        if count is None:
            count = 0
        if count_of_words_not_in_category > 0:
            count += 1
        word_probability = count / (category_size + count_of_words_not_in_category)
        probability += math.log(word_probability)
    return probability


# global objects using for filtering. Instantiating their only once
stop_words = set(stopwords.words('English'))
stemmer = PorterStemmer()
table = pandas.read_csv(filepath_or_buffer='sms-spam-corpus.csv', encoding='1251')
data = _filter(table.v2)
testing_message = _filter([input()])[0]

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

spam_probability = spam_messages_count / all_messages_count
ham_probability = ham_messages_count / all_messages_count

spam_words = split_rows(spam_rows)
ham_words = split_rows(ham_rows)
testing_message_words = split_rows([testing_message])

spam_freqs = count_words(spam_words)
ham_freqs = count_words(ham_words)

testing_message_spam_probability = \
    math.log(spam_probability) + \
    tested_message_in_category_probability(testing_message_words, spam_freqs, len(spam_words))

testing_message_ham_probability = \
    math.log(ham_probability) + \
    tested_message_in_category_probability(testing_message_words, ham_freqs, len(ham_words))

# backward potentiating
testing_message_spam_probability = math.e ** testing_message_spam_probability
testing_message_ham_probability = math.e ** testing_message_ham_probability

# normalizing
normaled_testing_message_spam_probability = \
    testing_message_spam_probability / (testing_message_spam_probability + testing_message_ham_probability)

normaled_testing_message_ham_probability = \
    testing_message_ham_probability / (testing_message_spam_probability + testing_message_ham_probability)

print(normaled_testing_message_spam_probability)
print(normaled_testing_message_ham_probability)
result = ''
if normaled_testing_message_spam_probability > normaled_testing_message_ham_probability:
    result = 'spam'
else:
    result = 'ham'
print('message is '+result)
