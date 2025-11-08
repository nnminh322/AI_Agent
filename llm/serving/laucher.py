# launcher.py
import yaml
import subprocess
import sys
import os
from loguru import logger

CONFIG_PATH = "./configs.yaml"

def build_vllm_command():
    """
    Đọc config.yaml và xây dựng danh sách lệnh để chạy vLLM server.
    """
    try:
        with open(CONFIG_PATH, "r") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Lỗi: Không tìm thấy file cấu hình '{CONFIG_PATH}'")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Lỗi khi đọc file YAML: {e}")
        sys.exit(1)

    server_config = config.get("vllm_server")
    if not server_config:
        logger.error("Lỗi: Không tìm thấy 'vllm_server' trong config.yaml")
        sys.exit(1)

    command = ["python", "-m", "vllm.entrypoints.openai.api_server"]

    for key, value in server_config.items():
        if value is not None:
            arg_name = f"--{key.replace('_', '-')}"
            command.append(arg_name)
            command.append(str(value))
    
    return command

if __name__ == "__main__":
    cmd = build_vllm_command()
    
    logger.info("--- 🚀 Đang khởi chạy vLLM Server ---")
    logger.info(f"Lệnh sẽ thực thi: {' '.join(cmd)}")
    logger.info("---------------------------------")
    
    try:
        os.execvp(cmd[0], cmd)
    except KeyboardInterrupt:
        logger.warning("\nĐã nhận tín hiệu dừng (Ctrl+C). Đang tắt server.")
    except Exception as e:
        logger.exception(f"Lỗi nghiêm trọng khi khởi chạy vLLM server: {e}")
        sys.exit(1)