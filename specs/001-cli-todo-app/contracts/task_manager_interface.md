# TaskManager Interface Contract

**Feature**: 001-cli-todo-app
**Component**: TaskManager (Business Logic Layer)
**Version**: 1.0.0
**Date**: 2025-12-05

## Purpose

This contract defines the public interface of the TaskManager class, which provides business logic for managing tasks in memory. The interface serves as a boundary between the UI layer and the data model, ensuring separation of concerns and testability.

## Interface Definition

### Class: `TaskManager`

**Responsibility**: Manage task lifecycle (create, read, update, delete, complete) and maintain task collection integrity.

**Dependencies**:
- `Task` (from todo.models)
- `Priority` (from todo.models)

**State**:
- Private: `_tasks: list[Task]` - Ordered collection of tasks
- Private: `_next_id: int` - Next available task ID

---

## Public Methods

### 1. `__init__() -> None`

Initialize a new TaskManager with empty task list.

**Parameters**: None

**Returns**: None

**Side Effects**:
- Initializes empty task list
- Sets next_id to 1

**Exceptions**: None

**Example**:
```python
manager = TaskManager()
```

---

### 2. `add_task(description: str, priority: Priority = Priority.MEDIUM) -> Task`

Create and add a new task to the task list.

**Parameters**:
- `description: str` - Task description (1-500 chars, required)
- `priority: Priority` - Task priority (optional, defaults to MEDIUM)

**Returns**: `Task` - The newly created task with assigned ID

**Side Effects**:
- Adds task to internal list
- Increments next_id counter

**Exceptions**:
- `ValueError` - If description is empty or >500 characters
- `TypeError` - If description is not a string or priority is not Priority enum

**Preconditions**:
- description must be non-empty after strip()
- priority must be valid Priority enum value

**Postconditions**:
- Task added to list with unique ID
- next_id incremented
- Task ID never reused

**Example**:
```python
task = manager.add_task("Buy groceries", Priority.HIGH)
assert task.id == 1
assert task.description == "Buy groceries"
assert task.priority == Priority.HIGH
assert task.completed == False
```

**Contract Tests**:
- Task ID starts at 1 for first task
- Task IDs increment sequentially (1, 2, 3...)
- Returned task is in task list (get_by_id succeeds)
- Default priority is MEDIUM if not specified
- Empty description raises ValueError
- Description >500 chars raises ValueError

---

### 3. `get_task_by_id(task_id: int) -> Task | None`

Retrieve a task by its unique ID.

**Parameters**:
- `task_id: int` - ID of task to retrieve

**Returns**:
- `Task` if task with given ID exists
- `None` if task not found

**Side Effects**: None (read-only operation)

**Exceptions**: None (invalid IDs return None rather than raising exceptions)

**Preconditions**: None

**Postconditions**:
- Task state unchanged
- Returns same task object on repeated calls with same ID

**Example**:
```python
task = manager.get_task_by_id(1)
if task:
    print(task.description)
else:
    print("Task not found")
```

**Contract Tests**:
- Valid ID returns correct task
- Invalid ID returns None
- Negative ID returns None
- Zero ID returns None
- ID of deleted task returns None

---

### 4. `get_all_tasks() -> list[Task]`

Retrieve all tasks in creation order.

**Parameters**: None

**Returns**: `list[Task]` - List of all tasks (may be empty)

**Side Effects**: None (read-only operation)

**Exceptions**: None

**Preconditions**: None

**Postconditions**:
- Returns empty list if no tasks
- Returns tasks in creation order (insertion order)
- Original task objects returned (not copies)

**Example**:
```python
tasks = manager.get_all_tasks()
for task in tasks:
    print(f"{task.id}: {task.description}")
```

**Contract Tests**:
- Returns empty list when no tasks
- Returns tasks in creation order
- Deleting task removes it from returned list
- Adding task appends to end of list

---

### 5. `update_task(task_id: int, new_description: str) -> bool`

Update the description of an existing task.

**Parameters**:
- `task_id: int` - ID of task to update
- `new_description: str` - New description (1-500 chars)

**Returns**:
- `True` if task found and updated
- `False` if task not found

**Side Effects**:
- Modifies task description if found
- Does NOT change ID, priority, completed status, or created_at

**Exceptions**:
- `ValueError` - If new_description is empty or >500 characters

**Preconditions**:
- new_description must be valid (1-500 chars after strip)

**Postconditions**:
- If True: task description changed, other attributes unchanged
- If False: no state changed

**Example**:
```python
success = manager.update_task(1, "Buy groceries and milk")
if success:
    print("Task updated")
else:
    print("Task not found")
```

**Contract Tests**:
- Valid ID and description returns True
- Invalid ID returns False
- Empty description raises ValueError
- Description >500 chars raises ValueError
- Only description changes (ID/priority/completed unchanged)
- Completed tasks can be updated

---

### 6. `delete_task(task_id: int) -> bool`

Delete a task from the task list.

**Parameters**:
- `task_id: int` - ID of task to delete

**Returns**:
- `True` if task found and deleted
- `False` if task not found

**Side Effects**:
- Removes task from internal list if found
- ID is retired (never reused for future tasks)

**Exceptions**: None

**Preconditions**: None

**Postconditions**:
- If True: task removed from list, get_by_id returns None
- If False: no state changed
- IDs never reused (next_id continues incrementing)

**Example**:
```python
success = manager.delete_task(1)
if success:
    print("Task deleted")
else:
    print("Task not found")
```

