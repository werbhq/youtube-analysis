
from api.comment_extract import *

def main():
    # Only use getComments() once. Then use importComments() for testing
    # getComments('Ntn1-SocNiY')
    comments = importComments()
    print(comments[0])


if __name__ == "__main__":
    main()
