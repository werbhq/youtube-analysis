from api.comment import importComments, fetchComments
from api.captions import importCaptions, fetchCaptions

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

    print(comments[0])
    print(captions.keys())


if __name__ == "__main__":
    main()
