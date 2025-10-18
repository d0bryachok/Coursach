from fastapi import FastAPI
import sqlite3
from datetime import date

app = FastAPI()

# Создаем базу данных и таблицы
conn = sqlite3.connect("fitness_tracker.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Workouts (
        workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        workout_type TEXT NOT NULL,
        duration_minutes INTEGER NOT NULL,
        calories_burned INTEGER,
        date DATE NOT NULL,
        notes TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Exercises (
        exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        muscle_group TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Progress (
        progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE NOT NULL,
        weight REAL,
        height REAL,
        body_fat_percentage REAL,
        muscle_mass REAL,
        notes TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS WorkoutExercises (
        workout_exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
        workout_id INTEGER,
        exercise_id INTEGER,
        sets INTEGER,
        reps INTEGER,
        weight_kg REAL,
        duration_seconds INTEGER
    )
''')

conn.commit()
conn.close()

# Тренировки
@app.post("/workouts/")
def create_workout(title: str, workout_type: str, duration_minutes: int, date: str, calories_burned: int = None, notes: str = ""):
    """Создание тренировки"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Workouts (title, workout_type, duration_minutes, calories_burned, date, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (title, workout_type, duration_minutes, calories_burned, date, notes)
        )
        conn.commit()
        workout_id = cursor.lastrowid
        return {"workout_id": workout_id, "message": "Тренировка создана"}
    except Exception as e:
        return {"error": f"Ошибка создания тренировки: {str(e)}"}
    finally:
        conn.close()

@app.get("/workouts/")
def get_workouts():
    """Получить все тренировки"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT workout_id, title, workout_type, duration_minutes, calories_burned, date, notes FROM Workouts ORDER BY date DESC")
    workouts = cursor.fetchall()
    conn.close()
    
    if not workouts:
        return {"error": "Список тренировок пуст"}
    
    return [{
        "workout_id": w[0], 
        "title": w[1], 
        "workout_type": w[2], 
        "duration_minutes": w[3], 
        "calories_burned": w[4], 
        "date": w[5], 
        "notes": w[6]
    } for w in workouts]

@app.put("/workouts/{workout_id}")
def update_workout(workout_id: int, title: str = None, workout_type: str = None, duration_minutes: int = None, calories_burned: int = None, date: str = None, notes: str = None):
    """Обновление тренировки"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    try:
        # Проверяем существование тренировки
        cursor.execute("SELECT * FROM Workouts WHERE workout_id = ?", (workout_id,))
        workout = cursor.fetchone()
        
        if not workout:
            return {"error": "Тренировка не найдена"}
        
        # Собираем поля для обновления
        update_fields = []
        update_values = []
        
        if title is not None:
            update_fields.append("title = ?")
            update_values.append(title)
        if workout_type is not None:
            update_fields.append("workout_type = ?")
            update_values.append(workout_type)
        if duration_minutes is not None:
            update_fields.append("duration_minutes = ?")
            update_values.append(duration_minutes)
        if calories_burned is not None:
            update_fields.append("calories_burned = ?")
            update_values.append(calories_burned)
        if date is not None:
            update_fields.append("date = ?")
            update_values.append(date)
        if notes is not None:
            update_fields.append("notes = ?")
            update_values.append(notes)
        
        if not update_fields:
            return {"error": "Нет данных для обновления"}
        
        update_values.append(workout_id)
        query = f"UPDATE Workouts SET {', '.join(update_fields)} WHERE workout_id = ?"
        
        cursor.execute(query, update_values)
        conn.commit()
        
        return {"message": "Тренировка обновлена"}
    except Exception as e:
        return {"error": f"Ошибка обновления тренировки: {str(e)}"}
    finally:
        conn.close()

# Упражнения
@app.post("/exercises/")
def create_exercise(name: str, description: str = "", muscle_group: str = ""):
    """Создание упражнения"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Exercises (name, description, muscle_group) VALUES (?, ?, ?)",
            (name, description, muscle_group)
        )
        conn.commit()
        exercise_id = cursor.lastrowid
        return {"exercise_id": exercise_id, "message": "Упражнение создано"}
    except:
        return {"error": "Такое упражнение уже существует"}
    finally:
        conn.close()

@app.get("/exercises/")
def get_exercises():
    """Получить все упражнения"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT exercise_id, name, description, muscle_group FROM Exercises")
    exercises = cursor.fetchall()
    conn.close()
    
    if not exercises:
        return {"error": "Список упражнений пуст"}
    
    return [{
        "exercise_id": e[0], 
        "name": e[1], 
        "description": e[2], 
        "muscle_group": e[3]
    } for e in exercises]

@app.put("/exercises/{exercise_id}")
def update_exercise(exercise_id: int, name: str = None, description: str = None, muscle_group: str = None):
    """Обновление упражнения"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    try:
        # Проверяем существование упражнения
        cursor.execute("SELECT * FROM Exercises WHERE exercise_id = ?", (exercise_id,))
        exercise = cursor.fetchone()
        
        if not exercise:
            return {"error": "Упражнение не найдено"}
        
        # Собираем поля для обновления
        update_fields = []
        update_values = []
        
        if name is not None:
            update_fields.append("name = ?")
            update_values.append(name)
        if description is not None:
            update_fields.append("description = ?")
            update_values.append(description)
        if muscle_group is not None:
            update_fields.append("muscle_group = ?")
            update_values.append(muscle_group)
        
        if not update_fields:
            return {"error": "Нет данных для обновления"}
        
        update_values.append(exercise_id)
        query = f"UPDATE Exercises SET {', '.join(update_fields)} WHERE exercise_id = ?"
        
        cursor.execute(query, update_values)
        conn.commit()
        
        return {"message": "Упражнение обновлено"}
    except Exception as e:
        return {"error": f"Ошибка обновления упражнения: {str(e)}"}
    finally:
        conn.close()

# Прогресс
@app.post("/progress/")
def create_progress(date: str, weight: float = None, height: float = None, body_fat_percentage: float = None, muscle_mass: float = None, notes: str = ""):
    """Создание записи прогресса"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO Progress (date, weight, height, body_fat_percentage, muscle_mass, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (date, weight, height, body_fat_percentage, muscle_mass, notes)
        )
        conn.commit()
        progress_id = cursor.lastrowid
        return {"progress_id": progress_id, "message": "Запись прогресса создана"}
    except Exception as e:
        return {"error": f"Ошибка создания записи прогресса: {str(e)}"}
    finally:
        conn.close()

@app.get("/progress/")
def get_progress():
    """Получить все записи прогресса"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT progress_id, date, weight, height, body_fat_percentage, muscle_mass, notes FROM Progress ORDER BY date DESC")
    progress_entries = cursor.fetchall()
    conn.close()
    
    if not progress_entries:
        return {"error": "Список записей прогресса пуст"}
    
    return [{
        "progress_id": p[0], 
        "date": p[1], 
        "weight": p[2], 
        "height": p[3], 
        "body_fat_percentage": p[4], 
        "muscle_mass": p[5], 
        "notes": p[6]
    } for p in progress_entries]

@app.put("/progress/{progress_id}")
def update_progress(progress_id: int, date: str = None, weight: float = None, height: float = None, body_fat_percentage: float = None, muscle_mass: float = None, notes: str = None):
    """Обновление записи прогресса"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    try:
        # Проверяем существование записи прогресса
        cursor.execute("SELECT * FROM Progress WHERE progress_id = ?", (progress_id,))
        progress = cursor.fetchone()
        
        if not progress:
            return {"error": "Запись прогресса не найдена"}
        
        # Собираем поля для обновления
        update_fields = []
        update_values = []
        
        if date is not None:
            update_fields.append("date = ?")
            update_values.append(date)
        if weight is not None:
            update_fields.append("weight = ?")
            update_values.append(weight)
        if height is not None:
            update_fields.append("height = ?")
            update_values.append(height)
        if body_fat_percentage is not None:
            update_fields.append("body_fat_percentage = ?")
            update_values.append(body_fat_percentage)
        if muscle_mass is not None:
            update_fields.append("muscle_mass = ?")
            update_values.append(muscle_mass)
        if notes is not None:
            update_fields.append("notes = ?")
            update_values.append(notes)
        
        if not update_fields:
            return {"error": "Нет данных для обновления"}
        
        update_values.append(progress_id)
        query = f"UPDATE Progress SET {', '.join(update_fields)} WHERE progress_id = ?"
        
        cursor.execute(query, update_values)
        conn.commit()
        
        return {"message": "Запись прогресса обновлена"}
    except Exception as e:
        return {"error": f"Ошибка обновления записи прогресса: {str(e)}"}
    finally:
        conn.close()

# Упражнения в тренировках
@app.post("/workout-exercises/")
def create_workout_exercise(workout_id: int, exercise_id: int, sets: int = None, reps: int = None, weight_kg: float = None, duration_seconds: int = None):
    """Добавление упражнения в тренировку"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    try:
        # Проверяем существование тренировки и упражнения
        cursor.execute("SELECT 1 FROM Workouts WHERE workout_id = ?", (workout_id,))
        workout = cursor.fetchone()
        
        cursor.execute("SELECT 1 FROM Exercises WHERE exercise_id = ?", (exercise_id,))
        exercise = cursor.fetchone()
        
        if not workout or not exercise:
            return {"error": "Тренировка или упражнение не найдены"}
        
        cursor.execute(
            "INSERT INTO WorkoutExercises (workout_id, exercise_id, sets, reps, weight_kg, duration_seconds) VALUES (?, ?, ?, ?, ?, ?)",
            (workout_id, exercise_id, sets, reps, weight_kg, duration_seconds)
        )
        
        conn.commit()
        workout_exercise_id = cursor.lastrowid
        return {"workout_exercise_id": workout_exercise_id, "message": "Упражнение добавлено в тренировку"}
    except Exception as e:
        return {"error": f"Ошибка добавления упражнения: {str(e)}"}
    finally:
        conn.close()

@app.get("/workout-exercises/{workout_id}")
def get_workout_exercises(workout_id: int):
    """Получить все упражнения для конкретной тренировки"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT we.workout_exercise_id, e.name, e.muscle_group, we.sets, we.reps, we.weight_kg, we.duration_seconds
        FROM WorkoutExercises we
        JOIN Exercises e ON we.exercise_id = e.exercise_id
        WHERE we.workout_id = ?
    ''', (workout_id,))
    exercises = cursor.fetchall()
    conn.close()
    
    if not exercises:
        return {"error": "В этой тренировке нет упражнений"}
    
    return [{
        "workout_exercise_id": e[0],
        "exercise_name": e[1],
        "muscle_group": e[2],
        "sets": e[3],
        "reps": e[4],
        "weight_kg": e[5],
        "duration_seconds": e[6]
    } for e in exercises]

@app.put("/workout-exercises/{workout_exercise_id}")
def update_workout_exercise(workout_exercise_id: int, sets: int = None, reps: int = None, weight_kg: float = None, duration_seconds: int = None):
    """Обновление упражнения в тренировке"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    try:
        # Проверяем существование записи
        cursor.execute("SELECT * FROM WorkoutExercises WHERE workout_exercise_id = ?", (workout_exercise_id,))
        workout_exercise = cursor.fetchone()
        
        if not workout_exercise:
            return {"error": "Запись упражнения в тренировке не найдена"}
        
        # Собираем поля для обновления
        update_fields = []
        update_values = []
        
        if sets is not None:
            update_fields.append("sets = ?")
            update_values.append(sets)
        if reps is not None:
            update_fields.append("reps = ?")
            update_values.append(reps)
        if weight_kg is not None:
            update_fields.append("weight_kg = ?")
            update_values.append(weight_kg)
        if duration_seconds is not None:
            update_fields.append("duration_seconds = ?")
            update_values.append(duration_seconds)
        
        if not update_fields:
            return {"error": "Нет данных для обновления"}
        
        update_values.append(workout_exercise_id)
        query = f"UPDATE WorkoutExercises SET {', '.join(update_fields)} WHERE workout_exercise_id = ?"
        
        cursor.execute(query, update_values)
        conn.commit()
        
        return {"message": "Упражнение в тренировке обновлено"}
    except Exception as e:
        return {"error": f"Ошибка обновления упражнения в тренировке: {str(e)}"}
    finally:
        conn.close()

# Статистика
@app.get("/stats/workouts")
def get_workout_stats():
    """Получить статистику по тренировкам"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    
    # Общее количество тренировок
    cursor.execute("SELECT COUNT(*) FROM Workouts")
    total_workouts = cursor.fetchone()[0]
    
    # Общее время тренировок (минуты)
    cursor.execute("SELECT SUM(duration_minutes) FROM Workouts")
    total_minutes = cursor.fetchone()[0] or 0
    
    # Общее количество сожженных калорий
    cursor.execute("SELECT SUM(calories_burned) FROM Workouts WHERE calories_burned IS NOT NULL")
    total_calories = cursor.fetchone()[0] or 0
    
    # Количество тренировок по типам
    cursor.execute("SELECT workout_type, COUNT(*) FROM Workouts GROUP BY workout_type")
    workouts_by_type = cursor.fetchall()
    
    conn.close()
    
    return {
        "total_workouts": total_workouts,
        "total_minutes": total_minutes,
        "total_calories": total_calories,
        "workouts_by_type": [{"type": w[0], "count": w[1]} for w in workouts_by_type]
    }

@app.get("/stats/progress")
def get_progress_stats():
    """Получить статистику прогресса"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    
    # Последние записи веса
    cursor.execute("SELECT date, weight FROM Progress WHERE weight IS NOT NULL ORDER BY date DESC LIMIT 10")
    weight_history = cursor.fetchall()
    
    # Последние записи мышечной массы
    cursor.execute("SELECT date, muscle_mass FROM Progress WHERE muscle_mass IS NOT NULL ORDER BY date DESC LIMIT 10")
    muscle_history = cursor.fetchall()
    
    conn.close()
    
    return {
        "weight_history": [{"date": w[0], "weight": w[1]} for w in weight_history],
        "muscle_mass_history": [{"date": m[0], "muscle_mass": m[1]} for m in muscle_history]
    }

# Удаление тренировки
@app.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int):
    """Удаление тренировки"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    try:
        # Сначала удаляем связанные упражнения
        cursor.execute("DELETE FROM WorkoutExercises WHERE workout_id = ?", (workout_id,))
        
        # Затем удаляем саму тренировку
        cursor.execute("DELETE FROM Workouts WHERE workout_id = ?", (workout_id,))
        
        conn.commit()
        return {"message": "Тренировка удалена"}
    except Exception as e:
        return {"error": f"Ошибка удаления тренировки: {str(e)}"}
    finally:
        conn.close()

# Удаление упражнения
@app.delete("/exercises/{exercise_id}")
def delete_exercise(exercise_id: int):
    """Удаление упражнения"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    try:
        # Сначала удаляем связанные записи в тренировках
        cursor.execute("DELETE FROM WorkoutExercises WHERE exercise_id = ?", (exercise_id,))
        
        # Затем удаляем само упражнение
        cursor.execute("DELETE FROM Exercises WHERE exercise_id = ?", (exercise_id,))
        
        conn.commit()
        return {"message": "Упражнение удалено"}
    except Exception as e:
        return {"error": f"Ошибка удаления упражнения: {str(e)}"}
    finally:
        conn.close()

# Удаление записи прогресса
@app.delete("/progress/{progress_id}")
def delete_progress(progress_id: int):
    """Удаление записи прогресса"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Progress WHERE progress_id = ?", (progress_id,))
        conn.commit()
        return {"message": "Запись прогресса удалена"}
    except Exception as e:
        return {"error": f"Ошибка удаления записи прогресса: {str(e)}"}
    finally:
        conn.close()

# Удаление упражнения из тренировки
@app.delete("/workout-exercises/{workout_exercise_id}")
def delete_workout_exercise(workout_exercise_id: int):
    """Удаление упражнения из тренировки"""
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM WorkoutExercises WHERE workout_exercise_id = ?", (workout_exercise_id,))
        conn.commit()
        return {"message": "Упражнение удалено из тренировки"}
    except Exception as e:
        return {"error": f"Ошибка удаления упражнения из тренировки: {str(e)}"}
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)