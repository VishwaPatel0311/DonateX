
# 📘 DonateX - Donation Management System

**DonateX** is a backend system for a charitable trust to manage and track user donations efficiently.  
It features:

- 🔐 OTP-based phone authentication  
- 💸 Secure donation processing via PayPal  
- 🧾 Donation history tracking  
- 📊 Data visualization with Streamlit  

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/donateX.git
cd donateX
```

### 2. Create Virtual Environment and Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment

Edit `settings.py` with your config values:

```python
MYSQL_DB_NAME = "db-name"
MYSQL_DB_USER = "user"
MYSQL_DB_PASSWORD = "password"
MYSQL_DB_PORT = "3306"
MYSQL_DB_HOST = "localhost"
WEB_PORT = 14011
PAYPAL_CLIENT_ID = "your-sandbox-client-id"
PAYPAL_CLIENT_SECRET = "your-sandbox-client-secret"
FRONT_END_URL = "localhost:14011"
```

### 4. Setup Database

**Using Alembic:**

```bash
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```


### 5. Start FastAPI Server

```bash
uvicorn main:app --reload
```

### 6. Run Streamlit Dashboard (Optional)

```bash
streamlit run donation_history_graph.py
```

---

## 🔐 Authentication Flow

### Request OTP

```http
POST /auth/request-otp
Content-Type: application/json

{
  "phone": "+1234567890"
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "message": "OTP sent successfully."
  }
}
```

### Verify OTP

```http
POST /auth/verify-otp
Content-Type: application/json

{
  "phone": "+1234567890",
  "otp": "123456"
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "access_token": "jwt_token"
  }
}
```

Add this token to the `Authorization` header:

```
Authorization: Bearer <jwt_token>
```

---

## 💸 Donation Flow

### 1. Create Donation

```http
POST /donate/
Authorization: Bearer <token>
Content-Type: application/json

{
  "amount": 50.0,
  "currency": "USD"
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "client_secret": "PAYID-NAF5XBQ0269364762375060F",
    "approval_url": "https://www.sandbox.paypal.com/checkoutnow?token=XYZ",
    "donation_id": 10
  }
}
```

### 2. Verify Donation

```http
GET /donate/verify
Authorization: Bearer <token>
Content-Type: application/json

{
  "payment_id": "PAYID-xxx",
  "payer_id": "ORDERID-xxx"
}
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "message": "Payment verified successfully."
  }
}
```
### 3. Get Donation List

```http
GET /donate/list  
Authorization: Bearer <token>
```

**Response:**

```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "user_id": 101,
      "payment_id": "PAYID-123",
      "status": "COMPLETED",
      "created_at": "2025-04-10T14:23:45",
      "updated_at": "2025-04-10T15:00:00"
    },
    {
      "id": 2,
      "user_id": 101,
      "payment_id": "PAYID-456",
      "status": "PENDING",
      "created_at": "2025-04-11T09:00:00",
      "updated_at": null
    }
  ]
}
```

---

### 4. Get Donation by ID

```http
GET /donate/{donation_id}  
Authorization: Bearer <token>
```

**Response:**

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "user_id": 101,
    "payment_id": "PAYID-123",
    "status": "COMPLETED",
    "created_at": "2025-04-10T14:23:45",
    "updated_at": "2025-04-10T15:00:00"
  }
}
```

**Failure Response:**

```json
{
  "status": "failure",
  "error": 103,
  "msg": "Donation not found"
}
```

---

## 📊 Payment History Visualization

```http
GET /donation/summary/plot?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```

_Response: Streamed PNG plot image of donation amounts._

---

## 🧱 Project Architecture

```
donateX/
├── app/
│   ├── api/api_v1/endpoints/        # API routes
│   │   ├── auth_apis.py
│   │   └── donate_apis.py
│   ├── core/                        # Common utils and error codes
│   ├── dao/                         # DB access abstraction
│   ├── db/                          # SQLAlchemy setup
│   ├── models/                      # ORM models
│   ├── schemas/                     # Pydantic models
├── donation_history_graph.py       # Streamlit dashboard
├── settings.py                     # Configuration settings
├── requirements.txt
└── main.py                         # FastAPI entry point
```

---

## 📈 Frontend-Backend-PayPal Integration Flow

1. **User initiates donation** → Frontend sends amount to `/donate/`  
2. **Backend responds** with approval URL  
3. **User redirected to PayPal** and approves the payment  
4. **User redirected back** to frontend with `paymentId` & `PayerID`  
5. **Frontend sends to** `/donate/verify`  
6. **Backend verifies** payment and stores it  
7. **Frontend shows success/failure message**

---

🚀 You're now ready to accept donations securely with **DonateX**!