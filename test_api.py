import requests
from datetime import date, timedelta
import json

BASE_URL = "http://127.0.0.1:8000"


def test_get_all_workouts():
    """Получение всех тренировок"""
    response = requests.get(f"{BASE_URL}/workouts/")
    print("GET Workouts Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())
    return response

def test_create_workout(workout_data):
    """Создание тренировки"""
    response = requests.post(f"{BASE_URL}/workouts/", json=workout_data)
    print("POST Workout Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())
    if response.status_code == 200:
        return response.json().get('workout_id')
    return None

def test_update_workout(workout_id, update_data):
    """Обновление тренировки"""
    response = requests.put(f"{BASE_URL}/workouts/{workout_id}", json=update_data)
    print("PUT Workout Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_delete_workout(workout_id):
    """Удаление тренировки"""
    response = requests.delete(f"{BASE_URL}/workouts/{workout_id}")
    print("DELETE Workout Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())


def test_get_all_exercises():
    """Получение всех упражнений"""
    response = requests.get(f"{BASE_URL}/exercises/")
    print("GET Exercises Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_create_exercise(exercise_data):
    """Создание упражнения"""
    response = requests.post(f"{BASE_URL}/exercises/", json=exercise_data)
    print("POST Exercise Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())
    if response.status_code == 200:
        return response.json().get('exercise_id')
    return None

def test_update_exercise(exercise_id, update_data):
    """Обновление упражнения"""
    response = requests.put(f"{BASE_URL}/exercises/{exercise_id}", json=update_data)
    print("PUT Exercise Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_delete_exercise(exercise_id):
    """Удаление упражнения"""
    response = requests.delete(f"{BASE_URL}/exercises/{exercise_id}")
    print("DELETE Exercise Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())


def test_get_all_progress():
    """Получение всех записей прогресса"""
    response = requests.get(f"{BASE_URL}/progress/")
    print("GET Progress Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_create_progress(progress_data):
    """Создание записи прогресса"""
    response = requests.post(f"{BASE_URL}/progress/", json=progress_data)
    print("POST Progress Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())
    if response.status_code == 200:
        return response.json().get('progress_id')
    return None

def test_update_progress(progress_id, update_data):
    """Обновление записи прогресса"""
    response = requests.put(f"{BASE_URL}/progress/{progress_id}", json=update_data)
    print("PUT Progress Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_delete_progress(progress_id):
    """Удаление записи прогресса"""
    response = requests.delete(f"{BASE_URL}/progress/{progress_id}")
    print("DELETE Progress Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())


def test_create_workout_exercise(workout_exercise_data):
    """Добавление упражнения в тренировку"""
    response = requests.post(f"{BASE_URL}/workout-exercises/", json=workout_exercise_data)
    print("POST Workout Exercise Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())
    if response.status_code == 200:
        return response.json().get('workout_exercise_id')
    return None

def test_get_workout_exercises(workout_id):
    """Получение упражнений для тренировки"""
    response = requests.get(f"{BASE_URL}/workout-exercises/{workout_id}")
    print("GET Workout Exercises Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_update_workout_exercise(workout_exercise_id, update_data):
    """Обновление упражнения в тренировке"""
    response = requests.put(f"{BASE_URL}/workout-exercises/{workout_exercise_id}", json=update_data)
    print("PUT Workout Exercise Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_delete_workout_exercise(workout_exercise_id):
    """Удаление упражнения из тренировки"""
    response = requests.delete(f"{BASE_URL}/workout-exercises/{workout_exercise_id}")
    print("DELETE Workout Exercise Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())


def test_get_workout_stats():
    """Получение статистики тренировок"""
    response = requests.get(f"{BASE_URL}/stats/workouts")
    print("GET Workout Stats Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())

def test_get_progress_stats():
    """Получение статистики прогресса"""
    response = requests.get(f"{BASE_URL}/stats/progress")
    print("GET Progress Stats Status Code:")
    print(response.status_code)
    print("Вывод тела запроса:")
    print(response.json())


def main():
    
    print("1. ТЕСТЫ ТРЕНИРОВОК")
    print("-" * 50)
    
    # Получение всех тренировок
    test_get_all_workouts()
    
    # Создание тестовой тренировки
    test_workout = {
        "title": "Утренняя кардио тренировка",
        "workout_type": "cardio",
        "duration_minutes": 45,
        "calories_burned": 350,
        "date": str(date.today()),
        "notes": "Хорошая интенсивность"
    }
    workout_id = test_create_workout(test_workout)
    
    # Получение всех тренировок после создания
    test_get_all_workouts()
    
    if workout_id:
        # Обновление тренировки
        workout_update = {
            "duration_minutes": 50,
            "calories_burned": 400,
            "notes": "Обновленная заметка"
        }
        test_update_workout(workout_id, workout_update)
    
    print("\n2. ТЕСТЫ УПРАЖНЕНИЙ")
    print("-" * 50)
    
    # Получение всех упражнений
    test_get_all_exercises()
    
    # Создание тестового упражнения
    test_exercise = {
        "name": "Приседания",
        "description": "Базовое упражнение для ног",
        "muscle_group": "Ноги"
    }
    exercise_id = test_create_exercise(test_exercise)
    
    # Получение всех упражнений после создания
    test_get_all_exercises()
    
    if exercise_id:
        # Обновление упражнения
        exercise_update = {
            "description": "Базовое упражнение для развития мышц ног и ягодиц",
            "muscle_group": "Ноги, Ягодицы"
        }
        test_update_exercise(exercise_id, exercise_update)
    
    print("\n3. ТЕСТЫ ПРОГРЕССА")
    print("-" * 50)
    
    # Получение всех записей прогресса
    test_get_all_progress()
    
    # Создание тестовой записи прогресса
    test_progress = {
        "date": str(date.today()),
        "weight": 75.5,
        "height": 180.0,
        "body_fat_percentage": 15.2,
        "muscle_mass": 65.0,
        "notes": "Хороший прогресс"
    }
    progress_id = test_create_progress(test_progress)
    
    # Получение всех записей прогресса после создания
    test_get_all_progress()
    
    if progress_id:
        # Обновление записи прогресса
        progress_update = {
            "weight": 75.0,
            "body_fat_percentage": 14.8,
            "notes": "Отличные результаты!"
        }
        test_update_progress(progress_id, progress_update)
    
    print("\n4. ТЕСТЫ УПРАЖНЕНИЙ В ТРЕНИРОВКАХ")
    print("-" * 50)
    
    workout_exercise_id = None
    if workout_id and exercise_id:
        # Добавление упражнения в тренировку
        test_workout_exercise = {
            "workout_id": workout_id,
            "exercise_id": exercise_id,
            "sets": 3,
            "reps": 12,
            "weight_kg": 60.0
        }
        workout_exercise_id = test_create_workout_exercise(test_workout_exercise)
        
        # Получение упражнений для тренировки
        test_get_workout_exercises(workout_id)
        
        if workout_exercise_id:
            # Обновление упражнения в тренировке
            workout_exercise_update = {
                "sets": 4,
                "reps": 10,
                "weight_kg": 65.0
            }
            test_update_workout_exercise(workout_exercise_id, workout_exercise_update)
    
    print("\n5. ТЕСТЫ СТАТИСТИКИ")
    print("-" * 50)
    
    # Статистика тренировок
    test_get_workout_stats()
    
    # Статистика прогресса
    test_get_progress_stats()
    
    print("\n6. ТЕСТЫ УДАЛЕНИЯ")
    print("-" * 50)
    
    # Удаление в правильном порядке (сначала зависимые сущности)
    if workout_exercise_id:
        test_delete_workout_exercise(workout_exercise_id)
    
    if progress_id:
        test_delete_progress(progress_id)
    
    if exercise_id:
        test_delete_exercise(exercise_id)
    
    if workout_id:
        test_delete_workout(workout_id)
    
    # Финальная проверка всех данных
    print("\n7. ФИНАЛЬНАЯ ПРОВЕРКА ДАННЫХ")
    print("-" * 50)
    
    test_get_all_workouts()
    test_get_all_exercises()
    test_get_all_progress()
    test_get_workout_stats()

if __name__ == "__main__":
    main()