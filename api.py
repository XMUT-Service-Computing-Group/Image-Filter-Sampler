from flask import Flask, redirect

import imageBlend

app = Flask(__name__)
# 处理中文编码
app.config['JSON_AS_ASCII'] = False


@app.route("/", methods=["GET"])
def readme():
    return redirect("https://github.com/XMUT-Service-Computing-Group/Image-Filter-Sampler#readme", code=301)


@app.route("/blend", methods=["GET"])
def blend():
    return imageBlend.blend()
    # return send_file(imageBlend.blend())


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, threaded=True)
