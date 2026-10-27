# Quality Gateway & Test Coverage Improvement Plan

## Overview

This document outlines the comprehensive quality gateway improvements for the coworker_ai project. Currently, the project has **2% test coverage** with only 4 tests covering a single dataclass. This plan addresses critical gaps in testing, code quality, and CI/CD strictness.

---

## 📊 Current State Analysis

### Test Coverage Summary
- **Total Lines of Code**: 958 (across 25 Python files in `src/`)
- **Tested Lines**: 8 (LLMConfig dataclass only)
- **Coverage**: **2%**
- **Untested Files**: 24 out of 25 source files

### Untested Modules (Priority Order)

#### 🔴 Critical (High Complexity, Core Functionality)
1. **`src/role/chat_manager.py`** - 312 lines, 0% coverage
   - Core business logic
   - Manages chat history, RAG integration, task/document relationships
   - Multiple TODOs indicate unfinished features
   
2. **`src/storage/vector_db.py`** - 122 lines, 0% coverage
   - ChromaDB integration
   - Vector store index management
   - Chat engine configuration

3. **`src/storage/data_ingestion.py`** - 88 lines, 0% coverage
   - Document loading and processing
   - Ingestion pipeline management
   - Cache setup

#### 🟡 High (Medium Complexity)
4. **`src/role/llm_client.py`** - 50 lines, 0% coverage
   - LLM Studio client integration
   - Chat completion streaming
   - System prompt handling

5. **`src/storage/chat_repository.py`** - 50 lines, 0% coverage
   - Redis-based chat storage
   - Session management

6. **`src/ui/datastructures.py`** - 44 lines, 0% coverage
   - Task and Document dataclasses
   - RelatedTasks and RelatedDocuments containers

7. **`src/settings.py`** - 37 lines, 0% coverage
   - Application configuration
   - LLM, embedding, and text splitter setup

#### 🟢 Medium (Lower Complexity)
8. **`src/storage/custom_transformations.py`** - 27 lines, 0% coverage
   - Text cleaning
   - Metadata transformation

9. **`src/storage/custom_embedding_clients/lm_studio_client.py`** - 78 lines, 0% coverage
   - Custom embedding implementation

10. **`src/role/prompt_repository/prompt_builder.py`** - 22 lines, 0% coverage
    - Prompt loading and management

11. **`src/api/main.py`** - 30 lines, 0% coverage
    - FastAPI healthcheck endpoints

12. **`src/ui/main.py`** - 67 lines, 0% coverage
    - Gradio UI construction

---

## 🎯 Quality Gateway Requirements

### Phase 1: Immediate (Must Have)

#### 1. Code Quality Checks
- [ ] **Flake8** - PEP 8 compliance
- [ ] **Black** - Code formatting
- [ ] **isort** - Import sorting
- [ ] **mypy** - Type checking
- [ ] **Bandit** - Security scanning

#### 2. Test Coverage Gates
- [ ] **Minimum 80% coverage** for new PRs
- [ ] **No uncovered critical paths** (chat_manager, vector_db, data_ingestion)
- [ ] **Branch coverage** reporting

#### 3. Pre-commit Hooks
- [ ] Auto-formatting on commit
- [ ] Linting checks
- [ ] Type checking

### Phase 2: Short-term (Should Have)

#### 4. Unit Tests
- [ ] **ChatManager** - 100% coverage
- [ ] **VectorStoreIndexManager** - 100% coverage
- [ ] **DataIngestionManager** - 100% coverage
- [ ] **LLMClient** - 100% coverage
- [ ] **ChatRepository** - 100% coverage
- [ ] **All datastructures** - 100% coverage

#### 5. Integration Tests
- [ ] Redis connection tests
- [ ] ChromaDB integration tests
- [ ] API endpoint tests
- [ ] Data ingestion pipeline tests

#### 6. Mocking Strategy
- [ ] Mock external dependencies (Redis, ChromaDB, LMStudio)
- [ ] Use pytest fixtures for common test scenarios
- [ ] Factory patterns for test data generation

### Phase 3: Long-term (Nice to Have)

#### 7. Advanced Testing
- [ ] Property-based testing (Hypothesis)
- [ ] Performance testing
- [ ] Load testing for API endpoints
- [ ] End-to-end UI tests

