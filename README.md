# Local JWT Auth API

A secure backend API built with FastAPI and Python, utilizing JSON Web Tokens (JWT) and bcrypt password hashing for user authentication and route protection.

## 🚀 Features
* **User Signup (`POST /auth/signup`)**: Registers a new user with encrypted password storage.
* **User Login (`POST /auth/login`):** Authenticates credentials and returns a secure JWT `access_token`.
* **Public Endpoint (`GET /public/info`):** Open to all unauthenticated users.
* **Protected Endpoint (`GET /protected/profile`):** Requires a valid Bearer Token in the authorization header.
* **User Logout (`POST /auth/logout`):** Terminates the user session.
* **Interactive Documentation:** Built-in Swagger UI with Bearer Token authorization support.

---

## 🛠️ Setup & Installation

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR-USERNAME/YOUR-REPOSITORY-NAME.git](https://github.com/YOUR-USERNAME/YOUR-REPOSITORY-NAME.git)
cd YOUR-REPOSITORY-NAME
