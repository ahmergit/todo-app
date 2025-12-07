<!--
Sync Impact Report:
Version change: [Not specified - treating as initial] → 1.0.0
Modified principles: None (initial creation)
Added sections:
  - Principle I: Spec-Driven Development
  - Principle II: Test-First Development
  - Principle III: Environment Management
  - Principle IV: Clean Code Practices
  - Principle V: Modular Architecture
  - Section: Technology Stack
  - Section: Development Workflow
  - Governance rules established
Templates requiring updates:
  ✅ plan-template.md - Constitution Check section references this file
  ✅ spec-template.md - Requirements align with principles
  ✅ tasks-template.md - Task categorization reflects TDD discipline
Follow-up TODOs: None
-->

# Todo App Constitution

## Core Principles

### I. Spec-Driven Development

Every feature MUST be defined through a clear specification before any code is written. No implementation work may begin without an approved spec document that includes:
- User stories with acceptance criteria
- Functional requirements
- Success metrics
- Edge cases

**Rationale**: Specifications prevent scope creep, ensure shared understanding between stakeholders, and provide a reference point for validating implementation completeness. Starting with specs reduces rework and keeps features aligned with actual user needs.

### II. Test-First Development (NON-NEGOTIABLE)

TDD is mandatory for all feature development. The Red-Green-Refactor cycle MUST be strictly followed:
1. **Red**: Write tests that capture requirements and watch them fail
2. **Green**: Implement minimal code to make tests pass
3. **Refactor**: Clean up code while keeping tests green

Tests MUST be written before implementation. No production code may be committed without corresponding tests that verify its behavior.

**Rationale**: Test-first development ensures requirements are testable, catches bugs early, serves as living documentation, and enables confident refactoring. This non-negotiable principle guarantees code quality and maintainability from day one.

### III. Environment Management

All development MUST use Python 3.13+ and uv for environment management and dependency handling. The uv tool provides:
- Fast, reproducible dependency resolution
- Consistent environments across development and deployment
- Efficient package installation and virtual environment management

Teams MUST NOT use alternative tools (pip, poetry, pipenv) unless explicitly approved and documented with architectural justification.

**Rationale**: Standardizing on uv ensures fast, deterministic builds, eliminates "works on my machine" issues, and reduces onboarding friction. Python 3.13+ provides modern language features and performance improvements critical for long-term maintainability.

### IV. Clean Code Practices

All code MUST adhere to clean coding principles:
- **Readable**: Self-documenting with clear naming and structure
- **Simple**: Avoid premature optimization and over-engineering
- **DRY**: Don't repeat yourself—extract common patterns appropriately
- **SOLID**: Single responsibility, open/closed, Liskov substitution, interface segregation, dependency inversion
- **Testable**: Design for testability with clear boundaries and dependencies

Code reviews MUST verify compliance with these practices. Complex code MUST include justification in comments or architectural decision records.

**Rationale**: Clean code reduces cognitive load, accelerates onboarding, simplifies debugging, and enables sustainable development velocity over the project lifecycle.

### V. Modular Architecture

The system MUST maintain a modular structure with clear separation of concerns:
- **Models**: Data structures and domain entities
- **Services**: Business logic and orchestration
- **CLI/API**: User-facing interfaces
- **Tests**: Organized by type (unit, integration, contract)

Modules MUST have well-defined interfaces and minimal coupling. Cross-cutting concerns (logging, configuration, error handling) MUST be implemented as reusable utilities.

**Rationale**: Modularity enables parallel development, independent testing, incremental feature delivery, and easier maintenance. Clear boundaries prevent architectural erosion and make the codebase easier to reason about.

### VI. Lightweight and Evolutionary Design

The system MUST remain lightweight and dependency-minimal:
- Prefer standard library solutions over third-party dependencies
- Each new dependency MUST be justified by clear, substantial value
- Architecture MUST support future evolution without requiring major rewrites
- Avoid frameworks that impose heavy abstractions or coupling

Design decisions MUST favor simplicity and flexibility over premature generalization. Future phases can extend capabilities, but the foundation must stay lean.

**Rationale**: Minimal dependencies reduce security surface area, simplify deployment, speed up testing, and lower maintenance burden. Evolutionary architecture acknowledges that requirements change and over-engineering wastes effort on unused features.

## Technology Stack

**Language**: Python 3.13+
**Package Manager**: uv (required for all dependency and environment management)
**Testing Framework**: pytest (or unittest for standard library preference)
**Code Quality**: ruff (or pylint/black for linting and formatting)
**Version Control**: Git with clear commit messages and branch strategy

Additional dependencies MUST be approved through the governance process and documented with rationale.

## Development Workflow

### Feature Development Cycle

1. **Specification Phase**: Create spec.md with user stories, requirements, and acceptance criteria
2. **Planning Phase**: Generate plan.md with architecture, technical context, and structure
3. **Task Breakdown**: Create tasks.md organized by user story with clear dependencies
4. **Red Phase**: Write failing tests for the first task
5. **Green Phase**: Implement minimal code to pass tests
6. **Refactor Phase**: Clean up while keeping tests green
7. **Repeat**: Continue Red-Green-Refactor for remaining tasks
8. **Review**: Code review verifies constitution compliance
9. **Deploy**: Ship incrementally after each completed user story

### Quality Gates

Before merging any code:
- All tests MUST pass
- Code coverage MUST meet project standards (defined per feature)
- Linter MUST pass with no violations
- Code review MUST approve with constitution compliance verified
- Specification acceptance criteria MUST be met

### Prompt History Records (PHR)

Every user interaction and development session MUST be recorded as a Prompt History Record under `history/prompts/`:
- Constitution changes → `history/prompts/constitution/`
- Feature work → `history/prompts/<feature-name>/`
- General tasks → `history/prompts/general/`

PHRs provide traceability, learning history, and context for future work.

### Architecture Decision Records (ADR)

Architecturally significant decisions MUST be documented as ADRs in `history/adr/`:
- Technology choices (frameworks, libraries, platforms)
- Design patterns and architectural styles
- Data models and storage strategies
- API contracts and integration approaches

ADRs require explicit user approval—no auto-creation without consent.

## Governance

This constitution supersedes all other development practices and guidelines. All code, designs, and decisions MUST comply with these principles.

### Amendment Process

Constitution changes require:
1. Documented proposal with rationale
2. Impact analysis on existing codebase and templates
3. User/stakeholder approval
4. Version increment following semantic versioning
5. Migration plan for affected artifacts
6. Synchronization of dependent templates (plan, spec, tasks, commands)

### Version Policy

- **MAJOR**: Backward-incompatible governance or principle changes
- **MINOR**: New principles added or existing ones materially expanded
- **PATCH**: Clarifications, wording improvements, typo fixes

### Compliance Review

All pull requests MUST verify constitution compliance:
- Spec-driven: Is there an approved spec?
- Test-first: Were tests written before implementation?
- Clean code: Does the code meet readability and simplicity standards?
- Modular: Are boundaries and separation of concerns maintained?
- Lightweight: Are new dependencies justified?

Violations MUST be documented in the plan.md Complexity Tracking section with explicit justification for why simpler alternatives were rejected.

### Runtime Guidance

For operational development guidance, see `CLAUDE.md` (agent-specific instructions) and `.specify/templates/commands/` (workflow execution).

**Version**: 1.0.0 | **Ratified**: 2025-12-05 | **Last Amended**: 2025-12-05
