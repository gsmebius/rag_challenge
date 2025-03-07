from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..utils.logging_config import setup_logging

setup_logging()

def evaluate_response_quality(query, response, context):
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform([query, response])
        relevance_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except:
        relevance_score = 0.0

    context_words = set(' '.join(context).lower().split())
    response_words = set(response.lower().split())
    context_usage = len(context_words.intersection(response_words)) / len(context_words) if context_words else 0

    response_length = len(response.split())
    length_score = min(1.0, response_length / 50)

    overall_score = (relevance_score + context_usage + length_score) / 3

    evaluation = {
        # roun score * 100, use 2 decimals
        "overall_score": round(overall_score * 100, 2),
        "relevance_score": round(relevance_score * 100, 2),
        "context_usage": round(context_usage * 100, 2),
        "length_score": round(length_score * 100, 2),
        "response_length": response_length,
        "feedback": []
    }

    # Relevance feedback
    if relevance_score >= 0.8:
        evaluation["feedback"].append("Excellent relevance to the question. The answer directly addresses the query.")
    elif relevance_score >= 0.6:
        evaluation["feedback"].append("Good relevance to the question. The answer mostly addresses the query.")
    elif relevance_score >= 0.4:
        evaluation["feedback"].append("Moderate relevance to the question. Some aspects could be better aligned.")
    else:
        evaluation["feedback"].append("The answer could be more focused on addressing the specific question.")

    # Context usage feedback
    if context_usage >= 0.8:
        evaluation["feedback"].append("Excellent use of context information. The answer effectively incorporates provided details.")
    elif context_usage >= 0.6:
        evaluation["feedback"].append("Good use of context information. The answer makes good use of provided details.")
    elif context_usage >= 0.4:
        evaluation["feedback"].append("Moderate use of context information. Could better utilize provided details.")
    else:
        evaluation["feedback"].append("The answer could make better use of the provided context information.")

    # Length feedback
    if length_score >= 0.8:
        evaluation["feedback"].append("Comprehensive answer with appropriate length and detail.")
    elif length_score >= 0.6:
        evaluation["feedback"].append("Good length with sufficient detail to address the question.")
    elif length_score >= 0.4:
        evaluation["feedback"].append("Answer could benefit from more detail and elaboration.")
    else:
        evaluation["feedback"].append("The answer is quite brief and could use more detailed explanation.")

    # Overall performance feedback
    if overall_score >= 0.8:
        evaluation["feedback"].append("Overall excellent response that effectively addresses the question.")
    elif overall_score >= 0.6:
        evaluation["feedback"].append("Overall good response with room for minor improvements.")
    elif overall_score >= 0.4:
        evaluation["feedback"].append("Overall moderate response that could benefit from several improvements.")
    else:
        evaluation["feedback"].append("The response needs significant improvement to better address the question.")

    return evaluation