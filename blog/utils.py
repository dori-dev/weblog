from difflib import SequenceMatcher
from django.contrib.postgres.search import TrigramWordSimilarity
from .models import Post


def get_most_similar_word(query: str):
    similar: Post = Post.published.annotate(
        title_similarity=TrigramWordSimilarity(query, 'title'),
        body_similarity=TrigramWordSimilarity(query, 'body'),
    ).order_by('-body_similarity', '-title_similarity').first()
    all_word_in_post = f"{similar.title} {similar.body}".split()
    similar_ratio = dict(map(
        lambda word: (
            word,
            SequenceMatcher(None, word, query).ratio()
        ),
        all_word_in_post
    ))
    return max(similar_ratio.keys(),
               key=lambda word: similar_ratio[word])
