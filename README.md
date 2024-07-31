# Chaotix

This Django application uses Celery for asynchronous image generation via the Stability AI Text-to-Image API. It sends parallel requests to create three images based on prompts such as "A red flying dog" and "A piano ninja." The app demonstrates Django and Celery integration, managing tasks with Redis and storing image URLs or metadata in Django models. For setup, follow the instructions to install dependencies, configure Django and Celery, and run the server and workers.



## Installation Guide

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/chittaranjan0275/Chaotix.git
```

### 2. Navigate to the Project Directory

Change to the project directory:

```bash
cd /path/Chaotix/chaotix_ai
```

### 3. Create and Activate the Conda Environment

Create a new Conda environment using the provided environment.yml file:

```bash
conda env create -f environment.yml
```
Activate the environment:

```bash
conda activate chaotic
```

### 4. Apply Database Migrations

In the project directory, run the following commands to apply database migrations:

```bash
python manage.py makemigrations image_generator
python manage.py migrate
```

### 5. Run the Development Server

Start the development server:

```bash
python manage.py runserver
```

### 6.  Start the Celery Worker

Open a new terminal window, navigate to the project directory, and start the Celery worker:

```bash
celery -A chaotix_ai worker --loglevel=info
```
