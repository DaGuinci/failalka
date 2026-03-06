---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-02b-vision', 'step-02c-executive-summary']
inputDocuments:
  - 'docs/index.md'
  - 'docs/project-overview.md'
  - 'docs/architecture.md'
  - 'docs/data-models.md'
  - 'docs/api-contracts.md'
  - 'docs/development-guide.md'
  - 'docs/deployment-guide.md'
  - 'docs/source-tree-analysis.md'
  - '_bmad-output/project-context.md'
documentCounts:
  briefs: 0
  research: 0
  brainstorming: 0
  projectDocs: 8
classification:
  projectType: web_app
  domain: scientific
  complexity: medium
  projectContext: brownfield
scope:
  inScope:
    - Pages de consultation enrichies (filtres, cartes, galeries)
    - Formulaires de création entités (validators/admins)
    - Soumission de commentaires (visitors)
    - Configuration Django Admin
    - Choix de stack frontend interactive (htmx/Alpine, Vue composants, ou autre)
  deferredFeatures:
    - Notifications aux validateurs
    - Demandes de téléchargement HD
    - Sélection d'articles pour demandes groupées
workflowType: 'prd'
---

# Product Requirements Document - Failaka

**Author:** Sensei
**Date:** 2026-03-06

## Executive Summary

Failaka is a web platform for storing, managing, and publicly showcasing digitized archaeological resources from the island of Failaka (Kuwait). As field artifacts and documentation risk being lost to neglect, ongoing digitization efforts need a reliable, accessible repository — one that serves both the contributing research teams and the broader community of scholars, students, and curious visitors.

The platform is built on an existing Django/DRF REST API with JWT authentication and a role-based workflow: administrators and validators create and publish resources, while the public freely browses sites, subsites, items, missions, and notable discoveries. The immediate goal is to complete the client-facing web interface — transforming a functional but headless API into a polished, content-rich experience.

Target audience spans from domain specialists (archaeologists, historians, researchers) to the general public interested in cultural heritage. The platform must accommodate high volumes of scientific content (photos, field reports, mission logs) without sacrificing navigability or visual appeal.

### What Makes This Special

- **Pragmatic alternative to institutional platforms** — Solutions like HumaNum/Nakala impose heavyweight metadata standards that field teams rarely follow. Failaka provides structured cataloguing without the bureaucratic overhead, making data actually get shared instead of buried.
- **Visual exploration over dry catalogues** — The interface is designed to make browsing an archaeological site feel like navigating a modern documentary, not scrolling through a spreadsheet. Maps, image galleries, contextual navigation, and filters turn raw data into an engaging experience.
- **Built for scientific volume** — Archaeologists produce large quantities of heterogeneous content. The UI must remain elegant and performant whether a site has 10 items or 10,000.
- **Quality-gated publishing** — Only validators can publish content, ensuring data reliability without requiring every contributor to master complex cataloguing rules.

## Project Classification

- **Project Type:** Web Application (server-rendered with progressive interactivity)
- **Domain:** Scientific — Archaeological resource management and public consultation
- **Complexity:** Medium — Established data model and API, focused on completing the client layer with rich UI features (maps, filters, galleries, forms)
- **Project Context:** Brownfield — Fully functional REST API, authentication system, and data models in place. Work focuses on the client-side experience.
