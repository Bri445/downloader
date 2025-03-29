from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_formats', methods=['POST'])
def get_formats():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        formats = [
            {
                'format_id': f['format_id'],
                'ext': f['ext'],
                'resolution': f.get('resolution') or f.get('format_note'),
                'filesize': f.get('filesize') or 0,
                'url': f['url']
            } for f in info['formats'] if f.get('url') and f.get('filesize')
        ]
        return jsonify({'title': info.get('title', ''), 'formats': formats})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
