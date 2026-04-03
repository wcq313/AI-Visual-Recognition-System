from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import base64
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 1. 文字识别(OCR)密钥
OCR_AK = "r9lzPZBMa5IJzsfruDFRVHdJ"
OCR_SK = "63BT186Zj7YptseAT0aCeZ6rcz83ldT3"

# 2. 图像识别密钥
IMAGE_AK = "0CSu3TPVmyozZi43LrUVDXOd"
IMAGE_SK = "acPspplNdxXfmBv01Aw32H4CDRQGQB3J"


# =============================================================================================

@app.route('/')
def index():
    return send_from_directory(os.path.dirname(__file__), "index.html")


# 获取 OCR token
def get_ocr_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": OCR_AK,
        "client_secret": OCR_SK
    }
    return requests.post(url, data=data).json().get("access_token")


# 获取 图像识别 token
def get_image_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": IMAGE_AK,
        "client_secret": IMAGE_SK
    }
    return requests.post(url, data=data).json().get("access_token")


# ------------------- 1. OCR 文字识别 -------------------
@app.route("/api/ocr", methods=["POST"])
def ocr():
    try:
        img = request.json["img"]
        token = get_ocr_token()
        url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={token}"
        res = requests.post(url, data={"image": img, "language_type": "CHN_ENG"}).json()
        text = "\n".join([w["words"] for w in res.get("words_result", [])])
        return jsonify({"code": 200, "data": text, "msg": "识别成功"})
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)})


# ------------------- 2. 通用图像识别 -------------------
@app.route("/api/image", methods=["POST"])
def image_recognize():
    try:
        img = request.json["img"]
        token = get_image_token()
        url = f"https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general?access_token={token}"
        res = requests.post(url, data={"image": img}).json()

        result = []
        for item in res.get("result", [])[:5]:  # 取前5个
            result.append(f"{item['keyword']} {item['score']:.1%}")

        return jsonify({"code": 200, "data": "\n".join(result), "msg": "识别成功"})
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
