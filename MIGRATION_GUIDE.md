# Migration Guide - Project Reorganization

This guide helps you adapt to the new reorganized project structure.

## What Changed?

The project has been reorganized for better clarity and maintainability:

### 📁 Directory Changes

| Old Location | New Location | Notes |
|-------------|--------------|-------|
| `./app.py` | `backend/api/app.py` | Flask API moved |
| `./rag/` | `backend/rag/` | RAG modules organized |
| `./lora/` | `backend/lora/` | LoRA training organized |
| `./include/`, `./src/`, `./examples/` | `cpp/` | All C++ code in one place |
| `./datasets/` | `data/datasets/` | Data files organized |
| `./furniture_db/` | `data/furniture_db/` | Vector DB in data/ |
| `./build/` | `cpp/build/` | C++ build artifacts |
| All `*.md` docs | `docs/` | Documentation organized by topic |
| Setup scripts | `scripts/setup/` | Organized by purpose |
| `./CMakeLists.txt` | `cpp/CMakeLists.txt` | C++ build config |

### 🗂️ New Structure

```
DecoPlan-LLM/
├── backend/          # 🐍 All Python backend code
│   ├── api/         # Flask API
│   ├── rag/         # RAG system
│   ├── lora/        # LoRA training
│   └── tests/       # Backend tests
├── frontend/        # ⚛️ React frontend (unchanged)
├── cpp/             # 🔧 C++ inference engine
├── data/            # 📊 Datasets and databases
├── docs/            # 📚 All documentation
├── scripts/         # 🛠️ Utility scripts
├── models/          # 🤖 Model files (.gguf)
├── config/          # ⚙️ Editor configs
└── external/        # 📦 Dependencies (llama.cpp)
```

## Migration Steps

### 1. Update Your Working Directory

If you have any local scripts or notebooks that reference old paths:

**Old:**
```python
from rag.furniture_retriever import FurnitureRetriever
```

**New:**
```python
# If running from project root
from backend.rag.furniture_retriever import FurnitureRetriever

# Or add backend to path
import sys
sys.path.append('backend')
from rag.furniture_retriever import FurnitureRetriever
```

### 2. Running the Backend

**Old way:**
```bash
python app.py
# or
bash start_backend.sh
```

**New way:**
```bash
# Option 1: Use the deployment script
bash scripts/deployment/start_backend.sh

# Option 2: Run from backend directory
cd backend/api
python app.py

# Option 3: Run from project root
python -m backend.api.app
```

### 3. Building C++ Code

**Old way:**
```bash
mkdir build && cd build
cmake ..
make
```

**New way:**
```bash
# Option 1: Use build script
bash scripts/setup/build.sh

# Option 2: Manual build
mkdir -p cpp/build && cd cpp/build
cmake ..
make
```

### 4. Running RAG Scripts

**Old way:**
```bash
python rag/build_furniture_db.py
python rag/furniture_retriever.py --query "modern sofa"
```

**New way:**
```bash
# Option 1: From project root
python -m backend.rag.build_furniture_db
python -m backend.rag.furniture_retriever --query "modern sofa"

# Option 2: From backend directory
cd backend
python -m rag.build_furniture_db
python -m rag.furniture_retriever --query "modern sofa"
```

**Note:** Default paths have been updated automatically. The scripts now use:
- `data/datasets/Input/Furniture Dataset - Furniture Data.csv`
- `data/furniture_db`

### 5. Running LoRA Training

**Old way:**
```bash
python lora/train_lora.py
```

**New way:**
```bash
# From project root
python -m backend.lora.train_lora

# Or from backend directory
cd backend
python -m lora.train_lora
```

### 6. Setup Scripts

**Old way:**
```bash
bash setup_rag_lora.sh
bash setup_backend.sh
```

**New way:**
```bash
bash scripts/setup/setup_rag_lora.sh
bash scripts/setup/setup_backend.sh
```

### 7. Documentation

All documentation is now organized in `docs/`:

- **Setup Guides**: `docs/setup/`
  - `INSTALL_GUIDE.md`
  - `QUICKSTART.md`
  - `FULLSTACK_SETUP.md`

- **Backend Docs**: `docs/backend/`
  - `QUICKSTART_RAG_LORA.md`
  - `RAG_LORA_README.md`
  - `IMPLEMENTATION_SUMMARY.md`

- **C++ Docs**: `docs/cpp/`
  - `BUILD.md`
  - `USAGE.md`

- **API Docs**: `docs/api/`
  - `API_DOCS.md`

### 8. Frontend (No Changes)

The frontend structure remains unchanged:
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

If you have custom paths in environment variables, update them:

**Old:**
```bash
export FURNITURE_DB_PATH="./furniture_db"
export DATASET_PATH="./datasets/Input/Furniture Dataset - Furniture Data.csv"
```

**New:**
```bash
export FURNITURE_DB_PATH="./data/furniture_db"
export DATASET_PATH="./data/datasets/Input/Furniture Dataset - Furniture Data.csv"
```

## Common Issues

### Issue: Import errors in Python

**Solution:** Make sure to run from the correct directory or add the backend directory to your Python path:

```bash
# Add to your script
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'backend'))
```

### Issue: CMake can't find llama.cpp

**Solution:** Ensure you're running CMake from the `cpp/` directory:

```bash
cd cpp
mkdir -p build && cd build
cmake ..
```

### Issue: Flask app can't find furniture_db

**Solution:** The app now uses absolute paths. Make sure the database exists at `data/furniture_db`. If needed, rebuild it:

```bash
python -m backend.rag.build_furniture_db
```

## Testing the Migration

Run these commands to verify everything works:

```bash
# 1. Test backend imports
python -c "from backend.rag.furniture_retriever import FurnitureRetriever; print('✓ Backend imports OK')"

# 2. Test C++ build
cd cpp && mkdir -p build && cd build && cmake .. && cd ../..

# 3. Test API
cd backend/api && python app.py &
sleep 5
curl http://localhost:5000/health
kill %1

# 4. Test frontend (unchanged)
cd frontend && npm install && npm run build
```

## Benefits of New Structure

✅ **Clearer Organization**: Backend, frontend, and C++ code are clearly separated

✅ **Better Documentation**: All docs organized by topic in `docs/`

✅ **Easier Navigation**: Related files are grouped together

✅ **Scalability**: Easy to add new modules without cluttering root

✅ **Standard Structure**: Follows industry best practices

## Need Help?

- Check the updated README.md in the project root
- See specific documentation in `docs/`
- Review the project structure diagram in this guide

## Rollback (If Needed)

If you need to rollback, all files are moved (not copied), so you can use git:

```bash
git checkout HEAD -- .
```

Or manually move files back to their original locations using this guide as a reference.
