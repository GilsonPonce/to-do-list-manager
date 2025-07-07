import json
from datetime import datetime

class ToDoListManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []
    
    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump(self.tasks, file, indent=4)
    
    def add_task(self):
        print("\n--- Añadir Nueva Tarea ---")
        title = input("Título de la tarea: ")
        description = input("Descripción: ")
        due_date = input("Fecha límite (YYYY-MM-DD): ")
        priority = input("Prioridad (Alta/Media/Baja): ").capitalize()
        
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            print("Formato de fecha incorrecto. Usa YYYY-MM-DD")
            return
        
        new_task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description,
            'due_date': due_date,
            'priority': priority,
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.tasks.append(new_task)
        self.save_tasks()
        print(f"Tarea '{title}' añadida correctamente!")
    
    def list_tasks(self, filter_type='all'):
        print("\n--- Lista de Tareas ---")
        if not self.tasks:
            print("No hay tareas registradas.")
            return
        
        filtered_tasks = []
        if filter_type == 'all':
            filtered_tasks = self.tasks
        elif filter_type == 'completed':
            filtered_tasks = [task for task in self.tasks if task['completed']]
        elif filter_type == 'pending':
            filtered_tasks = [task for task in self.tasks if not task['completed']]
        elif filter_type == 'high':
            filtered_tasks = [task for task in self.tasks if task['priority'] == 'Alta']
        
        if not filtered_tasks:
            print(f"No hay tareas {filter_type}.")
            return
        
        for task in filtered_tasks:
            status = "✓" if task['completed'] else "✗"
            print(f"\nID: {task['id']}")
            print(f"Título: {task['title']}")
            print(f"Descripción: {task['description']}")
            print(f"Fecha límite: {task['due_date']}")
            print(f"Prioridad: {task['priority']}")
            print(f"Estado: {status}")
            print(f"Creada el: {task['created_at']}")
    
    def mark_completed(self):
        self.list_tasks('pending')
        if not self.tasks:
            return
        
        try:
            task_id = int(input("\nID de la tarea a marcar como completada: "))
            task = next((t for t in self.tasks if t['id'] == task_id), None)
            
            if task:
                task['completed'] = True
                self.save_tasks()
                print(f"Tarea '{task['title']}' marcada como completada!")
            else:
                print("ID no válido.")
        except ValueError:
            print("Por favor, ingresa un número válido.")
    
    def delete_all_tasks(self):
        confirm = input("\n¿Estás seguro de borrar TODAS las tareas? (s/n): ").lower()
        if confirm == 's':
            self.tasks = []
            self.save_tasks()
            print("Todas las tareas han sido eliminadas.")
        else:
            print("Operación cancelada.")
    
    # Funcionalidades adicionales
    def search_tasks(self):
        keyword = input("\nBuscar tareas (palabra clave): ").lower()
        found_tasks = [
            task for task in self.tasks 
            if keyword in task['title'].lower() or keyword in task['description'].lower()
        ]
        
        if found_tasks:
            print(f"\n--- Resultados para '{keyword}' ---")
            for task in found_tasks:
                status = "✓" if task['completed'] else "✗"
                print(f"\nID: {task['id']} - {task['title']} ({status})")
                print(f"Descripción: {task['description']}")
        else:
            print(f"No se encontraron tareas con '{keyword}'.")
    
    def upcoming_deadlines(self):
        today = datetime.now().strftime('%Y-%m-%d')
        upcoming = [
            task for task in self.tasks 
            if not task['completed'] and task['due_date'] >= today
        ]
        
        if upcoming:
            print("\n--- Próximos vencimientos ---")
            for task in sorted(upcoming, key=lambda x: x['due_date']):
                print(f"\nID: {task['id']} - {task['title']}")
                print(f"Fecha límite: {task['due_date']}")
                print(f"Prioridad: {task['priority']}")
        else:
            print("No hay tareas pendientes con fechas próximas.")

def main():
    manager = ToDoListManager()
    
    while True:
        print("\n=== To-Do List Manager ===")
        print("1. Añadir tarea")
        print("2. Listar todas las tareas")
        print("3. Listar tareas pendientes")
        print("4. Listar tareas completadas")
        print("5. Listar tareas de alta prioridad")
        print("6. Marcar tarea como completada")
        print("7. Buscar tareas")
        print("8. Próximos vencimientos")
        print("9. Borrar todas las tareas")
        print("0. Salir")
        
        choice = input("\nSelecciona una opción: ")
        
        if choice == '1':
            manager.add_task()
        elif choice == '2':
            manager.list_tasks('all')
        elif choice == '3':
            manager.list_tasks('pending')
        elif choice == '4':
            manager.list_tasks('completed')
        elif choice == '5':
            manager.list_tasks('high')
        elif choice == '6':
            manager.mark_completed()
        elif choice == '7':
            manager.search_tasks()
        elif choice == '8':
            manager.upcoming_deadlines()
        elif choice == '9':
            manager.delete_all_tasks()
        elif choice == '0':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()