# Contributing Guide

> **Version**: 2026-07-08
> **Scope**: Software Engineering Architecture Reuse Knowledge System Project

Thank you for your interest in contributing! This guide helps you get started.

---

## 1. Types of Contributions

We welcome the following forms of contribution:

- **Content**: new topics, case studies, positive examples, or anti-patterns
- **Standards alignment**: correcting or updating international standard references
- **Errata**: fixing factual errors, broken links, or formatting issues
- **Tooling improvements**: enhancing health-check, link-checker, standard-tracker, etc.
- **Internationalization**: English summaries, terminology translations, English documents
- **Visualizations**: Mermaid diagrams, architecture diagrams, slide decks

---

## 2. Contribution Workflow

1. **Fork the repository** (if you are an external contributor)
2. **Create a feature branch**: `git checkout -b feature/your-topic`
3. **Modify or add files**: follow `99-reference/book-format-guide.md`
4. **Run health checks**: `python scripts/health-check.py`
5. **Open a PR**: describe the rationale, scope, and authoritative sources

---

## 3. Content Guidelines

### 3.1 File Structure

- Structured content goes in `struct/`
- Aggregated volumes and historical snapshots go in `view/`
- Tool scripts go in `scripts/` or `struct/99-reference/tools/`
- Reports go in `reports/`
- Deliverables go in `dist/`

### 3.2 Markdown Format

- Use ATX headings (`#` instead of `=`)
- Do not exceed 4 heading levels
- Leave blank lines before and after tables
- Use Markdown angle brackets `<https://...>` or `[text](path)` for links

### 3.3 Standards References

- Prefer entries from `struct/99-reference/standards-index/authoritative-sources-v2.md`
- Always provide an official URL
- Clearly distinguish "published", "draft", "initial public draft", and "roadmap"

### 3.4 Terminology

- New terms should be added to `struct/99-reference/glossary/glossary-master.md`
- English terms should also be added to `struct/99-reference/glossary/glossary-bilingual.md`

---

## 4. Quality Gates

Before opening a PR, run:

```bash
python scripts/health-check.py
```

Ensure:

- `struct/` and `view/` quality gates pass at 100%
- No dead links
- Cross-index is consistent
- Template padding check passes

---

## 5. Review Criteria

Maintainers will focus on:

- Whether authoritative sources are official and up-to-date
- Whether there are factual errors
- Whether existing cross-references are broken
- Whether formatting guidelines are followed
- Whether health-check passes

---

## 6. Code of Conduct

- Respect diverse backgrounds and perspectives
- Provide constructive criticism
- Focus on technology and content
- Comply with the project license

---

## 7. Contact

- Open an Issue or Discussion to start a conversation
- For major changes, please open an Issue first to discuss direction

---

> **Last updated**: 2026-07-08
