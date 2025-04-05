
```markdown
# 📱 Django Social Media API

A high-quality, scalable RESTful Social Media API built with Django and Django REST Framework. This backend powers user authentication, media sharing, following systems, notifications, and more — all ready for frontend integration and future real-time features.


##  Features

- ✅ User Registration, Login & JWT Authentication  
- ✅ Follow/Unfollow System  
- ✅ Post Creation, Editing, Deletion (with Image Uploads)  
- ✅ Like/Unlike Posts & Comments  
- ✅ Commenting on Posts  
- ✅ Real-time Notifications (via polling; WebSocket-ready)  
- ✅ Basic Search for Users & Posts  
- ✅ API Rate Limiting (Throttle classes)  
- ✅ Token Refresh Support  
- ✅ Clean, scalable architecture for future expansion  
- ✅ Password Reset via Email & Email Verification


## 🧱 Tech Stack

- **Backend:** Django, Django REST Framework  
- **Authentication:** JWT via SimpleJWT  
- **Database:** PostgreSQL / SQLite (dev)  
- **Deployment:** PythonAnywhere / Heroku  
- **Others:** Pillow (Image), django-cors-headers, drf-yasg (optional)  


## 🛠️ Installation (Local)

1. **Clone the Repo**
   ```bash
   git clone https://github.com/yourusername/social-media-api.git
   cd social-media-api
   ```

2. **Create & Activate a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run the Server**
   ```bash
   python manage.py runserver
   ```

6. **Create Superuser (Optional)**
   ```bash
   python manage.py createsuperuser
   ```

---

## 🧪 API Testing

You can use:
- **Postman**
- **cURL**
- **DRF's browsable API** (enabled in development)

---

## 📌 API Endpoints (Examples)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | `/api/register/`        | Register a new user         |
| POST   | `/api/token/`           | Login (JWT token)           |
| GET    | `/api/posts/`           | List all posts              |
| POST   | `/api/posts/`           | Create a post               |
| POST   | `/api/follow/<username>/` | Follow a user             |
| POST   | `/api/posts/<id>/like/` | Like a post                 |

---

## 🧠 Future Enhancements
- Image Compression for Media Uploads 
- Real-time Chat & WebSocket support (via Django Channels)  
- Enhanced Admin Dashboard  
- Frontend Integration (React / Flutter)  
- Analytics and Reporting  
- Tagging and Hashtag support  