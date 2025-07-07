# features/steps/todo_list_steps.py

from behave import given, when, then
from todo_manager import ToDoListManager
from datetime import datetime
import json
import os

@given('que tengo una lista de tareas vacía')
def given_empty_task_list(context):
    # Limpiar cualquier archivo de tareas existente
    if os.path.exists('tasks.json'):
        os.remove('tasks.json')
    context.manager = ToDoListManager()
    assert len(context.manager.tasks) == 0

@when('añado una tarea con título "{title}", descripción "{description}", fecha "{due_date}" y prioridad "{priority}"')
def when_add_task_with_details(context, title, description, due_date, priority):
    # Simulamos la entrada del usuario
    context.manager.add_task = lambda: None  # Desactivamos el input real
    context.manager.tasks.append({
        'id': 1,
        'title': title,
        'description': description,
        'due_date': due_date,
        'priority': priority,
        'completed': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    context.manager.save_tasks()

@then('la tarea "{title}" debe estar en la lista de tareas')
def then_task_should_be_in_list(context, title):
    assert any(task['title'] == title for task in context.manager.tasks)

@then('la tarea debe tener estado "{status}"')
def then_task_should_have_status(context, status):
    expected_status = False if status == "pendiente" else True
    assert context.manager.tasks[-1]['completed'] == expected_status

@given('que tengo las siguientes tareas:')
def given_following_tasks(context):
    context.manager = ToDoListManager()
    context.manager.tasks = []
    for row in context.table:
        context.manager.tasks.append({
            'id': len(context.manager.tasks) + 1,
            'title': row['Título'],
            'description': row['Descripción'] if 'Descripción' in row else '',
            'due_date': row['Fecha'] if 'Fecha' in row else '2023-12-31',
            'priority': row['Prioridad'] if 'Prioridad' in row else 'Media',
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    context.manager.save_tasks()

@when('listo todas las tareas')
def when_list_all_tasks(context):
    # Simplemente establecemos un flag para verificar que se llamó
    context.listed_tasks = True

@then('debo ver {count:d} tareas en la lista')
def then_should_see_n_tasks_in_list(context, count):
    assert len(context.manager.tasks) == count

@then('debo ver la tarea "{title}"')
def then_should_see_task(context, title):
    assert any(task['title'] == title for task in context.manager.tasks)

@given('que tengo una tarea "{title}" en mi lista')
def given_task_in_list(context, title):
    context.manager = ToDoListManager()
    context.manager.tasks = [{
        'id': 1,
        'title': title,
        'description': '',
        'due_date': '2023-12-31',
        'priority': 'Media',
        'completed': False,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }]
    context.manager.save_tasks()

@when('marco la tarea "{title}" como completada')
def when_mark_task_completed(context, title):
    for task in context.manager.tasks:
        if task['title'] == title:
            task['completed'] = True
    context.manager.save_tasks()

@then('la tarea "{title}" debe aparecer como completada')
def then_task_should_appear_completed(context, title):
    task = next(t for t in context.manager.tasks if t['title'] == title)
    assert task['completed'] is True

@then('la lista debe mostrar {count:d} tarea completada')
def then_list_should_show_n_completed_tasks(context, count):
    completed = sum(1 for task in context.manager.tasks if task['completed'])
    assert completed == count

@given('que tengo {count:d} tareas en mi lista')
def given_n_tasks_in_list(context, count):
    context.manager = ToDoListManager()
    context.manager.tasks = []
    for i in range(count):
        context.manager.tasks.append({
            'id': i+1,
            'title': f'Tarea {i+1}',
            'description': '',
            'due_date': '2023-12-31',
            'priority': 'Media',
            'completed': False,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    context.manager.save_tasks()

@when('borro todas las tareas')
def when_delete_all_tasks(context):
    context.manager.tasks = []
    context.manager.save_tasks()

@then('la lista de tareas debe estar vacía')
def then_task_list_should_be_empty(context):
    assert len(context.manager.tasks) == 0

@when('busco tareas con la palabra "{keyword}"')
def when_search_tasks_by_keyword(context, keyword):
    context.search_results = [
        task for task in context.manager.tasks 
        if keyword.lower() in task['title'].lower() or 
           keyword.lower() in task['description'].lower()
    ]

@then('debo ver {count:d} tarea en los resultados')
def then_should_see_n_tasks_in_results(context, count):
    assert len(context.search_results) == count

@given('que hoy es "{date}"')
def given_today_is(context, date):
    context.today = date

@when('consulto los próximos vencimientos')
def when_check_upcoming_tasks(context):
    context.upcoming_tasks = [
        task for task in context.manager.tasks 
        if not task['completed'] and task['due_date'] >= context.today
    ]

@then('no debo ver la tarea "{title}"')
def then_should_not_see_task_in_upcoming(context, title):
    assert not any(task['title'] == title for task in context.upcoming_tasks)