#### 8. Documentation
- [ ] Test documentation
- [ ] Code review checklists
- [ ] Architecture decision records (ADRs)

---

## 🔧 Implementation Plan

### Step 1: Update CI Workflow (Immediate)

Create `.github/workflows/quality-gateway.yml` with:
- Linting (flake8, black, isort)
- Type checking (mypy)
- Security scanning (bandit)
- Test coverage enforcement
- Coverage reporting (Codecov integration)

### Step 2: Add Pre-commit Configuration

Create `.pre-commit-config.yaml` with:
- black
- flake8
- isort
- mypy
- bandit

### Step 3: Create Test Infrastructure

1. **`tests/conftest.py`** - Enhanced with fixtures:
   - Mock Redis client
   - Mock ChromaDB client
   - Mock LLM Studio client
   - Test data factories

2. **`tests/factories.py`** - Test data generation:
   - Task factory
   - Document factory
   - Chat message factory
   - LLMConfig factory

### Step 4: Write Unit Tests

Create test files for each module:
- `tests/role/test_chat_manager.py`
- `tests/role/test_llm_client.py`
- `tests/storage/test_chat_repository.py`
- `tests/storage/test_vector_db.py`
- `tests/storage/test_data_ingestion.py`
- `tests/ui/test_datastructures.py`
- `tests/api/test_main.py`
- `tests/test_settings.py`

### Step 5: Add Integration Tests

- `tests/integration/test_redis_integration.py`
- `tests/integration/test_chroma_integration.py`
- `tests/integration/test_api_endpoints.py`

### Step 6: Configure Coverage

Update `pyproject.toml` with:
- Coverage thresholds
- Exclude patterns
- Reporting configuration

---

## 📋 Test File Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures and configuration
├── factories.py             # Test data factories
├── unit/                    # Unit tests
│   ├── __init__.py
│   ├── test_datastructures.py  # Existing
│   ├── role/
│   │   ├── __init__.py
│   │   ├── test_chat_manager.py
│   │   ├── test_llm_client.py
│   │   └── test_prompt_builder.py
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── test_chat_repository.py
│   │   ├── test_vector_db.py
│   │   ├── test_data_ingestion.py
│   │   └── test_custom_transformations.py
│   ├── ui/
│   │   ├── __init__.py
│   │   └── test_datastructures.py
│   └── api/
│       ├── __init__.py
│       └── test_main.py
├── integration/             # Integration tests
│   ├── __init__.py
│   ├── test_redis_integration.py
│   ├── test_chroma_integration.py
│   └── test_api_endpoints.py
└── e2e/                     # End-to-end tests (future)
    ├── __init__.py
    └── test_ui_flow.py
