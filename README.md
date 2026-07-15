ok

# StatsApp

A modern Web Platform for managing client accounts and user profiles.

## 🚀 Getting Started

*(Documentation on setup will go here)*

## ✨ Features

* [List of major features]

## 💾 Core Data Contracts (API v1)

### User Profile (`/api/v1/profiles/{uuid}`)

This contract handles all data related to a user's profile and client association.

**Model:** `Profile`
**Fields:**

* `user`: `UUID` - The unique identifier for the core Django `User`.
* `phone_number`: `String` - User's registered phone number.
* `email_confirmed`: `Boolean` - Indicates if the user has confirmed their email address (default: false).
* `is_admin`: `Boolean` - Flag indicating administrative privileges for this account.
* `client`: `Object` - Details of the associated organizational client. (See Client details below.)
* `has_seen_tour`: `Boolean` - Indicates if the user has completed the onboarding tour/setup.

### Client Organization (`/api/v1/clients/{client_id}`)

This contract defines the organizational context for a set of users.

**Model:** `ClientList`
**Fields:**

* `client_id`: `String` - The unique client ID.
* `company_name`: `String` - The full registered name of the organization/client.
* `email_id`: `String` - Primary email associated with the client account.

---

## 🖥️ Frontend Component Library & Design System

This section outlines reusable UI components that must be built or updated to achieve a consistent, modern Web Platform look. All new and updated components should adhere to the established design system.

**Core Components:**

* `<Button>`: (Props: `primary/secondary`, `size: sm/md/lg`)
* `<InputGroup>`: Handles field grouping, validation states, and labels for forms.
* `<Card>`: Flexible container component for displaying grouped information snippets (e.g., status boxes).
* `<LayoutShell>`: The main wrapper providing consistent header, sidebar, and content area structure across all pages.

**Key Flows:**

1. **New User Onboarding Flow:** A multi-step wizard guiding new users through initial setup, including client assignment and tour completion (`has_seen_tour` flag). Must be managed via a controlled state machine on the frontend.
2. **Client/Account Management:** Workflow for administrators to create, modify, and assign users to `ClientList` entities. This flow must enforce data integrity checks defined by the backend API.

## 🏗️ Technology Stack & Architecture Choices

The platform is designed using a modern **Hybrid Architecture**:

* **Backend Core:** Django REST Framework (or similar) will act as the central API Gateway, enforcing business logic and exposing structured JSON endpoints (refer to [Core Data Contracts] for details).
* **Frontend Client:** A dedicated Single Page Application (SPA) framework (e.g., React/Vue/Angular) will consume these APIs for dynamic elements, SPA features, and rendering complex interfaces.
* **Rendering Strategy:** We utilize Server-Side Rendering (SSR) via Django templates for high SEO-value pages (like public landing pages), while reserving CSR functionality for all authenticated, dashboard-style interactions.
