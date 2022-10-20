from api.comment import importComments, getComments


def main():
    # Only use getComments() once. Then use importComments() for testing
    # comments = getComments('Ntn1-SocNiY')
    comments = importComments()
    print(comments[0])


if __name__ == "__main__":
    main()
