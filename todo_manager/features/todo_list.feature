# features/todo_list.feature

Feature: Gestión de lista de tareas
  Como usuario
  Quiero poder gestionar mis tareas pendientes
  Para organizar mejor mi tiempo

  Scenario: Añadir una nueva tarea
    Given que tengo una lista de tareas vacía
    When añado una tarea con título "Comprar leche", descripción "Comprar leche desnatada", fecha "2023-12-31" y prioridad "Media"
    Then la tarea "Comprar leche" debe estar en la lista de tareas
    And la tarea debe tener estado "pendiente"

  Scenario: Listar todas las tareas
    Given que tengo las siguientes tareas:
      | Título        | Descripción          | Fecha     | Prioridad |
      | Comprar pan   | Pan integral         | 2023-12-15 | Alta      |
      | Pagar factura | Factura de electricidad | 2023-12-20 | Media    |
    When listo todas las tareas
    Then debo ver 2 tareas en la lista
    And debo ver la tarea "Comprar pan"
    And debo ver la tarea "Pagar factura"

  Scenario: Marcar tarea como completada
    Given que tengo una tarea "Llamar al médico" en mi lista
    When marco la tarea "Llamar al médico" como completada
    Then la tarea "Llamar al médico" debe aparecer como completada
    And la lista debe mostrar 1 tarea completada

  Scenario: Borrar todas las tareas
    Given que tengo 3 tareas en mi lista
    When borro todas las tareas
    Then la lista de tareas debe estar vacía

  Scenario: Buscar tareas por palabra clave (funcionalidad adicional)
    Given que tengo las siguientes tareas:
      | Título        | Descripción          |
      | Comprar regalo | Regalo de cumpleaños |
      | Limpiar casa  | Limpieza general     |
    When busco tareas con la palabra "regalo"
    Then debo ver 1 tarea en los resultados
    And debo ver la tarea "Comprar regalo"

  Scenario: Mostrar próximos vencimientos (funcionalidad adicional)
    Given que hoy es "2023-12-10"
    And tengo las siguientes tareas:
      | Título        | Fecha     |
      | Reunión       | 2023-12-15 |
      | Examen        | 2023-12-20 |
      | Entrega       | 2023-12-05 |
    When consulto los próximos vencimientos
    Then debo ver 2 tareas en la lista
    And debo ver la tarea "Reunión"
    And debo ver la tarea "Examen"
    And no debo ver la tarea "Entrega"