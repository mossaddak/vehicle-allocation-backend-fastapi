# Vehicle Allocation System

This project is a FastAPI-based vehicle allocation system that allows employees to allocate vehicles for a specific day, ensuring that a vehicle can only be allocated once per day. The system includes employee and vehicle management, and provides CRUD operations for vehicle allocations, with appropriate business logic constraints.

## API Document
```
    http://127.0.0.1:8000/docs
```

---

**Setting up a virtualenv**

    cd ~
    python3 -m venv env
    source ~/env/bin/activate
    source venv/bin/
    
**Build and run the project using Docker Compose**

    docker-compose up --build
    http://127.0.0.1:5000/docs


**Install the dependencies**

    pip install -r requirements/development.txt

**Run the development server**

    uvicorn index:app --reload

You can now visit 127.0.0.1:8000 on your browser and see that the project is running.

---
