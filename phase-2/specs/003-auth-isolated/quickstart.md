# Quickstart Guide: Authentication Implementation

## Overview
This guide provides step-by-step instructions for implementing the JWT-based authentication system with Better Auth for the full-stack todo web application. This implementation follows the isolated authentication approach, focusing solely on user identity management.

## Prerequisites

### Backend Requirements
- Python 3.13+
- FastAPI
- SQLModel
- python-jose
- passlib
- bcrypt
- Neon Serverless PostgreSQL database

### Frontend Requirements
- Node.js 18+
- Next.js 16+
- TypeScript
- Better Auth client
- Tailwind CSS

## Backend Setup

### 1. Install Backend Dependencies
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install fastapi uvicorn sqlmodel python-jose passlib[bcrypt] python-multipart
```

### 2. Configure Database Connection
Create the database models and connection:

```python
# backend/src/database.py
from sqlmodel import create_engine
from .models.user import User

DATABASE_URL = "postgresql://username:password@localhost/dbname"

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
```

### 3. Create User Model
The User model is already defined in the data model. Create the file:

```python
# backend/src/models/user.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class User(UserBase, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    email_verified: bool = Field(default=False)

class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    email_verified: bool

class UserCreate(UserBase):
    password: str
    email: str

class UserUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
```

### 4. Create Authentication Service
```python
# backend/src/services/auth_service.py
from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session, select
from passlib.context import CryptContext
from jose import JWTError, jwt
from .models.user import User, UserCreate
import uuid

