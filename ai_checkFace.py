#import os 
#os.system ("pip install tf-keras")

from deepface import DeepFace

# ניתוח תמונה לדוגמה
try:
    # נשתמש בתמונה לדוגמה מהספרייה
    obj = DeepFace.analyze(img_path = "https://raw.githubusercontent.com/serengil/deepface/master/tests/dataset/img1.jpg", actions = ['age', 'gender', 'race', 'emotion'])
    print("הניתוח הצליח! הנה התוצאה:")
    print(obj)
except Exception as e:
    print(f"שגיאה התרחשה: {e}")
