from model.spam.SpamDetection import SpamDetection
import api.captions as caption
import api.comment as comment


# Only use getComments() once. Then use importComments() for testing
TESTING = True


def main():
    videoId = 'rfscVS0vtbw'
    comments: list

    if TESTING:
        comments = comment.load()
        captions = caption.load()
    else:
        comments = comment.fetch(videoId)
        captions = caption.fetch(videoId)

    # print(comments[0])
    # print(captions.keys())

    spamDetector = SpamDetection()
    print(f'Model Accurary Score: {spamDetector.score}')
    spamDetector.process_comments(comments)


if __name__ == "__main__":
    main()
