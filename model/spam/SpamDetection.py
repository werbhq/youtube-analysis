import os
import pandas as pd
import json
import pickle
import re
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
import wordninja

FILE_PATH = os.path.join('temp', 'spam_comments.json')
DATASET_PATH = os.path.join("model", "spam", "data", "data_set.csv")
MODEL_PATH = os.path.join("model", "spam", "data", "model.bin")
VECTORIZER_PATH = os.path.join("model", "spam", "data", "vectorizer.bin")
SCORE_PATH = os.path.join("model", "spam", "data", "score.bin")


class SpamDetection:
    score: int
    __model: MultinomialNB
    __vectorizer: TfidfVectorizer

    def __init__(self, retrain_model=False):
        if not retrain_model and (os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH) and os.path.exists(SCORE_PATH)):
            print('Loading model')
            self.__model = pickle.load(open(MODEL_PATH, 'rb'))
            self.__vectorizer = pickle.load(open(VECTORIZER_PATH, 'rb'))
            self.score = pickle.load(open(SCORE_PATH, 'rb'))
        else:
            print('Generating model')
            data = pd.read_csv(DATASET_PATH)

            data = data[["CONTENT", "SPAM"]]
            data["SPAM"] = data["SPAM"].map({0: False,  1: True})
            data["CONTENT"] = data["CONTENT"].apply(self.__cleanComment)
            data = data.drop_duplicates(subset="CONTENT")

            x_train, x_test, y_train, y_test = train_test_split(data['CONTENT'], data['SPAM'], test_size=0.1, random_state=45)
            self.__vectorizer = TfidfVectorizer()
            x_train = self.__vectorizer.fit_transform(x_train)

            # save vectorizer file
            pickle.dump(self.__vectorizer, open(VECTORIZER_PATH, 'wb'))

            # train model on data
            self.__model = svm.SVC(C=1000)
            self.__model.fit(x_train, y_train)

            # save ML model
            pickle.dump(self.__model, open(MODEL_PATH, 'wb'))

            # Save score
            x_test = self.__vectorizer.transform(x_test)
            self.score = self.__model.score(x_test, y_test)
            pickle.dump(self.score, open(SCORE_PATH, 'wb'))

    def __cleanComment(self, s: str):
        s = re.sub(r'[^A-Za-z0-9 ]+', '', s)
        s = ' '.join(wordninja.split(s))
        s = s.lower()
        return s

    def __checkSpam(self, comment: str):
        clean_comment = self.__cleanComment(comment)
        comment_transformed = self.__vectorizer.transform([clean_comment])
        spam = self.__model.predict(comment_transformed)[0]
        return spam == 1

    def processComments(self, comments: list):
        """
        Checks whether the given comment in comments is a spam or not. Returns non-spam comments
        """
        spamComments = []
        nonSpamComments = []
        for i in comments:
            spam = self.__checkSpam(i['textDisplay'])
            if spam:
                spamComments.append(i['textDisplay'])
            else:
                nonSpamComments.append(i)

        print(f'Dumping {len(spamComments)}/{len(comments)} spam comments to {FILE_PATH}')
        with open(FILE_PATH, 'w') as f:
            f.write(json.dumps(spamComments, indent=4))

        return nonSpamComments
