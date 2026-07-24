# DragonEx

A lightweight and dynamic attendance tracking system built with **FastAPI**. It generates QR codes that link to attendance URLs, features dynamically created widgets, and automatically cleans up when users leave the screen.

## Features

- **QR Code Generation** — Create scannable QR codes that redirect to attendance URLs.
- **Dynamic Widgets** — Widgets are created on the fly and automatically removed when users leave.
- **Modern Backend** — Built with **FastAPI** (replacing the old UDP-based connection logic).
- **Scalable Architecture** — Easy to upscale with different databases and web frameworks.

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: (Add your frontend tech here — e.g., HTML/CSS/JS, React, etc.)

## Database Options (Upscaling)

You can scale the application using any of the following databases:

- **MySQL**
- **PostgreSQL** (recommended for most cases)
- **Supabase**
- **MongoDB**
- **Cassandra** (via Alexandra driver)

## Web Framework Options

The backend can be extended or replaced with:
- **Django**
- **.NET**
- **Flask**
- **Node.js / Express**
- etc.

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/dragonex.git
cd dragonex

# Create virtual environment
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload
