import os
import pandas as pd
import numpy as np
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

FILE_PATH = os.path.join('temp', 'revelevant_comments.json')


class RelevanceDetection:
    score: int
    __model: MultinomialNB
    __cv: CountVectorizer

    def __init__(self) -> None:
        MODEL_PATH = os.path.join("model", "relevance", "relevance.csv")
        data = pd.read_csv(MODEL_PATH)

        data = data[["CONTENT", "RELEVANT"]]
        data["RELEVANT"] = data["RELEVANT"].map({0: False,  1: True})

        x = np.array(data["CONTENT"])
        y = np.array(data["RELEVANT"])

        """
        Counte Vectorization
        --------------------
        Say there are 3 sentences:-
        0 apple is good
        1 apple is bad
        2 apple apple you

        now countVectorization o/p
        ----------------------------
            apple bad good is you    (columns are alphabetically sorted)
        0   1     0    1   1    0
        1   1     1    0   1    0
        2   2     0    0   0    1
        """
        self.__cv = CountVectorizer()
        x = self.__cv.fit_transform(x)

        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=42)

        self.__model = MultinomialNB()
        self.__model.fit(xtrain, ytrain)

        self.score = self.__model.score(xtest, ytest)

    def __checkSpam(self, comment: str):
        """
        Input comment: apple is great
        Example: countVectorization o/p
        ----------------------------
            apple bad good is you
        0   1     0    0   1    0
        """
        data = self.__cv.transform([comment]).toarray()  # This will generate the mapping to previously set CV
        return self.__model.predict(data)[0]

    def processComments(self, comments: list):
        """
        Checks whether the given comment in comments is a relevant or not. Returns non-relevant comments
        """
        relevantComments = []
        nonRelevantComments = []
        for i in comments:
            spam = self.__checkSpam(i['textDisplay'])
            if spam:
                relevantComments.append(i['textDisplay'])
            else:
                nonRelevantComments.append(i)

        print(f'Dumping {len(relevantComments)}/{len(comments)} spam comments to {FILE_PATH}')
        with open(FILE_PATH, 'w') as f:
            f.write(json.dumps(relevantComments, indent=4))

        return nonRelevantComments
