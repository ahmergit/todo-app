---

description: "Task list for CLI Todo Application implementation"
---

# Tasks: CLI Todo Application

**Input**: Design documents from `/specs/001-cli-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Constitution mandates Test-First Development (NON-NEGOTIABLE). All tasks follow TDD: Red-Green-Refactor cycle strictly enforced.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below use single project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Initialize uv project with name "todo" and Python 3.13+ in pyproject.toml
- [X] T002 Create src/todo/ package structure with __init__.py
- [X] T003 [P] Create test directories: tests/unit/, tests/integration/, tests/contract/
- [X] T004 [P] Configure pyproject.toml with pytest settings and project scripts
- [X] T005 [P] Create .gitignore for Python, uv, pytest, and IDE files
- [X] T006 [P] Add pytest as dev dependency via uv add --dev pytest

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Write tests for Priority enum in tests/unit/test_models.py (expect FAIL - Red phase)
- [X] T008 Implement Priority enum (HIGH, MEDIUM, LOW) in src/todo/models.py (Green phase)
- [X] T009 Write tests for Task dataclass creation with all fields in tests/unit/test_models.py (expect FAIL - Red phase)
- [X] T010 Write tests for Task dataclass default values in tests/unit/test_models.py (expect FAIL - Red phase)
- [X] T011 Write tests for Task validation (empty description, >500 chars) in tests/unit/test_models.py (expect FAIL - Red phase)
- [X] T012 Implement Task dataclass with validation in src/todo/models.py (Green phase)
- [X] T013 Refactor Task model: review code quality, add docstrings, ensure testability (Refactor phase)
- [X] T014 Write tests for TaskManager.__init__ in tests/unit/test_manager.py (expect FAIL - Red phase)
- [X] T015 Write tests for TaskManager.add_task with ID generation in tests/unit/test_manager.py (expect FAIL - Red phase)
- [X] T016 Write tests for TaskManager.get_task_by_id in tests/unit/test_manager.py (expect FAIL - Red phase)
- [X] T017 Write tests for TaskManager.get_all_tasks in tests/unit/test_manager.py (expect FAIL - Red phase)
- [X] T018 Implement TaskManager class skeleton with __init__, _tasks list, _next_id in src/todo/manager.py (Green phase)
- [X] T019 Implement TaskManager.add_task method in src/todo/manager.py (Green phase)
- [X] T020 Implement TaskManager.get_task_by_id method in src/todo/manager.py (Green phase)
- [X] T021 Implement TaskManager.get_all_tasks method in src/todo/manager.py (Green phase)
- [X] T022 Refactor TaskManager: review methods, add docstrings, ensure clean interfaces (Refactor phase)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 4 - Interactive Console Menu Navigation (Priority: P1) 🎯 MVP Foundation

**Goal**: Build the interactive menu system that enables all other features

**Independent Test**: Launch application, verify menu displays all options, test invalid input handling, confirm exit works gracefully

### Tests for User Story 4 (TDD - Red Phase)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T023 [P] [US4] Write tests for display_menu function in tests/unit/test_ui.py (expect FAIL - Red phase)
- [X] T024 [P] [US4] Write tests for get_menu_choice validation in tests/unit/test_ui.py (expect FAIL - Red phase)
- [X] T025 [P] [US4] Write tests for main menu loop with exit in tests/integration/test_app_flow.py (expect FAIL - Red phase)

### Implementation for User Story 4 (Green Phase)

- [X] T026 [US4] Implement display_menu function in src/todo/ui.py (Green phase)
- [X] T027 [US4] Implement get_menu_choice function with validation in src/todo/ui.py (Green phase)
- [X] T028 [US4] Implement main function with menu loop in src/todo/main.py (Green phase)
- [X] T029 [US4] Add exception handling (KeyboardInterrupt, general errors) in src/todo/main.py (Green phase)
- [X] T030 [US4] Refactor UI and main: clean up code, add docstrings, ensure readability (Refactor phase)

**Checkpoint**: At this point, User Story 4 should be fully functional - menu displays, accepts input, exits gracefully

---

## Phase 4: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP Core

**Goal**: Enable users to add tasks and view their task list (core value proposition)

**Independent Test**: Launch app, add multiple tasks with different descriptions, view tasks, verify all display correctly with ID/priority/status

### Tests for User Story 1 (TDD - Red Phase)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T031 [P] [US1] Write tests for validate_description function in tests/unit/test_ui.py (expect FAIL - Red phase)
- [X] T032 [P] [US1] Write tests for validate_priority_input function in tests/unit/test_ui.py (expect FAIL - Red phase)
- [X] T033 [P] [US1] Write tests for format_task_display function in tests/unit/test_ui.py (expect FAIL - Red phase)
- [X] T034 [P] [US1] Write tests for add task workflow in tests/integration/test_app_flow.py (expect FAIL - Red phase)
- [X] T035 [P] [US1] Write tests for view tasks workflow (empty and populated) in tests/integration/test_app_flow.py (expect FAIL - Red phase)

### Implementation for User Story 1 (Green Phase)

- [X] T036 [US1] Implement validate_description function in src/todo/ui.py (Green phase)
- [X] T037 [US1] Implement validate_priority_input function (accepts H/M/L, Enter for default) in src/todo/ui.py (Green phase)
- [X] T038 [US1] Implement format_task_display function in src/todo/ui.py (Green phase)
- [X] T039 [US1] Implement Colors class with ANSI escape codes in src/todo/ui.py (Green phase)
- [X] T040 [US1] Implement handle_add_task function in src/todo/ui.py (Green phase)
- [X] T041 [US1] Implement handle_view_tasks function with color formatting in src/todo/ui.py (Green phase)
- [X] T042 [US1] Integrate add and view handlers into main menu loop in src/todo/main.py (Green phase)
- [X] T043 [US1] Refactor US1 code: clean up validation, improve formatting, add docstrings (Refactor phase)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently - users can add and view tasks

---

## Phase 5: User Story 2 - Complete and Delete Tasks (Priority: P2)

**Goal**: Enable users to mark tasks complete and delete tasks for list maintenance

**Independent Test**: Create tasks, complete some, verify green color, delete specific tasks, confirm others remain

### Tests for User Story 2 (TDD - Red Phase)

- [ ] T044 [P] [US2] Write tests for TaskManager.toggle_complete in tests/unit/test_manager.py (expect FAIL - Red phase)
- [ ] T045 [P] [US2] Write tests for TaskManager.delete_task in tests/unit/test_manager.py (expect FAIL - Red phase)
- [ ] T046 [P] [US2] Write tests for validate_task_id function in tests/unit/test_ui.py (expect FAIL - Red phase)
- [ ] T047 [P] [US2] Write integration tests for complete task workflow in tests/integration/test_app_flow.py (expect FAIL - Red phase)
- [ ] T048 [P] [US2] Write integration tests for delete task workflow in tests/integration/test_app_flow.py (expect FAIL - Red phase)

### Implementation for User Story 2 (Green Phase)

- [ ] T049 [US2] Implement TaskManager.toggle_complete method in src/todo/manager.py (Green phase)
- [ ] T050 [US2] Implement TaskManager.delete_task method in src/todo/manager.py (Green phase)
- [ ] T051 [US2] Implement validate_task_id function in src/todo/ui.py (Green phase)
- [ ] T052 [US2] Implement handle_complete_task function in src/todo/ui.py (Green phase)
- [ ] T053 [US2] Implement handle_delete_task function in src/todo/ui.py (Green phase)
- [ ] T054 [US2] Integrate complete and delete handlers into main menu loop in src/todo/main.py (Green phase)
- [ ] T055 [US2] Refactor US2 code: review TaskManager methods, clean UI handlers, add docstrings (Refactor phase)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - add/view/complete/delete all functional

---

## Phase 6: User Story 3 - Set and Change Task Priority (Priority: P3)

**Goal**: Enable users to set priority during creation and change priority of existing tasks

**Independent Test**: Create tasks with different priorities (H/M/L), change priorities, verify display shows priority correctly

### Tests for User Story 3 (TDD - Red Phase)

- [ ] T056 [P] [US3] Write tests for TaskManager.set_priority in tests/unit/test_manager.py (expect FAIL - Red phase)
- [ ] T057 [P] [US3] Write tests for priority prompt during add_task in tests/integration/test_app_flow.py (expect FAIL - Red phase)
- [ ] T058 [P] [US3] Write tests for set priority workflow in tests/integration/test_app_flow.py (expect FAIL - Red phase)

### Implementation for User Story 3 (Green Phase)

- [ ] T059 [US3] Implement TaskManager.set_priority method in src/todo/manager.py (Green phase)
- [ ] T060 [US3] Implement handle_set_priority function in src/todo/ui.py (Green phase)
- [ ] T061 [US3] Integrate set priority handler into main menu loop in src/todo/main.py (Green phase)
- [ ] T062 [US3] Update format_task_display to show priority prominently in src/todo/ui.py (Green phase)
- [ ] T063 [US3] Refactor US3 code: review priority handling, clean up display, add docstrings (Refactor phase)

**Checkpoint**: All user stories 1, 2, and 3 should now be independently functional

---

## Phase 7: User Story 5 - Update Task Description (Priority: P4)

**Goal**: Enable users to edit task descriptions to correct mistakes

**Independent Test**: Create task with typo, update description, verify change persists and other attributes unchanged

### Tests for User Story 5 (TDD - Red Phase)

- [ ] T064 [P] [US5] Write tests for TaskManager.update_task in tests/unit/test_manager.py (expect FAIL - Red phase)
- [ ] T065 [P] [US5] Write tests for update task workflow in tests/integration/test_app_flow.py (expect FAIL - Red phase)

### Implementation for User Story 5 (Green Phase)

- [ ] T066 [US5] Implement TaskManager.update_task method in src/todo/manager.py (Green phase)
- [ ] T067 [US5] Implement handle_update_task function in src/todo/ui.py (Green phase)
- [ ] T068 [US5] Integrate update handler into main menu loop in src/todo/main.py (Green phase)
- [ ] T069 [US5] Refactor US5 code: review update logic, clean UI, add docstrings (Refactor phase)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T070 [P] Write contract tests for TaskManager interface in tests/contract/test_manager_contract.py
- [ ] T071 [P] Verify all TaskManager invariants (ID uniqueness, sequence, etc.) in tests/contract/test_manager_contract.py
- [ ] T072 [P] Create README.md with setup instructions (uv init, uv run todo)
- [ ] T073 [P] Add performance validation tests (1000 tasks, <100ms operations) in tests/integration/test_app_flow.py
- [ ] T074 Run full test suite with pytest -v and fix any failures
- [ ] T075 Manual end-to-end testing following quickstart.md validation steps
- [ ] T076 [P] Final code review: ensure all docstrings present, clean code principles followed
- [ ] T077 [P] Verify constitution compliance (TDD followed, uv used, clean architecture maintained)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - User Story 4 (Menu): Must complete first (enables other stories)
  - User Story 1 (Add/View): Can start after US4
  - User Story 2 (Complete/Delete): Can start after US4 and US1
  - User Story 3 (Priority): Can start after US4 and US1
  - User Story 5 (Update): Can start after US4 and US1
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 4 (Menu) - P1**: Must complete FIRST - provides UI infrastructure for all other stories
- **User Story 1 (Add/View) - P1**: Can start after US4 - No dependencies on other stories
- **User Story 2 (Complete/Delete) - P2**: Depends on US1 (needs tasks to complete/delete)
- **User Story 3 (Priority) - P3**: Depends on US1 (needs tasks to set priority)
- **User Story 5 (Update) - P4**: Depends on US1 (needs tasks to update)

### Within Each User Story (TDD Workflow)

- Tests (Red phase) MUST be written and FAIL before implementation
- Implementation (Green phase) makes tests pass with minimal code
- Refactoring (Refactor phase) cleans up code while keeping tests green
- Core implementation before integration with menu
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup tasks**: T002-T006 can run in parallel (different files, independent)
- **Foundational tests**: T007, T009-T011, T014-T017 can run in parallel (test files)
- **US4 tests**: T023-T025 can run in parallel (different test files)
- **US1 tests**: T031-T035 can run in parallel (test files)
- **US2 tests**: T044-T048 can run in parallel (test files)
- **US3 tests**: T056-T058 can run in parallel (test files)
- **US5 tests**: T064-T065 can run in parallel (test files)
- **Polish tasks**: T070-T073, T076-T077 can run in parallel (different concerns)

---

## Parallel Example: User Story 1 Tests (Red Phase)

```bash
# Launch all test writing tasks for User Story 1 together:
Task: "T031 [P] [US1] Write tests for validate_description function in tests/unit/test_ui.py"
Task: "T032 [P] [US1] Write tests for validate_priority_input function in tests/unit/test_ui.py"
Task: "T033 [P] [US1] Write tests for format_task_display function in tests/unit/test_ui.py"
Task: "T034 [P] [US1] Write tests for add task workflow in tests/integration/test_app_flow.py"
Task: "T035 [P] [US1] Write tests for view tasks workflow in tests/integration/test_app_flow.py"

