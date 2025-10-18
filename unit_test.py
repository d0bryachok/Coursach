import unittest
import requests
import time
from datetime import date, timedelta


class TestFitnessTrackerAPI(unittest.TestCase):
    BASE_URL = "http://localhost:8000"
    
    def setUp(self):
        self.timestamp = int(time.time())
        self.created_ids = {
            'workouts': [],
            'exercises': [],
            'progress': [],
            'workout_exercises': []
        }

    def tearDown(self):
        # Очистка созданных данных после каждого теста
        for workout_exercise_id in self.created_ids['workout_exercises']:
            try:
                requests.delete(f"{self.BASE_URL}/workout-exercises/{workout_exercise_id}")
            except:
                pass
        
        for progress_id in self.created_ids['progress']:
            try:
                requests.delete(f"{self.BASE_URL}/progress/{progress_id}")
            except:
                pass
        
        for exercise_id in self.created_ids['exercises']:
            try:
                requests.delete(f"{self.BASE_URL}/exercises/{exercise_id}")
            except:
                pass
        
        for workout_id in self.created_ids['workouts']:
            try:
                requests.delete(f"{self.BASE_URL}/workouts/{workout_id}")
            except:
                pass

    def test_01_get_workouts(self):
        """Тест получения всех тренировок"""
        response = requests.get(f"{self.BASE_URL}/workouts/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), (list, dict))

    def test_02_create_workout(self):
        """Тест создания тренировки"""
        data = {
            'title': f'Workout {self.timestamp}',
            'workout_type': 'cardio',
            'duration_minutes': 45,
            'calories_burned': 350,
            'date': str(date.today()),
            'notes': f'Test workout {self.timestamp}'
        }
        response = requests.post(f"{self.BASE_URL}/workouts/", params=data)
        self.assertEqual(response.status_code, 200)
        workout_id = response.json().get('workout_id')
        if workout_id:
            self.created_ids['workouts'].append(workout_id)

    def test_03_update_workout(self):
        """Тест обновления тренировки"""
        # Сначала создаем тренировку
        create_data = {
            'title': f'Workout to update {self.timestamp}',
            'workout_type': 'strength',
            'duration_minutes': 30,
            'date': str(date.today()),
            'notes': 'Original notes'
        }
        create_response = requests.post(f"{self.BASE_URL}/workouts/", params=create_data)
        self.assertEqual(create_response.status_code, 200)
        workout_id = create_response.json().get('workout_id')
        
        if workout_id:
            self.created_ids['workouts'].append(workout_id)
            
            # Обновляем тренировку
            update_data = {
                'duration_minutes': 40,
                'calories_burned': 300,
                'notes': f'Updated notes {self.timestamp}'
            }
            update_response = requests.put(f"{self.BASE_URL}/workouts/{workout_id}", params=update_data)
            self.assertEqual(update_response.status_code, 200)

    def test_04_get_exercises(self):
        """Тест получения всех упражнений"""
        response = requests.get(f"{self.BASE_URL}/exercises/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), (list, dict))

    def test_05_create_exercise(self):
        """Тест создания упражнения"""
        data = {
            'name': f'Exercise {self.timestamp}',
            'description': f'Test exercise description {self.timestamp}',
            'muscle_group': 'Legs'
        }
        response = requests.post(f"{self.BASE_URL}/exercises/", params=data)
        self.assertEqual(response.status_code, 200)
        exercise_id = response.json().get('exercise_id')
        if exercise_id:
            self.created_ids['exercises'].append(exercise_id)

    def test_06_update_exercise(self):
        """Тест обновления упражнения"""
        # Сначала создаем упражнение
        create_data = {
            'name': f'Exercise to update {self.timestamp}',
            'description': 'Original description',
            'muscle_group': 'Arms'
        }
        create_response = requests.post(f"{self.BASE_URL}/exercises/", params=create_data)
        self.assertEqual(create_response.status_code, 200)
        exercise_id = create_response.json().get('exercise_id')
        
        if exercise_id:
            self.created_ids['exercises'].append(exercise_id)
            
            # Обновляем упражнение
            update_data = {
                'description': f'Updated description {self.timestamp}',
                'muscle_group': 'Arms, Shoulders'
            }
            update_response = requests.put(f"{self.BASE_URL}/exercises/{exercise_id}", params=update_data)
            self.assertEqual(update_response.status_code, 200)

    def test_07_get_progress(self):
        """Тест получения всех записей прогресса"""
        response = requests.get(f"{self.BASE_URL}/progress/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), (list, dict))

    def test_08_create_progress(self):
        """Тест создания записи прогресса"""
        data = {
            'date': str(date.today()),
            'weight': 75.5 + (self.timestamp % 10) / 10,  # Разные значения для разных тестов
            'height': 180.0,
            'body_fat_percentage': 15.2,
            'muscle_mass': 65.0,
            'notes': f'Test progress {self.timestamp}'
        }
        response = requests.post(f"{self.BASE_URL}/progress/", params=data)
        self.assertEqual(response.status_code, 200)
        progress_id = response.json().get('progress_id')
        if progress_id:
            self.created_ids['progress'].append(progress_id)

    def test_09_update_progress(self):
        """Тест обновления записи прогресса"""
        # Сначала создаем запись прогресса
        create_data = {
            'date': str(date.today()),
            'weight': 76.0,
            'notes': 'Original progress'
        }
        create_response = requests.post(f"{self.BASE_URL}/progress/", params=create_data)
        self.assertEqual(create_response.status_code, 200)
        progress_id = create_response.json().get('progress_id')
        
        if progress_id:
            self.created_ids['progress'].append(progress_id)
            
            # Обновляем запись прогресса
            update_data = {
                'weight': 75.0,
                'body_fat_percentage': 14.8,
                'notes': f'Updated progress {self.timestamp}'
            }
            update_response = requests.put(f"{self.BASE_URL}/progress/{progress_id}", params=update_data)
            self.assertEqual(update_response.status_code, 200)

    def test_10_create_workout_exercise(self):
        """Тест добавления упражнения в тренировку"""
        # Сначала создаем тренировку и упражнение
        workout_data = {
            'title': f'Workout for exercise {self.timestamp}',
            'workout_type': 'strength',
            'duration_minutes': 60,
            'date': str(date.today())
        }
        workout_response = requests.post(f"{self.BASE_URL}/workouts/", params=workout_data)
        workout_id = workout_response.json().get('workout_id')
        
        exercise_data = {
            'name': f'Exercise for workout {self.timestamp}',
            'muscle_group': 'Chest'
        }
        exercise_response = requests.post(f"{self.BASE_URL}/exercises/", params=exercise_data)
        exercise_id = exercise_response.json().get('exercise_id')
        
        if workout_id and exercise_id:
            self.created_ids['workouts'].append(workout_id)
            self.created_ids['exercises'].append(exercise_id)
            
            # Добавляем упражнение в тренировку
            workout_exercise_data = {
                'workout_id': workout_id,
                'exercise_id': exercise_id,
                'sets': 3,
                'reps': 10,
                'weight_kg': 50.0
            }
            response = requests.post(f"{self.BASE_URL}/workout-exercises/", params=workout_exercise_data)
            self.assertEqual(response.status_code, 200)
            workout_exercise_id = response.json().get('workout_exercise_id')
            if workout_exercise_id:
                self.created_ids['workout_exercises'].append(workout_exercise_id)

    def test_11_get_workout_exercises(self):
        """Тест получения упражнений для тренировки"""
        # Сначала создаем тренировку с упражнением
        workout_data = {
            'title': f'Workout for get exercises {self.timestamp}',
            'workout_type': 'strength',
            'duration_minutes': 45,
            'date': str(date.today())
        }
        workout_response = requests.post(f"{self.BASE_URL}/workouts/", params=workout_data)
        workout_id = workout_response.json().get('workout_id')
        
        if workout_id:
            self.created_ids['workouts'].append(workout_id)
            
            # Пытаемся получить упражнения для тренировки
            response = requests.get(f"{self.BASE_URL}/workout-exercises/{workout_id}")
            self.assertEqual(response.status_code, 200)

    def test_12_get_workout_stats(self):
        """Тест получения статистики тренировок"""
        response = requests.get(f"{self.BASE_URL}/stats/workouts")
        self.assertEqual(response.status_code, 200)
        stats = response.json()
        self.assertIsInstance(stats, dict)
        self.assertIn('total_workouts', stats)

    def test_13_get_progress_stats(self):
        """Тест получения статистики прогресса"""
        response = requests.get(f"{self.BASE_URL}/stats/progress")
        self.assertEqual(response.status_code, 200)
        stats = response.json()
        self.assertIsInstance(stats, dict)

    def test_14_delete_workout(self):
        """Тест удаления тренировки"""
        # Сначала создаем тренировку
        create_data = {
            'title': f'Workout to delete {self.timestamp}',
            'workout_type': 'yoga',
            'duration_minutes': 30,
            'date': str(date.today())
        }
        create_response = requests.post(f"{self.BASE_URL}/workouts/", params=create_data)
        self.assertEqual(create_response.status_code, 200)
        workout_id = create_response.json().get('workout_id')
        
        if workout_id:
            # Удаляем тренировку
            delete_response = requests.delete(f"{self.BASE_URL}/workouts/{workout_id}")
            self.assertEqual(delete_response.status_code, 200)

    def test_15_delete_exercise(self):
        """Тест удаления упражнения"""
        # Сначала создаем упражнение
        create_data = {
            'name': f'Exercise to delete {self.timestamp}',
            'description': 'To be deleted',
            'muscle_group': 'Back'
        }
        create_response = requests.post(f"{self.BASE_URL}/exercises/", params=create_data)
        self.assertEqual(create_response.status_code, 200)
        exercise_id = create_response.json().get('exercise_id')
        
        if exercise_id:
            # Удаляем упражнение
            delete_response = requests.delete(f"{self.BASE_URL}/exercises/{exercise_id}")
            self.assertEqual(delete_response.status_code, 200)

    def test_16_delete_progress(self):
        """Тест удаления записи прогресса"""
        # Сначала создаем запись прогресса
        create_data = {
            'date': str(date.today()),
            'weight': 77.0,
            'notes': 'To be deleted'
        }
        create_response = requests.post(f"{self.BASE_URL}/progress/", params=create_data)
        self.assertEqual(create_response.status_code, 200)
        progress_id = create_response.json().get('progress_id')
        
        if progress_id:
            # Удаляем запись прогресса
            delete_response = requests.delete(f"{self.BASE_URL}/progress/{progress_id}")
            self.assertEqual(delete_response.status_code, 200)

    def test_17_update_workout_exercise(self):
        """Тест обновления упражнения в тренировке"""
        # Сначала создаем тренировку, упражнение и связь
        workout_data = {
            'title': f'Workout for update exercise {self.timestamp}',
            'workout_type': 'strength',
            'duration_minutes': 50,
            'date': str(date.today())
        }
        workout_response = requests.post(f"{self.BASE_URL}/workouts/", params=workout_data)
        workout_id = workout_response.json().get('workout_id')
        
        exercise_data = {
            'name': f'Exercise for update {self.timestamp}',
            'muscle_group': 'Shoulders'
        }
        exercise_response = requests.post(f"{self.BASE_URL}/exercises/", params=exercise_data)
        exercise_id = exercise_response.json().get('exercise_id')
        
        if workout_id and exercise_id:
            self.created_ids['workouts'].append(workout_id)
            self.created_ids['exercises'].append(exercise_id)
            
            # Создаем связь
            workout_exercise_data = {
                'workout_id': workout_id,
                'exercise_id': exercise_id,
                'sets': 3,
                'reps': 12,
                'weight_kg': 20.0
            }
            create_response = requests.post(f"{self.BASE_URL}/workout-exercises/", params=workout_exercise_data)
            workout_exercise_id = create_response.json().get('workout_exercise_id')
            
            if workout_exercise_id:
                self.created_ids['workout_exercises'].append(workout_exercise_id)
                
                # Обновляем связь
                update_data = {
                    'sets': 4,
                    'reps': 10,
                    'weight_kg': 25.0
                }
                update_response = requests.put(f"{self.BASE_URL}/workout-exercises/{workout_exercise_id}", params=update_data)
                self.assertEqual(update_response.status_code, 200)

    def test_18_delete_workout_exercise(self):
        """Тест удаления упражнения из тренировки"""
        # Сначала создаем тренировку, упражнение и связь
        workout_data = {
            'title': f'Workout for delete exercise {self.timestamp}',
            'workout_type': 'strength',
            'duration_minutes': 40,
            'date': str(date.today())
        }
        workout_response = requests.post(f"{self.BASE_URL}/workouts/", params=workout_data)
        workout_id = workout_response.json().get('workout_id')
        
        exercise_data = {
            'name': f'Exercise for delete {self.timestamp}',
            'muscle_group': 'Legs'
        }
        exercise_response = requests.post(f"{self.BASE_URL}/exercises/", params=exercise_data)
        exercise_id = exercise_response.json().get('exercise_id')
        
        if workout_id and exercise_id:
            self.created_ids['workouts'].append(workout_id)
            self.created_ids['exercises'].append(exercise_id)
            
            # Создаем связь
            workout_exercise_data = {
                'workout_id': workout_id,
                'exercise_id': exercise_id,
                'sets': 3,
                'reps': 15
            }
            create_response = requests.post(f"{self.BASE_URL}/workout-exercises/", params=workout_exercise_data)
            workout_exercise_id = create_response.json().get('workout_exercise_id')
            
            if workout_exercise_id:
                # Удаляем связь
                delete_response = requests.delete(f"{self.BASE_URL}/workout-exercises/{workout_exercise_id}")
                self.assertEqual(delete_response.status_code, 200)

    def test_19_complete_workflow(self):
        """Тест полного рабочего процесса"""
        # 1. Создаем тренировку
        workout_data = {
            'title': f'Complete Workflow Workout {self.timestamp}',
            'workout_type': 'hiit',
            'duration_minutes': 30,
            'calories_burned': 400,
            'date': str(date.today()),
            'notes': 'Complete workflow test'
        }
        workout_response = requests.post(f"{self.BASE_URL}/workouts/", params=workout_data)
        self.assertEqual(workout_response.status_code, 200)
        workout_id = workout_response.json().get('workout_id')
        
        # 2. Создаем упражнение
        exercise_data = {
            'name': f'Complete Workflow Exercise {self.timestamp}',
            'description': 'For complete workflow test',
            'muscle_group': 'Full Body'
        }
        exercise_response = requests.post(f"{self.BASE_URL}/exercises/", params=exercise_data)
        self.assertEqual(exercise_response.status_code, 200)
        exercise_id = exercise_response.json().get('exercise_id')
        
        if workout_id and exercise_id:
            self.created_ids['workouts'].append(workout_id)
            self.created_ids['exercises'].append(exercise_id)
            
            # 3. Добавляем упражнение в тренировку
            workout_exercise_data = {
                'workout_id': workout_id,
                'exercise_id': exercise_id,
                'sets': 4,
                'reps': 15,
                'duration_seconds': 60
            }
            workout_exercise_response = requests.post(f"{self.BASE_URL}/workout-exercises/", params=workout_exercise_data)
            self.assertEqual(workout_exercise_response.status_code, 200)
            workout_exercise_id = workout_exercise_response.json().get('workout_exercise_id')
            
            if workout_exercise_id:
                self.created_ids['workout_exercises'].append(workout_exercise_id)
            
            # 4. Создаем запись прогресса
            progress_data = {
                'date': str(date.today()),
                'weight': 76.0,
                'muscle_mass': 66.0,
                'notes': 'After complete workout'
            }
            progress_response = requests.post(f"{self.BASE_URL}/progress/", params=progress_data)
            self.assertEqual(progress_response.status_code, 200)
            progress_id = progress_response.json().get('progress_id')
            
            if progress_id:
                self.created_ids['progress'].append(progress_id)
            
            # 5. Проверяем статистику
            stats_response = requests.get(f"{self.BASE_URL}/stats/workouts")
            self.assertEqual(stats_response.status_code, 200)
            
            # 6. Проверяем данные
            workouts_response = requests.get(f"{self.BASE_URL}/workouts/")
            self.assertEqual(workouts_response.status_code, 200)
            
            exercises_response = requests.get(f"{self.BASE_URL}/exercises/")
            self.assertEqual(exercises_response.status_code, 200)
            
            progress_response = requests.get(f"{self.BASE_URL}/progress/")
            self.assertEqual(progress_response.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)