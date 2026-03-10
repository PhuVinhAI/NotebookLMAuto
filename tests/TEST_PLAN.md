# Research CLI - Comprehensive Test Plan

## 📋 Test Categories

### 1. Core YouTube Functionality Tests
- [x] YouTube client initialization
- [x] Video search (basic, with filters)
- [x] Video filtering (views, duration, date, channel)
- [x] Video sorting (views, date, title, relevance)
- [ ] Video info extraction
- [ ] Subtitle download
- [ ] Error handling (network issues, API limits)

### 2. CLI Commands Tests
- [x] Main CLI help
- [x] Search command help
- [x] Pipeline command help
- [ ] **Search command execution**
- [ ] **Info command execution**
- [ ] **Export command execution**
- [ ] Command validation (missing args, invalid options)

### 3. NotebookLM Integration Tests
- [ ] **Authentication check and auto-login**
- [ ] **Notebook management (create, list, delete)**
- [ ] **Source management (add, list, wait for processing)**
- [ ] **Chat functionality (ask questions, get references)**
- [ ] **Language settings (list, get, set)**
- [ ] **Artifact management (list, wait for completion)**

### 4. Content Generation Tests
- [ ] **Podcast generation (all formats, languages)**
- [ ] **Quiz generation (all difficulties, formats)**
- [ ] **Flashcards generation**
- [ ] **Infographic generation (all orientations)**
- [ ] **Video generation (all styles)**
- [ ] **Slide deck generation (PDF/PPTX)**
- [ ] **Report generation (all formats)**
- [ ] **Mind map generation**
- [ ] **Data table generation**
- [ ] **Slide revision**

### 5. Pipeline Workflow Tests
- [ ] **End-to-end pipeline (YouTube → NotebookLM → Content)**
- [ ] **Multi-content generation**
- [ ] **Language-specific workflows**
- [ ] **Error recovery in pipeline**

### 6. Integration & Error Handling Tests
- [ ] **Network failure handling**
- [ ] **API rate limiting**
- [ ] **Authentication failures**
- [ ] **File I/O errors**
- [ ] **Invalid inputs**

## 🎯 Test Execution Plan

### Phase 1: Core & CLI Tests (CURRENT)
- ✅ Import tests
- ✅ YouTube client tests
- ✅ CLI help tests
- 🔄 CLI execution tests

### Phase 2: NotebookLM Basic Tests
- Auth & setup tests
- Notebook CRUD tests
- Source management tests
- Basic chat tests

### Phase 3: Content Generation Tests
- Individual content type tests
- Format/language variation tests
- Error handling tests

### Phase 4: Pipeline Integration Tests
- End-to-end workflow tests
- Multi-step error recovery
- Performance tests

### Phase 5: Real-world Scenario Tests
- Complete user workflows
- Edge cases
- Load testing

## 📝 Test Files Structure

```
tests/
├── test_core_youtube.py      ✅ (Updated)
├── test_cli_commands.py      🔄 (In Progress)
├── test_notebooklm_auth.py   📝 (To Create)
├── test_notebooklm_crud.py   📝 (To Create)
├── test_content_generation.py 📝 (To Create)
├── test_pipeline_workflows.py 📝 (To Create)
├── test_error_handling.py    📝 (To Create)
├── test_real_scenarios.py    📝 (To Create)
└── run_comprehensive_tests.py 📝 (Master Test Runner)
```

## 🚀 Next Steps

1. **Fix current CLI command tests** (remove pytest dependency)
2. **Create NotebookLM authentication tests**
3. **Create notebook CRUD operation tests**
4. **Create content generation tests**
5. **Create end-to-end pipeline tests**
6. **Create comprehensive test runner**

## 🎯 Success Criteria

- ✅ All imports work correctly
- ✅ YouTube search and filtering work
- ✅ CLI help commands work
- 🎯 All CLI commands execute without errors
- 🎯 NotebookLM authentication works
- 🎯 Notebook operations work (create, list, delete)
- 🎯 Source operations work (add, process, query)
- 🎯 All content generation types work
- 🎯 Pipeline workflows complete successfully
- 🎯 Error handling works gracefully

## 📊 Current Status

**Completed**: 4/7 test categories
**In Progress**: CLI command execution tests
**Next**: NotebookLM integration tests

**Overall Progress**: ~30% complete