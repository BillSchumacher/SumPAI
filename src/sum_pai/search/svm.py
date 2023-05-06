import numpy as np
from sklearn import svm


def svm_search(embeddings, query) -> np.ndarray:
    """Performs a search using SVMs."""
    embeds = len(embeddings)
    x = np.concatenate([query[None, ...], embeddings])
    # x is (1001, 1536) array, with query now as the first row
    y = np.zeros(embeds + 1)
    y[0] = 1  # we have a single positive example, mark it as such

    # train our (Exemplar) SVM
    # docs: https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html
    clf = svm.LinearSVC(
        class_weight="balanced", verbose=False, max_iter=100000, tol=1e-6, C=0.1
    )
    clf.fit(x, y)  # train

    # infer on whatever data you wish, e.g. the original data
    similarities = clf.decision_function(x[1:])
    return np.argsort(-similarities)