SECRET_KEY = "your-secret-key-change-in-production"  # Should be in environment variables
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.access_token_expire_minutes = ACCESS_TOKEN_EXPIRE_MINUTES

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def authenticate_user(self, session: Session, email: str, password: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if not user or not self.verify_password(password, user.password_hash):
            return None
        return user

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_user(self, session: Session, user_create: UserCreate) -> User:
        # Check if user already exists
        existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
        if existing_user:
            raise ValueError("Email already registered")

        # Create new user
        user = User(
            id=str(uuid.uuid4()),
            email=user_create.email,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            password_hash=self.get_password_hash(user_create.password),
            is_active=True,
            email_verified=False
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def get_user_by_email(self, session: Session, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

    def get_current_user(self, session: Session, token: str) -> Optional[User]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
        except JWTError:
            return None

        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        return user
```

### 5. Create JWT Dependency
```python
# backend/src/api/deps.py
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from .database import engine
from .models.user import User
from .services.auth_service import AuthService

def get_session():
    with Session(engine) as session:
        yield session

def get_auth_service():
    return AuthService()

def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    auth_service = get_auth_service()
    user = auth_service.get_current_user(session, token)
    if user is None:
        raise credentials_exception
    return user
```

### 6. Create Authentication Router
```python
# backend/src/api/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from .deps import get_session, get_auth_service
from ..models.auth import UserLogin, Token
from ..models.user import UserCreate, UserRead
from ..services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(user_create: UserCreate, session: Session = Depends(get_session), auth_service: AuthService = Depends(get_auth_service)):
    try:
        user = auth_service.create_user(session, user_create)
        access_token = auth_service.create_access_token(data={"sub": user.id, "email": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=Token)
def login(user_login: UserLogin, session: Session = Depends(get_session), auth_service: AuthService = Depends(get_auth_service)):
    user = auth_service.authenticate_user(session, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(data={"sub": user.id, "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout")
def logout():
    # In a stateless JWT system, logout is typically handled on the client side
    # This endpoint can be used for additional cleanup if needed
    return {"message": "Successfully logged out"}
```

### 7. Update Main Application
```python
# backend/src/main.py
from fastapi import FastAPI
from .api.auth_router import router as auth_router
from .database import create_db_and_tables

app = FastAPI(title="Todo API with Authentication")

# Create database tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include authentication routes
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Todo API with Authentication"}
```

## Frontend Setup

### 1. Install Frontend Dependencies
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install @better-auth/react better-auth @types/react
```

### 2. Create Authentication Context
```typescript
// frontend/src/context/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useAuth } from '@better-auth/react';

interface AuthContextType {
  user: any;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, firstName?: string, lastName?: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuthContext = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuthContext must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const { signIn, signOut, session } = useAuth();
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    setIsAuthenticated(!!session?.user);
  }, [session]);

  const login = async (email: string, password: string) => {
    try {
      await signIn('credentials', {
        email,
        password,
        redirect: false,
      });
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const register = async (email: string, password: string, firstName?: string, lastName?: string) => {
    // Registration typically handled by API call to backend
    // This is a simplified example
    console.log('Registration would be handled by backend API');
  };

  const logout = async () => {
    try {
      await signOut();
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    }
  };

  const value = {
    user: session?.user,
    isAuthenticated,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
```

### 3. Create Better Auth Client Configuration
```typescript
// frontend/src/lib/better-auth-client.ts
import { createAuthClient } from 'better-auth/client';

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  // Additional configuration as needed
});
```

### 4. Create Authentication Components
```tsx
// frontend/src/components/auth/LoginForm.tsx
import React, { useState } from 'react';
import { useAuthContext } from '../../context/AuthContext';

const LoginForm: React.FC = () => {
  const { login } = useAuthContext();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(email, password);
      setError('');
    } catch (err) {
      setError('Invalid email or password');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="email" className="block text-sm font-medium">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full px-3 py-2 border rounded-md"
          required
        />
      </div>
      <div>
        <label htmlFor="password" className="block text-sm font-medium">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full px-3 py-2 border rounded-md"
          required
        />
      </div>
      {error && <div className="text-red-500 text-sm">{error}</div>}
      <button
        type="submit"
        className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600"
      >
        Login
      </button>
    </form>
  );
};

export default LoginForm;
```

```tsx
// frontend/src/components/auth/SignupForm.tsx
import React, { useState } from 'react';
import { useAuthContext } from '../../context/AuthContext';

const SignupForm: React.FC = () => {
  const { register } = useAuthContext();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await register(email, password, firstName, lastName);
      setError('');
    } catch (err) {
      setError('Registration failed');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="firstName" className="block text-sm font-medium">First Name</label>
        <input
          id="firstName"
          type="text"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          className="w-full px-3 py-2 border rounded-md"
        />
      </div>
      <div>
        <label htmlFor="lastName" className="block text-sm font-medium">Last Name</label>
        <input
          id="lastName"
          type="text"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
          className="w-full px-3 py-2 border rounded-md"
        />
      </div>
      <div>
        <label htmlFor="email" className="block text-sm font-medium">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full px-3 py-2 border rounded-md"
          required
        />
      </div>
      <div>
        <label htmlFor="password" className="block text-sm font-medium">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full px-3 py-2 border rounded-md"
          required
        />
      </div>
      {error && <div className="text-red-500 text-sm">{error}</div>}
      <button
        type="submit"
        className="w-full bg-green-500 text-white py-2 rounded-md hover:bg-green-600"
      >
        Sign Up
      </button>
    </form>
  );
};

export default SignupForm;
```

### 5. Create Authentication Pages
```tsx
// frontend/src/pages/login.tsx
import React from 'react';
import LoginForm from '../components/auth/LoginForm';
import { useAuthContext } from '../context/AuthContext';
import { useRouter } from 'next/router';

const LoginPage: React.FC = () => {
  const { isAuthenticated } = useAuthContext();
  const router = useRouter();

  // Redirect if already authenticated
  React.useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router]);

  if (isAuthenticated) {
    return null; // Or redirect to dashboard
  }

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6 text-center">Login</h1>
        <LoginForm />
        <div className="mt-4 text-center">
          <p>Don't have an account? <a href="/signup" className="text-blue-500 hover:underline">Sign up</a></p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
```

```tsx
// frontend/src/pages/signup.tsx
import React from 'react';
import SignupForm from '../components/auth/SignupForm';
import { useAuthContext } from '../context/AuthContext';
import { useRouter } from 'next/router';

const SignupPage: React.FC = () => {
  const { isAuthenticated } = useAuthContext();
  const router = useRouter();

  // Redirect if already authenticated
  React.useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, router]);

  if (isAuthenticated) {
    return null; // Or redirect to dashboard
  }

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-2xl font-bold mb-6 text-center">Sign Up</h1>
        <SignupForm />
        <div className="mt-4 text-center">
          <p>Already have an account? <a href="/login" className="text-blue-500 hover:underline">Login</a></p>
        </div>
      </div>
    </div>
  );
};

export default SignupPage;
```

### 6. Wrap Application with Auth Provider
```tsx
// frontend/src/pages/_app.tsx
import '../styles/globals.css';
import type { AppProps } from 'next/app';
import { AuthProvider } from '../context/AuthContext';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AuthProvider>
      <Component {...pageProps} />
    </AuthProvider>
  );
}

export default MyApp;
```

## Environment Configuration

### Backend Environment Variables
Create a `.env` file in the backend directory:

```
DATABASE_URL=postgresql://username:password@localhost/dbname
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend Environment Variables
Create a `.env.local` file in the frontend directory:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running the Application

### 1. Start the Backend
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

### 2. Start the Frontend
```bash
cd frontend
npm run dev
```

## Testing the Authentication

### Backend API Testing
You can test the authentication endpoints using curl or a tool like Postman:

```bash
# Register a new user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login with the user
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!"
  }'

# Access protected endpoint (replace TOKEN with actual token from login response)
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer TOKEN"
```

## Security Considerations

1. **Never commit secret keys** to version control. Use environment variables.
2. **Use HTTPS** in production to protect JWT tokens in transit.
3. **Implement rate limiting** to prevent brute force attacks.
4. **Short token expiration** times to minimize risk of token misuse.
5. **Validate tokens properly** on every protected endpoint.
6. **Use secure storage** for tokens on the frontend (preferably HttpOnly cookies).

## Next Steps

1. Implement refresh token functionality for longer user sessions
2. Add email verification for user accounts
3. Implement password reset functionality
4. Add additional security measures like rate limiting
5. Integrate authentication with the todo functionality