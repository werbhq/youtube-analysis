from model.spam.SpamDetection import SpamDetection
from api.captions import import_captions, fetch_captions
from api.comment import import_comments, fetch_comments


# Only use getComments() once. Then use importComments() for testing
TESTING = True


def main():
    videoId = 'rfscVS0vtbw'
    comments: list

    if TESTING:
        comments = import_comments()
        captions = import_captions()
    else:
        comments = fetch_comments(videoId)
        captions = fetch_captions(videoId)

    # print(comments[0])
    # print(captions.keys())

    spamDetector = SpamDetection()
    print(f'Model Accurary Score: {spamDetector.score}')
    spamDetector.process_comments(comments)


if __name__ == "__main__":
    main()
