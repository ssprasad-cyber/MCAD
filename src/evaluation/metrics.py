from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score
import numpy as np


def evaluate(labels, scores, threshold=0.5):
    """
    Compute classification metrics.

    Args:
        labels: list of int (0 or 1)
        scores: list of float anomaly scores in [0, 1]
        threshold: threshold to binarize scores for P/R/F1

    Returns:
        dict with roc_auc, precision, recall, f1
    """
    labels = np.array(labels)
    scores = np.array(scores)
    preds = (scores >= threshold).astype(int)

    # ROC-AUC needs both classes present; fall back gracefully
    if len(np.unique(labels)) < 2:
        roc_auc = float("nan")
    else:
        roc_auc = roc_auc_score(labels, scores)

    precision = precision_score(labels, preds, zero_division=0)
    recall    = recall_score(labels, preds, zero_division=0)
    f1        = f1_score(labels, preds, zero_division=0)

    return {
        "roc_auc":   round(float(roc_auc), 4),
        "precision": round(float(precision), 4),
        "recall":    round(float(recall), 4),
        "f1":        round(float(f1), 4)
    }
