# Annual Trip System – מערכת ניהול טיול שנתי

## תיאור
מערכת לניהול טיול שנתי של בית ספר. מאפשרת למורות לנהל תלמידות, לצפות במיקומן על מפה ולבדוק שאף תלמידה לא התרחקה מדי.

## טכנולוגיות
- **Backend:** Python + Flask
- **Database:** SQL Server
- **Frontend:** HTML + JavaScript
- **Maps:** Leaflet.js

## התקנה והרצה

### דרישות מוקדמות
- Python 3.x
- SQL Server + SSMS
- דפדפן מודרני

### הרצת השרת
1. היכנסי לתיקיית server
2. הפעילי סביבה וירטואלית: `venv\Scripts\activate`
3. התקיני תלויות: `pip install -r requirements.txt`
4. הריצי: `python app.py`

### הרצת הלקוח
1. פתחי את `client/index.html` בדפדפן

## אופן השימוש

### כניסה כמורה
- הכניסי תעודת זהות של מורה קיימת במערכת
- נהלי תלמידות ומורות דרך הלשוניות
- צפי במפה עם מיקומי התלמידות
- בדקי מרחקי תלמידות

### כניסה כהורה/תלמידה
- הכניסי תעודת זהות של תלמידה
- צפי במפה ובסטטוס התלמידה

### (Postman)
את כל הפונקציות שנכתבו ניתן לממש ב- POSTMAN

#### לדוגמא סימולציית מיקום (Postman)
שלחי POST ל-`/Locations` עם:
```json
{
    "ID": xxxxxxxxx,
    "Coordinates": {
        "Longitude": {"Degrees": "dd", "Minutes": "mm", "Seconds": "ss"},
        "Latitude": {"Degrees": "dd", "Minutes": "mm", "Seconds": "ss"}
    },
    "Time": "YYYY-MM-DDTHH:MM:SSZ"
}
```

## הנחות מקלות
- מיקום המכשירים מדומה דרך Postman במקום מכשירי איכון אמיתיים