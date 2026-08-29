def classification_metrics(y_true, y_pred):
    tp=sum(a==1 and b==1 for a,b in zip(y_true,y_pred))
    tn=sum(a==0 and b==0 for a,b in zip(y_true,y_pred))
    fp=sum(a==0 and b==1 for a,b in zip(y_true,y_pred))
    fn=sum(a==1 and b==0 for a,b in zip(y_true,y_pred))
    precision=tp/(tp+fp) if tp+fp else 0
    recall=tp/(tp+fn) if tp+fn else 0
    f1=2*precision*recall/(precision+recall) if precision+recall else 0
    fpr=fp/(fp+tn) if fp+tn else 0
    return {"precision":round(precision,4),"recall":round(recall,4),
            "f1":round(f1,4),"false_positive_rate":round(fpr,4)}
