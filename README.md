# Explainable AI (XAI) Fraud Detection Microservice

This project is a distributed microservice architecture designed to evaluate financial transactions for fraud. Instead of a simple "yes/no" AI response, the system utilizes **Explainable AI (XAI)** to provide transparent, human-readable insights detailing exactly *why* a transaction was flagged as fraudulent or safe.

The architecture emphasizes security, high performance, and machine learning interpretability.

---

## 🏗 Architecture & Tech Stack

The system consists of two distinct microservices communicating synchronously over HTTP:

### 1. Java Security & Routing Backend (`/java-backend`)
Acts as the main entry point, API Gateway, and data persistence layer.
- **Framework:** Java 21 / Spring Boot 3.x
- **Security:** Spring Security with stateless JWT (JSON Web Token) authentication.
- **Database:** Spring Data JPA with an H2 in-memory database for rapid prototyping and testing.
- **Integration:** Utilizes Spring's `RestClient` for robust HTTP communication with the Python AI service.

### 2. Python Explainable AI Service (`/python-ai-service`)
A dedicated, high-performance inference engine for evaluating transactions.
- **Framework:** Python 3 / FastAPI
- **AI Model:** `scikit-learn` Random Forest Classifier trained on synthetic transaction data.
- **Explainability:** Employs **SHAP (SHapley Additive exPlanations)** to calculate feature importance and dynamically generate human-readable explanations (e.g., "Transaction flagged as FRAUD. High amount contributed to this decision").

---

## 🚀 Getting Started

### Prerequisites
- Java 17+ (Java 21 recommended)
- Python 3.9+
- Maven (or use the provided `mvnw` wrapper)

### Running the Python AI Service
1. Navigate to the Python directory:
   ```bash
   cd python-ai-service
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Train the mock model (generates `fraud_model.pkl`):
   ```bash
   python model_trainer.py
   ```
5. Start the FastAPI server (runs on `http://127.0.0.1:8000`):
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000
   ```

### Running the Java Backend
1. Open a new terminal and navigate to the Java directory:
   ```bash
   cd java-backend
   ```
2. Build and run the Spring Boot application (runs on `http://localhost:8080`):
   ```bash
   ./mvnw spring-boot:run
   ```

---

## 🧪 Testing the End-to-End Flow

Once both services are running, you can test the system using `curl`, Postman, or PowerShell.

### 1. Authenticate and Get JWT
Send a POST request to login and retrieve your Bearer token.
```bash
curl -X POST "http://localhost:8080/auth/login?username=admin&password=password"
```

### 2. Submit a Transaction
Send a POST request to the API with your JWT token in the Authorization header.

**Safe Transaction Example:**
```bash
curl -X POST http://localhost:8080/api/transactions \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"userId":"U123","amount":25.50,"location":"Local Store","distanceToPrevious":2.1}'
```

**Fraudulent Transaction Example:**
```bash
curl -X POST http://localhost:8080/api/transactions \
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"userId":"U999","amount":1500.00,"location":"Unknown","distanceToPrevious":500.0}'
```

The response will contain the `isFraud` boolean and an `xaiExplanation` detailing the decision factors.
