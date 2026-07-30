from utils.text_prediction import predict_text_emotion

text = input("Enter Text : ")

svc, rf, xgb, final = predict_text_emotion(text)

print()

print("SVC   :", svc)
print("RF    :", rf)
print("XGB   :", xgb)
print("---------------------")
print("FINAL :", final)