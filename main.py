"""API FastAPI para execução do dashboard de transações."""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import subprocess
import sys
import os
from typing import Optional
import uvicorn

app = FastAPI(
    title="API do Dashboard de Transações",
    description="API para gerenciar a execução do dashboard Streamlit",
    version="1.0.0"
)

# Variável global para armazenar o processo do Streamlit
streamlit_process: Optional[subprocess.Popen] = None

@app.get("/")
async def root():
    """Endpoint raiz com informações da API."""
    return {
        "message": "API do Dashboard de Transações",
        "endpoints": {
            "start_dashboard": "/start-dashboard",
            "stop_dashboard": "/stop-dashboard",
            "dashboard_status": "/dashboard-status"
        }
    }

@app.post("/start-dashboard")
async def start_dashboard(port: int = 8501):
    """Inicia o dashboard Streamlit."""
    global streamlit_process
    
    if streamlit_process is not None:
        raise HTTPException(
            status_code=400,
            detail="Dashboard já está em execução"
        )
    
    try:
        # Inicia o processo do Streamlit
        streamlit_process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "src/dashboard/app.py",
                "--server.port",
                str(port)
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Dashboard iniciado com sucesso",
                "port": port,
                "url": f"http://localhost:{port}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao iniciar o dashboard: {str(e)}"
        )

@app.post("/stop-dashboard")
async def stop_dashboard():
    """Para o dashboard Streamlit."""
    global streamlit_process
    
    if streamlit_process is None:
        raise HTTPException(
            status_code=400,
            detail="Dashboard não está em execução"
        )
    
    try:
        # Termina o processo do Streamlit
        streamlit_process.terminate()
        streamlit_process = None
        
        return {"message": "Dashboard parado com sucesso"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao parar o dashboard: {str(e)}"
        )

@app.get("/dashboard-status")
async def dashboard_status():
    """Retorna o status atual do dashboard."""
    global streamlit_process
    
    if streamlit_process is None:
        return {
            "status": "stopped",
            "message": "Dashboard não está em execução"
        }
    
    # Verifica se o processo ainda está rodando
    if streamlit_process.poll() is None:
        return {
            "status": "running",
            "message": "Dashboard está em execução",
            "pid": streamlit_process.pid
        }
    else:
        streamlit_process = None
        return {
            "status": "stopped",
            "message": "Dashboard não está mais em execução"
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