**Contract Tests**:
- Valid ID returns True and removes task
- Invalid ID returns False
- Deleted task ID returns None on get_by_id
- Task count decreases by 1 after successful delete
- IDs never reused after deletion
- Can delete completed tasks

---

### 7. `toggle_complete(task_id: int) -> bool`

Toggle the completion status of a task.

**Parameters**:
- `task_id: int` - ID of task to toggle

**Returns**:
- `True` if task found and toggled
- `False` if task not found

**Side Effects**:
- Toggles task.completed boolean if found
- Does NOT change ID, description, priority, or created_at

**Exceptions**: None

**Preconditions**: None

**Postconditions**:
- If True: task.completed inverted (False→True or True→False)
- If False: no state changed

**Example**:
```python
success = manager.toggle_complete(1)
if success:
    task = manager.get_task_by_id(1)
    print(f"Task completed: {task.completed}")
else:
    print("Task not found")
```

**Contract Tests**:
- Valid ID returns True and toggles status
- Invalid ID returns False
- Incomplete task becomes complete
- Complete task becomes incomplete (if toggled again)
- Only completed status changes (other attributes unchanged)

---

### 8. `set_priority(task_id: int, priority: Priority) -> bool`

Set the priority of an existing task.

**Parameters**:
- `task_id: int` - ID of task to update
- `priority: Priority` - New priority level

**Returns**:
- `True` if task found and priority updated
- `False` if task not found

**Side Effects**:
- Updates task.priority if found
- Does NOT change ID, description, completed status, or created_at

**Exceptions**:
- `TypeError` - If priority is not a Priority enum value

**Preconditions**:
- priority must be valid Priority enum (HIGH, MEDIUM, or LOW)

**Postconditions**:
- If True: task.priority changed, other attributes unchanged
- If False: no state changed

**Example**:
```python
success = manager.set_priority(1, Priority.HIGH)
if success:
    print("Priority updated to HIGH")
else:
    print("Task not found")
```

**Contract Tests**:
- Valid ID and priority returns True
- Invalid ID returns False
- Priority changes correctly (MEDIUM → HIGH, etc.)
- Invalid priority type raises TypeError
- Only priority changes (other attributes unchanged)
- Completed tasks can have priority changed

---

## Invariants

These conditions MUST hold true before and after every public method call:

1. **ID Uniqueness**: All task IDs in _tasks list are unique
2. **ID Sequence**: next_id is always greater than any existing task ID
3. **ID Positivity**: All task IDs are positive integers (>= 1)
4. **List Integrity**: _tasks list contains only valid Task objects
5. **No Nulls**: _tasks list contains no None values
6. **Order Preservation**: Tasks maintain insertion order
7. **Task Validity**: All tasks in list satisfy Task dataclass validation rules

---

## Performance Guarantees

Based on FR-019 (1000 tasks) and SC-005 (<100ms response):

| Method | Time Complexity | Guaranteed Max Time (n=1000) |
|--------|-----------------|------------------------------|
| `__init__()` | O(1) | <1ms |
| `add_task()` | O(1) | <10ms |
| `get_task_by_id()` | O(n) | <100ms |
| `get_all_tasks()` | O(1) | <10ms |
| `update_task()` | O(n) | <100ms |
| `delete_task()` | O(n) | <100ms |
| `toggle_complete()` | O(n) | <100ms |
| `set_priority()` | O(n) | <100ms |

**Rationale**: Linear search O(n) is acceptable for n ≤ 1000. Python list operations are highly optimized.

---

## Error Handling Philosophy

**Validation Strategy**:
- **Input validation**: Performed at UI layer before calling manager
- **Type validation**: Performed at manager layer (raises TypeError)
- **Business rules**: Enforced at manager layer (raises ValueError)

**Exception vs Return Value**:
- **Exceptions**: Used for programming errors (invalid types, validation failures)
- **Return None/False**: Used for expected "not found" cases

**Rationale**: Clear separation allows UI to handle user errors gracefully while catching programming errors during development.

---

## Thread Safety

**Not Required**: Single-threaded CLI application (Assumption 1: "Single user session").

**If Future Parallelism Needed**: Add threading.Lock around _tasks mutations.

---

## Testing Requirements

### Contract Tests (tests/contract/test_manager_contract.py)

Must verify ALL postconditions and invariants listed above:

```python
def test_task_id_uniqueness_invariant(manager):
    """Verify all task IDs are unique"""
    manager.add_task("Task 1")
    manager.add_task("Task 2")
    manager.add_task("Task 3")

    tasks = manager.get_all_tasks()
    ids = [t.id for t in tasks]
    assert len(ids) == len(set(ids)), "Task IDs must be unique"

def test_id_never_reused_after_deletion(manager):
    """Verify deleted task IDs are never reused"""
    task1 = manager.add_task("Task 1")
    task2 = manager.add_task("Task 2")
    manager.delete_task(task1.id)
    task3 = manager.add_task("Task 3")

    assert task3.id == 3, "ID 1 should not be reused"
    assert task3.id > task2.id, "IDs must continue incrementing"
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-05 | Initial contract definition |

---

## Summary

The TaskManager interface provides 8 public methods for managing tasks in memory. All methods have well-defined preconditions, postconditions, side effects, and performance guarantees. The interface maintains 7 critical invariants and provides clear error handling through exceptions and return values. Contract tests MUST verify all postconditions and invariants to ensure implementation correctness.
