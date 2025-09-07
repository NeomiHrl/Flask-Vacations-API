Vacation Manager API – Backend Project

This is a backend-only project built with Python (Flask) for managing a vacation listing platform. The project includes user roles (admin & regular users) and allows interaction with vacation data via REST API tested through Postman.

---

🛠 Technologies
- Python  
- Flask (backend framework)  
- SQLite (Database: mydb)  
- Postman (API testing)  

---

📌 Features
- View Vacations: All users (including guests) can view vacation listings  
- Like/Unlike: Registered users can like and unlike vacations  
- Admin Controls: Admin users can:
  - Add new vacations  
  - Edit existing vacations  
  - Delete vacations  
- Authentication & Roles: Basic permission handling for admin/user  

---

🧪 Testing
All endpoints can be tested via Postman.  
Use the included collection or manually test with:

- GET /vacations  
- POST /login, POST /register  
- POST /vacations (admin)  
- PUT /vacations/<id> (admin)  
- DELETE /vacations/<id> (admin)  
- POST /vacations/<id>/like  
- POST /vacations/<id>/unlike  

---

🔧 Database
- SQL-based database named mydb
- Includes tables for users, vacations, and likes
- Automatically creates tables on first run if they don't exist

---

📌 Status
Backend complete.  
Frontend (React) is under development and will be integrated soon.

