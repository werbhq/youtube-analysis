from os.path import join as os_join, dirname as os_dirname, relpath as os_relpath, exists as path_exists
import pandas as pd
import json
import pickle
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import wordninja

from api import comment

FILE_PATH = os_join('temp', 'spam_comments.json')

DIR_PATH = os_dirname(os_relpath(__file__))
DATASET_PATH = os_join(DIR_PATH, "data", "data_set.csv")
MODEL_PATH = os_join(DIR_PATH,  "data", "model.bin")
VECTORIZER_PATH = os_join(DIR_PATH, "data", "vectorizer.bin")
SCORE_PATH = os_join(DIR_PATH, "data", "score.bin")


class SpamDetection:
    score: int
    __model: SVC
    __vectorizer: TfidfVectorizer

    def __init__(self, retrain_model=False):
        if not retrain_model and (path_exists(MODEL_PATH) and path_exists(VECTORIZER_PATH) and path_exists(SCORE_PATH)):
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

            x_train, x_test, y_train, y_test = train_test_split(data['CONTENT'], data['SPAM'], test_size=0.1, random_state=11)
            self.__vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
            x_train = self.__vectorizer.fit_transform(x_train)

            # save vectorizer file
            pickle.dump(self.__vectorizer, open(VECTORIZER_PATH, 'wb'))

            # train model on data
            self.__model = SVC(C=1000)
            self.__model.fit(x_train, y_train)

            # save ML model
            pickle.dump(self.__model, open(MODEL_PATH, 'wb'))

            # Save score
            x_test = self.__vectorizer.transform(x_test)
            self.score = self.__model.score(x_test, y_test)
            pickle.dump(self.score, open(SCORE_PATH, 'wb'))

    def __cleanComment(self, comment: str):
        comment = re.sub(r'[^A-Za-z0-9 ]+', '', comment)  # Remove special chars
        comment = ' '.join(wordninja.split(comment))  # convert 'h-e-y' type words to 'hey'
        comment = comment.lower()
        return comment

    def processComments(self, comments: list):
        """
        Checks whether the given comment in comments is a spam or not. Returns non-spam comments
        """
        comments_df = pd.DataFrame(comments)
        comments_cleaned = comments_df['textDisplay'].apply(self.__cleanComment)
        comment_transformed = self.__vectorizer.transform(comments_cleaned)
        comments_df['spam'] = self.__model.predict(comment_transformed)

        spam_comments = comments_df.loc[comments_df['spam'] == True].drop('spam', axis=1)
        non_spam_comments = comments_df.loc[comments_df['spam'] == False].drop('spam', axis=1)

        print(f'Dumping {len(spam_comments.index)}/{len(comments_df)} spam comments to {FILE_PATH}')

        with open(FILE_PATH, 'w') as f:
            f.write(json.dumps(spam_comments['textDisplay'].to_dict(), indent=4))

        return non_spam_comments.to_dict('records')
