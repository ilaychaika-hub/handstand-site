from flask import Flask, render_template, redirect, url_for
from datetime import date, timedelta, datetime
import json
import os

app = Flask(__name__)

PROGRESS_FILE = "progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_progress(data):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    print("🔄 Вхід у маршрут '/'")

    start_date = date(2025, 10, 11)
    end_date = date(2026, 1, 28)
    total_days = (end_date - start_date).days + 1

    print(f"📅 Генеруємо {total_days} днів тренувань")

    progress = load_progress()
    workouts = []
    level = 1

    # Вибір фону за днем тижня
    day_number = datetime.now().weekday()  # 0 = понеділок
    chosen_bg = f"images/background{day_number+1}.jpg"

    # Перевірка чи файл існує
    bg_path = os.path.join("static", chosen_bg)
    if not os.path.exists(bg_path):
        print(f"⚠️ Файл фону не знайдено: {bg_path}, використовую резервний")
        chosen_bg = "images/background1.jpg"
    else:
        print(f"🖼️ Використовується фон: {chosen_bg}")

    for i in range(total_days):
        day_date = start_date + timedelta(days=i)
        title = ""
        exercises = []

        if i % 7 == 0 and i != 0:
            level += 1

        mod = i % 4
        if mod == 0:
            title = "Баланс та стабільність"
            exercises = [
                {"name": "Стояння біля стіни", "time": f"{10 + level*3} сек", "sets": "3 підходи"},
                {"name": "Балансування без стіни", "time": f"{2 + level*1} сек", "sets": "2 спроби"},
            ]
        elif mod == 1:
            title = "Сила та витривалість"
            exercises = [
                {"name": "Віджимання у стійці біля стіни", "reps": f"{3 + level} повторень", "sets": "3 підходи"},
                {"name": "Планка на руках", "time": f"{20 + level*5} сек", "sets": "3 підходи"},
            ]
        elif mod == 2:
            title = "Контроль тіла"
            exercises = [
                {"name": "Переходи з ноги на ногу у стійці", "time": f"{10 + level*3} сек", "sets": "2 підходи"},
                {"name": "Підйоми у стійку з підлоги", "reps": f"{2 + level} рази", "sets": "3 підходи"},
            ]
        else:
            title = "Відновлення"
            exercises = [
                {"name": "Розтяжка плечей", "time": f"{60 + level*10} сек", "sets": "2 підходи"},
                {"name": "Дихальна практика", "time": "2 хв", "sets": "1 раз"},
            ]

        done = progress.get(day_date.strftime("%Y-%m-%d"), False)

        workouts.append({
            "date": day_date.strftime("%Y-%m-%d"),
            "title": title,
            "exercises": exercises,
            "done": done
        })

    print(f"📦 Передача шаблону з {len(workouts)} днями")
    return render_template("index.html", workouts=workouts, background=chosen_bg)

@app.route("/complete/<string:day>")
def complete(day):
    progress = load_progress()
    progress[day] = True
    save_progress(progress)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    app.run(debug=True)