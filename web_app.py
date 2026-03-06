from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from my_bot import start_spam_attack, is_valid_israeli_phone
import threading

# התקנת הספרייה הנדרשת:
# pip install Flask requests

# יצירת אפליקציית ווב
app = Flask(__name__, template_folder='.')
app.secret_key = "RONEN-SECRET-KEY-SESSION" # נדרש עבור הודעות Flash

# הגדרת מפתח אבטחה פשוט. בשימוש אמיתי, יש להשתמש במנגנון חזק יותר.
API_KEY = "RONEN-SPAM-2026"

@app.route('/', methods=['GET'])
def index():
    """מציג את דף הבית (index.html)."""
    return render_template('index.html')

@app.route('/spam', methods=['GET', 'POST'])
def handle_spam_request():
    """
    מטפל בבקשות ווב להתחלת תקיפה.
    תומך גם ב-API (GET) וגם בטופס מהאתר (POST).
    דורש את הפרמטרים הבאים בכתובת ה-URL:
    - phone: מספר הטלפון לתקיפה.
    - waves: מספר הגלים (אופציונלי, ברירת מחדל 1).
    - api_key: מפתח האבטחה שהוגדר למעלה.
    """
    
    # --- טיפול בבקשות מהטופס (POST) ---
    if request.method == 'POST':
        phone_number = request.form.get('phone')
        try:
            waves = int(request.form.get('waves', 1))
        except ValueError:
            flash("מספר גלים לא תקין", "error")
            return redirect(url_for('index'))

        if not phone_number or not is_valid_israeli_phone(phone_number):
            flash("מספר טלפון לא תקין או חסר", "error")
            return redirect(url_for('index'))

        # התחלת התקיפה
        thread = threading.Thread(target=start_spam_attack, args=(phone_number, waves))
        thread.start()

        flash(f"המתקפה נשלחה בהצלחה ל-{phone_number} ({waves} גלים)", "success")
        return redirect(url_for('index'))

    # --- טיפול בבקשות API (GET) ---
    # --- בדיקת אבטחה ---
    provided_key = request.args.get('api_key')
    if provided_key != API_KEY:
        return jsonify({"error": "Unauthorized access"}), 401

    # --- קבלת פרמטרים ---
    phone_number = request.args.get('phone')
    try:
        waves = int(request.args.get('waves', 1))
    except ValueError:
        return jsonify({"error": "Invalid 'waves' parameter. Must be a number."}), 400

    # --- ולידציה ---
    if not phone_number or not is_valid_israeli_phone(phone_number):
        return jsonify({"error": "Invalid or missing 'phone' parameter."}), 400

    # --- התחלת התקיפה ב-Thread נפרד ---
    # זה מאפשר לשרת להחזיר תשובה מיידית בזמן שהתקיפה רצה ברקע.
    thread = threading.Thread(target=start_spam_attack, args=(phone_number, waves))
    thread.start()

    # החזרת תשובה מיידית למשתמש
    return jsonify({
        "message": "Spam attack initiated in the background. Check the console for progress.",
        "target": phone_number,
        "waves": waves
    })

if __name__ == '__main__':
    # הרצת השרת. הוא יהיה זמין בכתובת של המחשב שלך בפורט 5000.
    app.run(host='0.0.0.0', port=5000, debug=False)