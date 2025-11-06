from functools import reduce


def calculate_title_rating(reviews):
    if reviews == []:
        return 0.0
    rating = reduce(lambda acc, review: acc + review['score'], reviews, 0)
    return rating / len(reviews)
