from model.spam.SpamDetection import SpamDetection
from api.captions import importCaptions, fetchCaptions
from api.comment import importComments, fetchComments


# Only use getComments() once. Then use importComments() for testing
TESTING = True


def main():
    videoId = 'rfscVS0vtbw'
    comments: list

    if TESTING:
        comments = importComments()
        captions = importCaptions()
    else:
        comments = fetchComments(videoId)
        captions = fetchCaptions(videoId)

    # print(comments[0])
    # print(captions.keys())

    spamDetector = SpamDetection()
    print(f'Model Accurary Score: {spamDetector.score}')
    spamDetector.processComments(comments)


if __name__ == "__main__":
    main()
