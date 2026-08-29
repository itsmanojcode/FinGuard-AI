from backend.safety.policy import evaluate_action
def test_small(): assert evaluate_action(500,"x")["status"]=="ALLOWED"
def test_medium(): assert evaluate_action(2000,"x")["status"]=="APPROVAL_REQUIRED"
def test_large(): assert evaluate_action(10000,"x")["status"]=="BLOCKED"
