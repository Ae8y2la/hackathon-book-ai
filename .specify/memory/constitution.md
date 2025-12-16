<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0 (project-specific constitution update)
- Modified principles: All principles revised to match RAG Chatbot for Docusaurus Book requirements
- Added sections: None
- Removed sections: Original Physical AI & Humanoid Robotics specific content
- Templates requiring updates: ✅ updated / ⚠ pending
- Follow-up TODOs: None
-->
# RAG Chatbot for Existing Docusaurus Book Constitution

## Core Principles

### Grounded Answers
All chatbot responses must be strictly grounded in book content retrieved from the indexed documentation. The system must never generate answers based on external knowledge or hallucinate information beyond the provided /docs content.

### Retrieval Accuracy
The RAG system must prioritize source-based retrieval with verifiable citations. All responses must clearly indicate which document sections or pages were used as source material for the generated answer.

### Student Clarity
All chatbot interactions must be optimized for technical students' comprehension. Responses should be clear, well-structured, and avoid unnecessary jargon while maintaining technical precision and accuracy.

### Reproducible Ingestion
The document ingestion pipeline must be deterministic and reproducible. Indexing processes must be version-controlled and repeatable to ensure consistent retrieval quality and debugging capability.

### Backend Engineering Rigor
All backend components must follow production-ready engineering practices. This includes proper error handling, logging, monitoring, asynchronous processing, and clean integration with the existing Docusaurus architecture.

## Quality Standards

- **Zero Hallucination Tolerance**: Chatbot must never fabricate information or respond with content not present in indexed documentation
- **Citation Requirement**: Every response must include proper source citations indicating the specific documents/passages used
- **Selected-Text Mode**: When users provide text selections, responses must be based ONLY on the provided text, not broader document context
- **Backend Reliability**: All API endpoints must be asynchronous, properly error-handled, and meet production service level objectives
- **Performance Standards**: Query responses must meet acceptable latency targets for interactive chat experience
- **Integration Cleanliness**: Backend must integrate seamlessly with existing Docusaurus site without disrupting current functionality

## Development Workflow

- **Scope Boundary**: Chatbot operates exclusively on content from /docs directory, no external knowledge sources allowed
- **RAG Implementation**: System must use appropriate vector storage and retrieval mechanisms for document search
- **Query Modes**: Both full-document search and selected-text query modes must be properly implemented and enforced
- **Quality Assurance**: All responses must be validated against source documents before release
- **Testing Protocol**: Comprehensive testing of retrieval accuracy, citation correctness, and edge cases required
- **Deployment Compatibility**: Solution must deploy cleanly alongside existing Docusaurus site infrastructure

## Governance

This constitution establishes the foundational principles and standards for the RAG Chatbot for Existing Docusaurus Book project. All contributors must adhere to these principles, and any deviations require formal amendment procedures. The constitution serves as the ultimate authority for project decisions, quality standards, and development practices.

All code reviews, content reviews, and project decisions must verify compliance with these principles. Any complexity introduced must be justified by clear benefits to the project's core mission of delivering accurate, citation-backed responses from the existing book content.

**Version**: 1.1.0 | **Ratified**: 2025-12-15 | **Last Amended**: 2025-12-16
