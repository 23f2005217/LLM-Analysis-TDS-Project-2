import subprocess
from langchain_core.tools import tool
from dotenv import load_dotenv
import os
from logger import setup_logger

load_dotenv()
logger = setup_logger("run_code")

def strip_code_fences(code: str) -> str:
    code = code.strip()
    if code.startswith("```"):
        code = code.split("\n", 1)[1]
    if code.endswith("```"):
        code = code.rsplit("\n", 1)[0]
    return code.strip()

@tool
def run_code(code: str) -> dict:
    """
    Executes a Python code 
    This tool:
      1. Takes in python code as input
      3. Writes code into a temporary .py file
      4. Executes the file
      5. Returns its output

    Parameters
    ----------
    code : str
        Python source code to execute.

    Returns
    -------
    dict
        {
            "stdout": <program output>,
            "stderr": <errors if any>,
            "return_code": <exit code>
        }
    """
    try: 
        logger.info("Executing Python code")
        filename = "runner.py"
        os.makedirs("LLMFiles", exist_ok=True)
        with open(os.path.join("LLMFiles", filename), "w") as f:
            f.write(code)

        proc = subprocess.Popen(
            ["uv", "run", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd="LLMFiles"
        )
        stdout, stderr = proc.communicate()
        
        if proc.returncode != 0:
            logger.error(f"Code execution failed with return code {proc.returncode}")
            logger.error(f"Stderr: {stderr}")
        else:
            logger.info("Code execution successful")

        return {
            "stdout": stdout,
            "stderr": stderr,
            "return_code": proc.returncode
        }
    except Exception as e:
        logger.error(f"Exception during code execution: {e}")
        return {
            "stdout": "",
            "stderr": str(e),
            "return_code": -1
        }