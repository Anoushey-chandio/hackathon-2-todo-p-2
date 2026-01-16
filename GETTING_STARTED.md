# 🚀 Getting Started Checklist

Follow this checklist to get the Todo App up and running in minutes!

## ✅ Prerequisites (5 minutes)

- [ ] **Python 3.11+** installed
  ```bash
  python --version
  ```

- [ ] **Node.js 18+** installed
  ```bash
  node --version
  npm --version
  ```

- [ ] **Git** installed (optional, but recommended)
  ```bash
  git --version
  ```

- [ ] **Neon Database** connection URL ready
  - Already configured in `.env` file
  - Check: `cat backend/.env` or `type backend\.env`

## 📦 Installation (5 minutes)

### Backend Setup

- [ ] Navigate to backend directory
  ```bash
  cd backend
  ```

- [ ] Create/activate virtual environment
  ```bash
  python -m venv venv
  source venv/bin/activate  # macOS/Linux
  # or
  venv\Scripts\activate     # Windows
  ```

- [ ] Install Python dependencies
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Verify database connection
  ```bash
  python -c "from src.core.database import init_db; import asyncio; asyncio.run(init_db())" && echo "✅ Database connected!"
  ```

### Frontend Setup

- [ ] Open new terminal, navigate to frontend
  ```bash
  cd frontend
  ```

- [ ] Install Node dependencies
  ```bash
  npm install
  ```

## 🎬 Starting the App (2 minutes)

### Option 1: Automatic (Recommended)

**Windows:**
```bash
START_APP.bat
```

**macOS/Linux:**
```bash
chmod +x start_app.sh
./start_app.sh
```

### Option 2: Manual

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate
python -m uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

Wait for: `Uvicorn running on http://127.0.0.1:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Wait for: `localhost:3000` ready in

## 🧪 Verify Everything Works (2 minutes)

- [ ] Quick test verification
  ```bash
  # In a new terminal
  python run_quick_tests.py
  ```
  Expected: All tests pass with ✅ marks

## 🌐 Access the App (1 minute)

- [ ] Open browser and go to: **http://localhost:3000**

- [ ] You should see the Todo App login page

## 👤 Test User Account (1 minute)

### Option 1: Sign Up a New Account

- [ ] Click "Sign up" button
- [ ] Enter email: `test@example.com`
- [ ] Enter password: `Test123!Password`
- [ ] Enter username: `Test User`
- [ ] Click "Sign up" button
- [ ] You should be redirected to dashboard

### Option 2: Use Quick Test

- [ ] The quick test created a user automatically
- [ ] Email: `test@example.com`
- [ ] Password: `TestPassword123!`
- [ ] Use these credentials to login

## ✅ Test Core Features (2 minutes)

- [ ] **Sign Up**: Create a new account successfully
- [ ] **Sign In**: Login with created account
- [ ] **Create Task**: Add a new task titled "Test Task"
- [ ] **Read Tasks**: See task in list
- [ ] **Update Task**: Mark task as complete
- [ ] **Delete Task**: Remove task from list
- [ ] **Sign Out**: Logout and verify redirected to login

## 📊 Run Full Test Suite (Optional, 10 minutes)

```bash
# Install test dependencies
pip install pytest

# Run all tests
pytest TEST_INTEGRATION.md -v

# Expected: 25+ tests, all passing
```

## 📚 Documentation (As Needed)

If you need help:

- [ ] **Quick Start**: Read [README.md](README.md)
- [ ] **Complete Setup**: Read [SETUP_GUIDE.md](SETUP_GUIDE.md)
- [ ] **Testing Guide**: Read [TESTING_GUIDE.md](TESTING_GUIDE.md)
- [ ] **API Reference**: Read [SETUP_GUIDE.md](SETUP_GUIDE.md#api-endpoints)

## 🐛 Troubleshooting

### Backend won't start

- [ ] Check Python version: `python --version` (need 3.11+)
- [ ] Activate venv: `source venv/bin/activate` or `venv\Scripts\activate`
- [ ] Try again: `python -m uvicorn src.main:app --reload`

### Frontend won't start

- [ ] Check Node version: `node --version` (need 18+)
- [ ] Clear cache: `rm -rf .next node_modules`
- [ ] Reinstall: `npm install`
- [ ] Try again: `npm run dev`

### Can't connect to database

- [ ] Check `.env` file has DATABASE_URL
- [ ] Verify Neon credentials are correct
- [ ] Test directly: `psql <DATABASE_URL>`

### 401 Unauthorized on API calls

- [ ] Check token in localStorage (DevTools → Application → Local Storage)
- [ ] Verify backend is running on port 8000
- [ ] Verify token is included in request headers

**Still stuck?** See [TESTING_GUIDE.md#troubleshooting](TESTING_GUIDE.md#troubleshooting)

## 🎉 Success Criteria

You're done when you can:

- ✅ Start backend: `python -m uvicorn src.main:app --reload`
- ✅ Start frontend: `npm run dev`
- ✅ Access app: http://localhost:3000
- ✅ Create account
- ✅ Login successfully
- ✅ Create/read/update/delete tasks
- ✅ Logout successfully
- ✅ Run tests: `python run_quick_tests.py` (all pass)

## 🚀 Next Steps

1. **Explore the Code**
   - Backend: `backend/src/api/endpoints/auth.py`
   - Frontend: `frontend/src/app/(auth)/signup/page.tsx`
   - Database: `backend/src/core/database.py`

2. **Customize**
   - Add your own logo
   - Change colors in `frontend/tailwind.config.ts`
   - Add more task features

3. **Deploy**
   - Choose hosting (Vercel for frontend, Railway for backend)
   - Update environment variables
   - Run production builds

4. **Extend**
   - Add email verification
   - Add password reset
   - Add task sharing
   - Add real-time updates

## 📞 Quick Reference

| Command | Purpose |
|---------|---------|
| `python run_quick_tests.py` | Quick verification |
| `pytest TEST_INTEGRATION.md -v` | Full test suite |
| `START_APP.bat` | Start both servers (Windows) |
| `./start_app.sh` | Start both servers (macOS/Linux) |
| `curl http://127.0.0.1:8000/` | Check backend is running |
| `psql <DATABASE_URL>` | Test database connection |

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Prerequisites check | 5 min |
| Backend installation | 5 min |
| Frontend installation | 3 min |
| Start servers | 2 min |
| Quick test | 2 min |
| Manual feature test | 5 min |
| **Total** | **22 minutes** |

## 🎓 Learning Resources

- FastAPI: https://fastapi.tiangolo.com/
- Next.js: https://nextjs.org/docs
- SQLAlchemy: https://docs.sqlalchemy.org/
- JWT: https://tools.ietf.org/html/rfc8725
- PostgreSQL: https://www.postgresql.org/docs/

---

**You're all set! 🎉**

1. Start servers using one of the methods above
2. Open http://localhost:3000
3. Create account and start using the app!

For detailed documentation, see [README.md](README.md)

Need help? Check [TESTING_GUIDE.md](TESTING_GUIDE.md#troubleshooting)