# Then run pytest to verify all tests FAIL (Red phase)
# Then proceed to implementation tasks (Green phase)
```

---

## Implementation Strategy

### MVP First (User Stories 4 + 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T022) - CRITICAL foundation
3. Complete Phase 3: User Story 4 Menu (T023-T030) - Enables all features
4. Complete Phase 4: User Story 1 Add/View (T031-T043) - Core value
5. **STOP and VALIDATE**: Test US4 + US1 independently
6. Deploy/demo if ready - this is a working MVP!

### Incremental Delivery (All User Stories)

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 4 (Menu) → Test independently → MVP infrastructure
3. Add User Story 1 (Add/View) → Test independently → MVP complete!
4. Add User Story 2 (Complete/Delete) → Test independently → Enhanced functionality
5. Add User Story 3 (Priority) → Test independently → Power user features
6. Add User Story 5 (Update) → Test independently → Convenience features
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 4 (Menu) - MUST complete first
3. After US4 complete:
   - Developer A: User Story 1 (Add/View)
   - Developer B: Can prepare US2 tests (will need US1 complete for integration)
4. After US1 complete:
   - Developer B: User Story 2 (Complete/Delete)
   - Developer C: User Story 3 (Priority)
   - Developer D: User Story 5 (Update)
5. Stories complete and integrate independently

---

## TDD Workflow Enforcement

**Constitution Mandate**: Test-First Development is NON-NEGOTIABLE

For EVERY user story phase:

1. **RED**: Write all tests for the story (marked with [P] where parallel)
2. **Verify RED**: Run `uv run pytest -v` - ALL tests MUST FAIL
3. **GREEN**: Implement minimal code to make tests pass
4. **Verify GREEN**: Run `uv run pytest -v` - ALL tests MUST PASS
5. **REFACTOR**: Clean up code while keeping tests green
6. **Verify REFACTOR**: Run `uv run pytest -v` - ALL tests MUST STILL PASS

**Never skip RED phase**: If tests pass before implementation, they're not testing the right thing.

---

## Notes

- **[P] tasks**: Different files, no dependencies - safe to parallelize
- **[Story] label**: Maps task to specific user story for traceability
- **TDD strictly enforced**: Tests before code, always
- **Each user story**: Independently completable and testable
- **Verify tests FAIL**: Critical - don't skip RED phase validation
- **Commit after each phase**: Or after each TDD cycle (Red→Green→Refactor)
- **Stop at any checkpoint**: Validate story independently before proceeding
- **Constitution compliance**: Zero runtime dependencies, uv for env, clean architecture maintained

---

## Task Count Summary

- **Phase 1 (Setup)**: 6 tasks
- **Phase 2 (Foundational)**: 16 tasks (TDD: 9 test tasks + 7 implementation/refactor)
- **Phase 3 (US4 - Menu - P1)**: 8 tasks (TDD: 3 test tasks + 5 implementation/refactor)
- **Phase 4 (US1 - Add/View - P1)**: 13 tasks (TDD: 5 test tasks + 8 implementation/refactor)
- **Phase 5 (US2 - Complete/Delete - P2)**: 12 tasks (TDD: 5 test tasks + 7 implementation/refactor)
- **Phase 6 (US3 - Priority - P3)**: 8 tasks (TDD: 3 test tasks + 5 implementation/refactor)
- **Phase 7 (US5 - Update - P4)**: 6 tasks (TDD: 2 test tasks + 4 implementation/refactor)
- **Phase 8 (Polish)**: 8 tasks

**Total**: 77 tasks

**Test tasks**: 27 (35% of total - reflects TDD mandate)
**Parallel opportunities**: 28 tasks marked [P] (36% parallelizable)
**MVP scope**: 27 tasks (Phases 1-4: Setup + Foundational + US4 + US1)
