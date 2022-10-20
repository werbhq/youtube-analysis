def process_comments(response_items):
    comments = []
    for res in response_items:

        # for reply comments
        # if 'replies' in res.keys():
        #     for reply in res['replies']['comments']:
        #         comment = reply['snippet']
        #         comment['commentId'] = reply['id']
        #         comments.append(comment)

        # for non reply comments
        if 'replies' not in res.keys():
            comment = {}
            comment['snippet'] = res['snippet']['topLevelComment']['snippet']
            comment['snippet']['parentId'] = None
            comment['snippet']['commentId'] = res['snippet']['topLevelComment']['id']
            comments.append(comment['snippet'])

    return comments
