from backend.analytics.metrics import classification_metrics
def test_metrics():
    m=classification_metrics([1,1,0,0],[1,0,0,0])
    assert 0 <= m["precision"] <= 1
    assert 0 <= m["recall"] <= 1
