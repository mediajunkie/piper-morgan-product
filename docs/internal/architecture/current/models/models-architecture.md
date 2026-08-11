# Models Architecture

**Last Updated**: September 18, 2025
**Source**: `services/domain/models.py`
**Total Models**: 39 (38 dataclass models + 1 enum)
**Architecture**: Hub-and-spoke documentation by technical layers

## Navigation Hub

### 🗂️ By Technical Layer
Navigate by architectural concern and DDD purity level:

- **[Pure Domain Models](pure-domain.md)** (8 models)
  Business concepts with no infrastructure dependencies

- **[Supporting Domain Models](supporting-domain.md)** (7 models)
  Business concepts requiring data structures or complex state

- **[Integration & Transfer Models](integration.md)** (16 models)
  External system contracts, DTOs, data transfer objects, and enums

- **[Infrastructure Models](infrastructure.md)** (8 models)
  System mechanisms, events, and technical concerns

### 🏷️ By Business Function
Navigate by business capability and domain area:

- **[#pm - Product Management](#pm-models)** (12 models)
  Products, features, stakeholders, work items, projects

- **[#workflow - Process Orchestration](#workflow-models)** (5 models)
  Workflows, tasks, intents, results, execution

- **[#knowledge - Information Management](#knowledge-models)** (9 models)
  Documents, summaries, knowledge graphs, analysis

- **[#spatial - Spatial Intelligence](#spatial-models)** (5 models)
  Spatial metaphor, events, objects, context, navigation

- **[#ai - AI Enhancement](#ai-models)** (3 models)
  Humanization, insights, confidence scoring

- **[#ethics - Safety & Boundaries](#ethics-models)** (2 models)
  Ethical decisions, boundary violations, safety

- **[#system - Infrastructure](#system-models)** (10 models)
  Events, lists, todos, conversations, system tracking

- **[#integration - External Systems](#integration-models)** (6 models)
  GitHub, Jira, external tool integrations

- **[#files - File Management](#files-models)** (4 models)
  Upload, validation, type detection, processing

### 🔤 Alphabetical Quick Lookup
[A](#a) [B](#b) [C](#c) [D](#d) [E](#e) [F](#f) [I](#i) [K](#k) [L](#l) [P](#p) [S](#s) [T](#t) [U](#u) [V](#v) [W](#w)

#### A
- [ActionHumanization](supporting-domain.md#actionhumanization) - AI text enhancement
- [AnalysisResult](integration.md#analysisresult) - Document analysis results

#### B
- [BoundaryViolation](pure-domain.md#boundaryviolation) - Safety boundary events

#### C
- [ContentSample](integration.md#contentsample) - Content for analysis
- [Conversation](infrastructure.md#conversation) - User-AI conversation
- [ConversationTurn](infrastructure.md#conversationturn) - Single conversation exchange

#### D
- [Document](supporting-domain.md#document) - Document memory system entity
- [DocumentSample](integration.md#documentsample) - Extracted document samples
- [DocumentSummary](integration.md#documentsummary) - Document summaries

#### E
- [EthicalDecision](pure-domain.md#ethicaldecision) - Recorded ethical decisions
- [Event](infrastructure.md#event) - Base event class

#### F
- [Feature](pure-domain.md#feature) - Product capabilities
- [FeatureCreated](infrastructure.md#featurecreated) - Feature creation events
- [FileTypeInfo](integration.md#filetypeinfo) - File type detection

#### I
- [Intent](pure-domain.md#intent) - User intent classification
- [InsightGenerated](infrastructure.md#insightgenerated) - AI insights

#### K
- [KnowledgeEdge](supporting-domain.md#knowledgeedge) - Knowledge graph relationships
- [KnowledgeNode](supporting-domain.md#knowledgenode) - Knowledge graph concepts

#### L
- [List](infrastructure.md#list) - User-created lists
- [ListItem](infrastructure.md#listitem) - List items
- [ListMembership](infrastructure.md#listmembership) - List permissions

#### P
- [Product](pure-domain.md#product) - Products being managed
- [Project](integration.md#project) - PM projects with integrations
- [ProjectContext](integration.md#projectcontext) - Workflow context
- [ProjectIntegration](integration.md#projectintegration) - Tool configurations

#### S
- [Stakeholder](pure-domain.md#stakeholder) - Product stakeholders
- [SpatialContext](supporting-domain.md#spatialcontext) - Spatial navigation context
- [SpatialEvent](supporting-domain.md#spatialevent) - Spatial metaphor events
- [SpatialObject](supporting-domain.md#spatialobject) - Spatial environment objects
- [SummarySection](integration.md#summarysection) - Document summary sections

#### T
- [Task](pure-domain.md#task) - Workflow tasks
- [Todo](infrastructure.md#todo) - Todo items
- [TodoList](infrastructure.md#todolist) - Todo collections

#### U
- [UploadedFile](integration.md#uploadedfile) - File uploads

#### V
- [ValidationResult](integration.md#validationresult) - File validation results

#### W
- [WorkflowResult](pure-domain.md#workflowresult) - Workflow execution results
- [Workflow](pure-domain.md#workflow) - Workflow definitions
- [WorkItem](integration.md#workitem) - External work items

---

## Architecture Overview

### Layer Distribution

| Layer | Count | Primary Functions | DDD Purity |
|-------|-------|-------------------|------------|
| Pure Domain | 8 | Business rules and concepts | ⚠️ Highest - No infrastructure |
| Supporting Domain | 7 | Business with data needs | ⚠️ High - Minimal infrastructure |
| Integration & Transfer | 16 | External contracts and enums | ⚠️ Medium - External dependencies |
| Infrastructure | 8 | System mechanisms | ⚠️ Low - Technical concerns |

### Business Function Coverage

| Tag | Model Count | Percentage | Primary Layer |
|-----|-------------|------------|---------------|
| #pm | 12 | 31.6% | Mixed (Pure + Integration) |
| #system | 10 | 26.3% | Infrastructure |
| #knowledge | 9 | 23.7% | Supporting + Integration |
| #workflow | 5 | 13.2% | Pure Domain |
| #spatial | 5 | 13.2% | Supporting Domain |
| #integration | 6 | 15.8% | Integration |
| #files | 4 | 10.5% | Integration |
| #ai | 3 | 7.9% | Mixed |
| #ethics | 2 | 5.3% | Pure Domain |

*Note: Some models have multiple tags, percentages sum > 100%*

---

## Business Function Views

### #pm Models
**Product Management Domain** - Managing products, features, stakeholders, and work items

| Model | Layer | Purpose | File |
|-------|-------|---------|------|
| [Product](pure-domain.md#product) | Pure Domain | Core product entity | pure-domain.md |
| [Feature](pure-domain.md#feature) | Pure Domain | Product capabilities | pure-domain.md |
| [Stakeholder](pure-domain.md#stakeholder) | Pure Domain | People with product interest | pure-domain.md |
| [WorkItem](integration.md#workitem) | Integration | External work tracking | integration.md |
| [Project](integration.md#project) | Integration | PM workspace | integration.md |
| [ProjectIntegration](integration.md#projectintegration) | Integration | Tool configurations | integration.md |
| [ProjectContext](integration.md#projectcontext) | Integration | Workflow context | integration.md |

### #workflow Models
**Process Orchestration** - Managing workflows, tasks, and execution

| Model | Layer | Purpose | File |
|-------|-------|---------|------|
| [Intent](pure-domain.md#intent) | Pure Domain | User intent classification | pure-domain.md |
| [Task](pure-domain.md#task) | Pure Domain | Individual workflow tasks | pure-domain.md |
| [Workflow](pure-domain.md#workflow) | Pure Domain | Workflow definitions | pure-domain.md |
| [WorkflowResult](pure-domain.md#workflowresult) | Pure Domain | Execution results | pure-domain.md |

### #knowledge Models
**Information Management** - Documents, analysis, and knowledge graphs

| Model | Layer | Purpose | File |
|-------|-------|---------|------|
| [Document](supporting-domain.md#document) | Supporting | Document memory system | supporting-domain.md |
| [KnowledgeNode](supporting-domain.md#knowledgenode) | Supporting | Knowledge graph concepts | supporting-domain.md |
| [KnowledgeEdge](supporting-domain.md#knowledgeedge) | Supporting | Knowledge relationships | supporting-domain.md |
| [DocumentSample](integration.md#documentsample) | Integration | Document processing | integration.md |
| [ContentSample](integration.md#contentsample) | Integration | Content analysis | integration.md |
| [AnalysisResult](integration.md#analysisresult) | Integration | Analysis outputs | integration.md |
| [SummarySection](integration.md#summarysection) | Integration | Summary structure | integration.md |
| [DocumentSummary](integration.md#documentsummary) | Integration | Document summaries | integration.md |

### #spatial Models
**Spatial Intelligence** - Spatial metaphor system for navigation and context

| Model | Layer | Purpose | File |
|-------|-------|---------|------|
| [SpatialEvent](supporting-domain.md#spatialevent) | Supporting | Spatial metaphor events | supporting-domain.md |
| [SpatialObject](supporting-domain.md#spatialobject) | Supporting | Spatial environment objects | supporting-domain.md |
| [SpatialContext](supporting-domain.md#spatialcontext) | Supporting | Spatial navigation context | supporting-domain.md |

### #ai Models
**AI Enhancement** - AI-generated insights and humanization

| Model | Layer | Purpose | File |
|-------|-------|---------|------|
| [Intent](pure-domain.md#intent) | Pure Domain | User intent classification | pure-domain.md |
| [ActionHumanization](supporting-domain.md#actionhumanization) | Supporting | AI text enhancement | supporting-domain.md |
| [InsightGenerated](infrastructure.md#insightgenerated) | Infrastructure | AI-generated insights | infrastructure.md |

### #ethics Models
**Ethics & Safety** - Ethical decisions and boundary violations

| Model | Layer | Purpose | File |
|-------|-------|---------|------|
| [EthicalDecision](pure-domain.md#ethicaldecision) | Pure Domain | Recorded ethical decisions | pure-domain.md |
| [BoundaryViolation](pure-domain.md#boundaryviolation) | Pure Domain | Safety boundary events | pure-domain.md |

---

## Layer Summaries

### Pure Domain Models
⚠️ **DDD Purity Warning**: Models in this layer must have NO infrastructure dependencies, NO database concerns, and NO external system references. These represent pure business concepts and rules.

**8 models** representing core business domain: Product management (Product, Feature, Stakeholder), workflow orchestration (Intent, Task, Workflow, WorkflowResult), and ethical decision making (EthicalDecision, BoundaryViolation).

**[View detailed specifications →](pure-domain.md)**

### Supporting Domain Models
⚠️ **DDD Purity Warning**: Models in this layer represent business concepts but require data structures, complex state, or specialized methods. Minimal infrastructure acceptable.

**7 models** supporting business capabilities: Document memory system (Document), spatial intelligence (SpatialEvent, SpatialObject, SpatialContext), knowledge graphs (KnowledgeNode, KnowledgeEdge), and AI enhancement (ActionHumanization).

**[View detailed specifications →](supporting-domain.md)**

### Integration & Transfer Models
⚠️ **DDD Purity Warning**: Models in this layer handle external system contracts and data transfer. External dependencies expected but should be contained.

**16 models** managing external integration: Work item synchronization (WorkItem), project configuration (Project, ProjectIntegration, ProjectContext), file handling (UploadedFile, ValidationResult, FileTypeInfo), document processing (DocumentSample, ContentSample, AnalysisResult, SummarySection, DocumentSummary), and analysis enums (AnalysisType).

**[View detailed specifications →](integration.md)**

### Infrastructure Models
⚠️ **DDD Purity Warning**: Models in this layer support system operations and technical concerns. Full infrastructure dependencies acceptable.

**8 models** providing system capabilities: Event tracking (Event, FeatureCreated, InsightGenerated), list management (List, ListItem, ListMembership), task tracking (Todo, TodoList), and conversation logging (Conversation, ConversationTurn).

**[View detailed specifications →](infrastructure.md)**

---

## Related Documentation

- **[Pure Domain Models](pure-domain.md)** - Core business concepts
- **[Supporting Domain Models](supporting-domain.md)** - Business with data needs
- **[Integration Models](integration.md)** - External system contracts
- **[Infrastructure Models](infrastructure.md)** - System mechanisms
- **[Data Model Documentation](../data-model.md)** - Database persistence
- **Schema Validator *(proposed; doc TBD)*** - Validation tools

---

## Migration from domain-models.md

This hub-and-spoke architecture replaces the outdated `domain-models.md` with current model documentation reflecting all 38 models in `services/domain/models.py`.

### What's Changed
- **Added**: 18 new models not previously documented
- **Updated**: All field definitions to match current implementation
- **Reorganized**: By technical layers with detailed spoke documents
- **Enhanced**: Added business function navigation and cross-references

### Finding Models
- **Old location**: `domain-models.md#[model-name]`
- **New location**: `models/[layer].md#[model-name]`
- **Quick lookup**: Use alphabetical index above

---

**Status**: ✅ **CURRENT** - All models documented with complete field definitions and architectural context
