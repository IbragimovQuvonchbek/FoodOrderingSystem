
---

# Golden Burgers - Developer README

## Project Overview

**Golden Burgers** is a Django-based web application designed for a burger restaurant to allow customers to view menus, add items to a cart, place orders online, and for admins to manage products and orders.

---

## Features

* Customer-facing menu browsing and ordering
* Shopping cart functionality with quantity management
* Online order placement with customer details
* Admin panel for product and order management
* User roles: customers and admins

---

## Technologies Used

* Python 3.10+
* Django3.x
* SQLite (default) or PostgreSQL (optional)
* HTML, CSS, JavaScript for frontend
* Bootstrap (optional) for styling
* Git for version control

---

## Getting Started

### Prerequisites

* Python 3.10 or higher installed
* Git installed
* Virtual environment tool (venv or similar)

### Clone the Repository

```bash
git clone https://github.com/yourusername/golden-burgers.git
cd golden-burgers
```

### Set up Virtual Environment and Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Database Setup

* By default, the app uses SQLite. To use PostgreSQL or another DB, update `settings.py` accordingly.

* Run migrations to create database tables:

```bash
python manage.py migrate
```

### Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow prompts to create admin credentials.

### Run the Development Server

```bash
python manage.py runserver
```

Open your browser and go to `http://127.0.0.1:8000/` to access the app.

---

## Running Tests

To run unit and integration tests:

```bash
python manage.py test
```

---

## Project Structure

```
golden-burgers/
│
├── golden_burgers/       # Django project settings and config
├── menu/                 # App managing menu items and orders
├── templates/            # HTML templates
├── static/               # CSS, JS, images
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## Environment Variables

(Optional) You can use environment variables for sensitive settings, e.g., secret key, database credentials. Configure `.env` and use `python-decouple` or similar.

---

## Contributing

Feel free to fork the repo and submit pull requests. Please follow the existing code style and write tests for new features.

---

## Contact

For questions or support, contact the project maintainer:
Ibragimov Quvonchbek — [1.quvonchbek.ibragimov@gmail.com](mailto:your.email@example.com)

---

