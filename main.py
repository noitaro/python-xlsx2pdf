import os
import shutil
import tempfile
import subprocess

from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse

app = FastAPI()

def convertXlsx2Pdf(out_path, file_name):
    cmd = []
    cmd.append("libreoffice")
    cmd.append("--headless")
    cmd.append("--nologo")
    cmd.append("--nofirststartwizard")
    cmd.append("--convert-to")
    cmd.append("pdf:calc_pdf_Export")
    cmd.append("--outdir")
    cmd.append(out_path)
    cmd.append(file_name)

    subprocess.run(" ".join(cmd), shell=True)

@app.post("/xlsx2pdf/")
async def create_upload_file(upload_file: UploadFile):

    # アップロードされたファイルを保存
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(upload_file.file, temp_file)

    # Xlsx -> Pdf
    convertXlsx2Pdf('./work', temp_file.name)

    # ファイル名のみ抽出
    temp_file_name = os.path.basename(temp_file.name)
    upload_file_name = upload_file.filename.rsplit('.', 1)[0]

    # 変換済みPDFを返却
    return FileResponse(f'./work/{temp_file_name}.pdf', media_type='application/octet-stream', filename=f'{upload_file_name}.pdf')

# docker build -t xlsx2pdf-image .
# docker run -p 80:80 xlsx2pdf-image
