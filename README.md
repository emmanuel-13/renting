# 🏠 Rent4Less

Rent4Less is a **Django-based property rental platform** designed to make housing more accessible and flexible for both tenants and landlords. It provides users with an intuitive interface to **search, explore, and rent apartments** on a **monthly payment basis**, while landlords can **list and manage properties** effortlessly.

---

## Features

### For Tenants
- Browse thousands of verified properties.
- Pay rent monthly — no agency or commission fees.
- Search apartments by city or location.
- View top property deals and discounts.
- Register and manage personal accounts.

### For Landlords
- List properties with images, descriptions, and pricing.
- Participate in the **Guaranteed Rental Income Programme (GRIP)**.
- Earn consistent income while Rent4Less handles tenant verification and property maintenance.

### General Platform Features
- Responsive, modern frontend design built with **HTML, CSS, and Swiper.js**.
- Interactive search and filtering.
- Lazy image loading for improved performance.
- Toast notifications and loading spinners for smoother UX.
- Dynamic estate and featured property sections using Django template logic.

---

## Tech Stack

| Category | Technology |
|-----------|-------------|
| Backend | Django (Python) |
| Frontend | HTML5, CSS3, JavaScript |
| UI Libraries | Boxicons, Swiper.js |
| Database | SQLite / PostgreSQL (configurable) |
| Templating | Django Template Language |
| Version Control | Git & GitHub |

---

## Installation & Setup

Follow these steps to run Rent4Less locally:

```bash
# 1️⃣ Clone the repository
git clone https://github.com/yourusername/rent4less.git
cd rent4less

# 2️⃣ Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run database migrations
python manage.py migrate

# 5️⃣ Start the development server
python manage.py runserver