```

---

## 🎯 Coverage Targets

### Minimum Acceptable Coverage
| Module | Current | Target | Priority |
|--------|---------|--------|----------|
| `role/chat_manager.py` | 0% | 100% | Critical |
| `storage/vector_db.py` | 0% | 100% | Critical |
| `storage/data_ingestion.py` | 0% | 100% | Critical |
| `role/llm_client.py` | 0% | 100% | High |
| `storage/chat_repository.py` | 0% | 100% | High |
| `ui/datastructures.py` | 0% | 100% | High |
| `settings.py` | 0% | 100% | High |
| All other modules | 0% | 100% | Medium |
| **Overall** | **2%** | **80%** | **Critical** |

### Coverage Enforcement
- **New PRs**: Must not decrease overall coverage
- **Critical modules**: Must have 100% coverage before merge
- **Branch coverage**: Minimum 70%

---

## 🔍 Code Quality Standards

### Flake8 Configuration
```ini
[flake8]
max-line-length = 88
exclude = .venv,venv,.git,__pycache__,migrations
ignore = E203,W503
max-complexity = 10
```

### Black Configuration
```toml
[tool.black]
line-length = 88
target-version = ['py312']
```

### isort Configuration
```toml
[tool.isort]
profile = "black"
line_length = 88
```

### mypy Configuration
```toml
[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
```

---

## 🚦 CI/CD Quality Gates

### Required Checks (All must pass)
1. ✅ All unit tests pass
2. ✅ Coverage >= 80% (or no decrease from main)
3. ✅ Flake8 passes (no violations)
4. ✅ Black formatting verified
5. ✅ isort import sorting verified
6. ✅ mypy type checking passes
7. ✅ Bandit security scan passes

### Optional Checks
1. Codecov coverage reporting
2. SonarCloud analysis
3. Test mutation coverage

---

## 📝 Testing Guidelines

### Unit Test Requirements
- Each function must have at least one test
- Test happy paths, edge cases, and error conditions
- Use mocking for external dependencies
- Tests should be fast (< 1 second each)
- Tests should be isolated (no shared state)

### Integration Test Requirements
- Test real service interactions
- Use test containers for databases
- Test API endpoints with real HTTP requests
- Can be slower but must be reliable

### Test Naming Convention
```python
# Function: function_name
# Test: test_function_name_[scenario]

def test_chat_manager_predict_empty_query():
    """Test predict with empty query returns error."""
    pass

def test_chat_manager_predict_with_valid_query():
    """Test predict with valid query returns stream."""
    pass
```

---

## 🛠️ Tools & Dependencies

### Testing
```toml
[tool.poetry.group.dev.dependencies]
pytest = "^9.1.1"
pytest-cov = "^5.0.0"
pytest-mock = "^3.14.0"
hypothesis = "^6.100.0"
factory-boy = "^3.3.0"
```

### Linting & Formatting
```toml
[tool.poetry.group.dev.dependencies]
flake8 = "^7.0.0"
black = "^24.0.0"
isort = "^5.13.0"
mypy = "^1.10.0"
bandit = "^1.7.8"
```

### Pre-commit
```toml
[tool.poetry.group.dev.dependencies]
pre-commit = "^3.7.0"
```

---

## 📅 Timeline

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| Phase 1 | 1 week | CI updates, pre-commit hooks, basic linting |
| Phase 2 | 2 weeks | Unit tests for critical modules (80% coverage) |
| Phase 3 | 1 week | Integration tests, coverage enforcement |
| Phase 4 | Ongoing | Maintain coverage, add new tests with features |

---

## 🎓 Best Practices

### 1. Test-Driven Development (TDD)
- Write tests before implementation
- Red, Green, Refactor cycle
- Ensures testable code design

### 2. Mocking Strategy
- Mock external services at boundaries
- Use `pytest-mock` for simple mocks
- Use `unittest.mock` for complex scenarios
- Never mock what you don't own

### 3. Test Isolation
- Each test should be independent
- Use fixtures for common setup
- Clean up after each test
- Avoid global state

### 4. Test Performance
- Unit tests should run in < 1 second
- Integration tests should run in < 10 seconds
- Use `@pytest.mark.slow` for slower tests
- Run slow tests separately in CI

### 5. Test Maintainability
- Keep tests simple and readable
- One assertion per test (when possible)
- Use descriptive test names
- Document complex test scenarios

---

## 📊 Success Metrics

1. **Coverage**: 80%+ overall, 100% for critical modules
2. **Test Count**: Minimum 100 tests
3. **CI Pass Rate**: 100% for main branch
4. **PR Review Time**: < 24 hours (with quality gates)
5. **Bug Escape Rate**: < 5% of bugs reach production

---

## 🔗 References

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Black Documentation](https://black.readthedocs.io/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Factory Boy](https://factoryboy.readthedocs.io/)
- [Hypothesis](https://hypothesis.readthedocs.io/)

---

## ✅ Next Steps

1. **Immediate** (This PR):
   - [ ] Create `.github/workflows/quality-gateway.yml`
   - [ ] Create `.pre-commit-config.yaml`
   - [ ] Update `pyproject.toml` with dev dependencies
   - [ ] Create basic test infrastructure

2. **Short-term** (Next 2 weeks):
   - [ ] Write unit tests for critical modules
   - [ ] Achieve 80% coverage
   - [ ] Set up Codecov integration

3. **Long-term** (Ongoing):
   - [ ] Maintain coverage standards
   - [ ] Add integration tests
   - [ ] Implement mutation testing
   - [ ] Add performance tests

---

*Document created: 2024*
*Last updated: 2024*
*Owner: Engineering Team*
