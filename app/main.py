from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
import logging
import uuid
import os

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기본 디렉토리 설정
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR.parent / "static"
UPLOAD_DIR = BASE_DIR.parent / "uploads"

# uploads 폴더 생성
UPLOAD_DIR.mkdir(exist_ok=True)

# 템플릿 설정
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# 정적 파일 설정
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/api/analyze-document")
async def analyze_document(file: UploadFile = File(...)):
    logger.info(f"File upload started: {file.filename}")
    try:
        # 파일 확장자 검사
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in ['.jpg', '.jpeg', '.png', '.pdf']:
            logger.warning(f"Invalid file type: {file_extension}")
            raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")

        # 임시 파일 저장
        file_path = UPLOAD_DIR / f"{uuid.uuid4()}{file_extension}"
        logger.info(f"Saving file to: {file_path}")

        with open(file_path, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

        logger.info("File saved successfully")

        # 임시 응답 데이터 (실제 분석 결과로 대체 필요)
        response_data = {
            "status": "success",
            "ocr_result": {
                "document_type": "진단서",
                "patient_name": "홍길동",
                "diagnosis": "요추 추간판 탈출증",
                "treatment_period": "4주",
                "hospital": "서울중앙병원"
            },
            "compensation_estimate": {
                "total": 25000000,
                "breakdown": {
                    "medical_expenses": 5000000,
                    "lost_income": 3000000,
                    "disability_compensation": 12000000,
                    "consolation_money": 5000000
                }
            },
            "related_cases": [
                {
                    "case_number": "2023가합12345",
                    "summary": "유사 산재 사고 판례",
                    "compensation": 28000000
                }
            ],
            "applicable_laws": [
                {
                    "name": "산업재해보상보험법",
                    "article": "제40조",
                    "content": "요양급여 지급 기준"
                }
            ]
        }

        # 임시 파일 삭제
        try:
            os.unlink(file_path)
            logger.info("Temporary file deleted")
        except Exception as e:
            logger.warning(f"Failed to delete temporary file: {e}")

        logger.info("Analysis completed successfully")
        return JSONResponse(content=response_data)

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error during file processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/test")
async def test_endpoint():
    return {"message": "API is working"}



