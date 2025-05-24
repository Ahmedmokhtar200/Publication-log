# 📚 Publication Log

A Django-based project for managing and tracking publications, authorship, conferences, project proposals, and events. The system is designed with a normalized relational database schema to maintain data integrity, consistency, and extensibility.

---

## 🗃️ Project Overview

The **Publication Log** system allows users to:

- Track and manage publications associated with research projects.
- Associate publications with authors and conferences.
- Record detailed project proposals, collaborators, and events related to project development and research activities.
- Maintain normalized information about individuals, emails, and actions.

The database was normalized to meet best practices and improve performance and data integrity. This restructuring was necessary due to Django’s historical lack of support for composite primary keys (prior to Django 5.2). The new schema supports full normalization with surrogate keys and join tables.

---

## 🧰 Technologies Used

- **Backend**: [Django](https://www.djangoproject.com/) (Python-based web framework)
- **Database**: MySQL
- **ORM**: Django ORM
- **Frontend**: HTML, CSS (with optional HTMX/JavaScript for dynamic behavior)
- **Containerization**: Docker (for environment setup and isolation)
- **Dev Tools**: Django Admin, Postman (API testing), Visual Studio Code

---

## 📦 Database Structure
![ERD Diagram](./database schema.jpg)

The updated schema includes the following key entities:

### Core Tables:
- **`human`**: Stores system-wide individual records.
- **`human_info`**: Contains personal details (first name, last name, city).
- **`email`**: Email addresses linked to human info.
- **`project`**: Abstract project entity.
- **`project_info`**: Contains descriptive and scientific case details of a project.
- **`proposal`**: Contains proposals related to projects.
- **`publication`**: Links publications with projects and conferences.
- **`conference`**: Stores conference metadata.
- **`publication_author`**: Join table between publications and authors (many-to-many).
- **`collaborator`**: Maps project participants to their emails.
- **`event`**: Tracks actions and success state of operations.
- **`event_proposal`**: Logs the connection between events and proposals.
- **`action`**: Defines types of actions that can be logged (e.g., creation, submission).

Each table is linked with foreign keys and surrogate primary keys for compatibility with Django < 5.2.

---

## 🧠 Normalization Approach

Due to Django's lack of composite primary key support before version 5.2, this project follows a **fully normalized relational model**:

- **Surrogate keys** (`id`) are used across all tables.
- **Many-to-many** relationships are handled with **junction tables** (e.g., `publication_author`).
- All redundant and multivalued attributes are separated into related tables for **Third Normal Form (3NF)** compliance.

---

## 🔮 Future Updates

- I ill Upgrade to **Django 5.2** to leverage native **composite primary key support** and redisgn database schema .
---

## 📌 Setup Instructions

1. Clone the repo
2. Set up virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt

   python manage.py migrate
   python manage.py runserver
  bash```

