from api.comment import importComments, getComments

# Only use getComments() once. Then use importComments() for testing
TESTING = False


def main():
    videoId = 'Ntn1-SocNiY'
    comments: list

    if TESTING:
        comments = importComments()
    else:
        comments = getComments(videoId)

    print(comments[0])


if __name__ == "__main__":
    main()
