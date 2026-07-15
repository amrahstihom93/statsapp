# Phase 1: Django & Dependency Upgrade (Parallel Environment)

## Overview
The goal of this phase is to modernize the `statsapp` codebase from Django 2.1 to Django 4.2 LTS and update all associated data science libraries. We will use a **Parallel Modern Environment** approach to ensure a clean migration without carrying over technical debt. We will also produce comprehensive platform documentation.

## Architecture & Scaffolding
- **Target Stack:** Python 3.11, Django 4.2 LTS, latest stable Pandas, SciPy, NumPy, Scikit-learn.
- **Project Structure:** A new directory named `modern_app/` will be scaffolded within the repository alongside the existing legacy code.
- **Dependency Management:** A fresh `requirements.txt` will be created from scratch. Only strictly required and modern packages will be added. Abandoned packages (e.g., `django-angular`) will be evaluated and dropped or replaced.

## Code Migration & Adaptation
- **Migration Strategy:** Apps will be ported one by one in order of dependency and complexity (e.g., core/utilities -> `accounts` -> `statistical` -> `mlearn` -> `charts`).
- **Code Modernization Guidelines:**
  - Update `url()` routing to `path()`/`re_path()`.
  - Ensure all `ForeignKey` definitions have explicit `on_delete` behaviors.
  - Refactor data processing logic to align with any deprecated or changed APIs in modern Pandas and SciPy.
- **Documentation:** We will generate comprehensive documentation covering the platform's architecture, setup instructions, and feature flows as part of the final deliverables.

## Testing & Verification
- **Ground Truth:** The existing Django 2.1 environment will remain intact and serve as the behavioral reference.
- **Validation:** As each app is migrated, unit tests will be written in the `modern_app/` environment. These tests will verify that the statistical and mathematical outputs (e.g., using `xbarrange.csv`) exactly match the legacy system's outputs.

## Out of Scope (For this phase)
- Complete UI/UX redesign (Phase 3).
- Adding major new features.
