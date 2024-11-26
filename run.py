import uvicorn
import os
from pathlib import Path

# 프로젝트 루트 디렉토리를 Python 경로에 추가
import sys
sys.path.append(str(Path(__file__).parent))

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="debug"
    )

