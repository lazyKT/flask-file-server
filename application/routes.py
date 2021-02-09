import os
from datetime import datetime
from flask import Blueprint, render_template, current_app, request, jsonify
from .Model.Record import Record
from werkzeug.utils import secure_filename
from . import helper


bp = Blueprint ('_record_bp', __name__, template_folder='templates', static_folder='static')


ALLOWED_EXTENSTION = { 'jpeg', 'jpg', 'png', 'gif', 'mp4', 'omv' }


@bp.route ('/', methods = ['GET'])
def index ():
    records = Record.get_records()
    return render_template('index.html', records = records)


@bp.route('/upload-desc', methods = ['POST'])
def upload_desc ():
    description = request.get_json()['desc']
    tag = request.get_json()['tag']
    print("Description", description)
    try:
        timeline = helper.calculate_timeline()
        _new_record = Record(description=description, timeline=timeline, tag = tag)
        _new_id = _new_record.add_desc_only()
        return {'msg': {'id':_new_id}}, 201
    except Exception:
        print("Error Encountered Adding Descritpion!")
        return {'Error Encountered Adding Descritpion!'}, 500


@bp.route('/upload/<_id>', methods = ['POST'])
def upload (_id):

    if 'file' not in request.files:
        print("No file found in request body!")
        flash('No file part')
        return redirect(url_for(index))

    doc = request.files['file']

    timeline = helper.calculate_timeline()
    _dir_name = f"{current_app.config['BASE_DIR']}/Day_{timeline}"
    if not os.path.isdir(_dir_name):
        os.mkdir(_dir_name)
        print("New directory created!")
    
    if doc:      
        doc_name = secure_filename(doc.filename).split('.')[0]
        ext = secure_filename(doc.filename).split('.')[1]
        new_doc_name = f"{doc_name}-{datetime.now()}.{ext}"
        
        if ext not in ALLOWED_EXTENSTION:
            return {'msg': 'Invalid File'}, 400

        _type = "video" if ext == 'mp4' or ext == 'omv' else "image"
        # _path = current_app.config['VDO_FOLDER'] if ext == 'mp4' or ext == 'omv' else current_app.config['IMAGE_FOLDER']

        _record = {
            'name': new_doc_name,
            'content-type': _type
        }

        dd = Record.add_file(_id, **_record)
        if dd == -1:
            return {"Upload Failed!"}, 500

        try:
            doc.save(os.path.join(f"{_dir_name}", new_doc_name))
            return {'msg': 'File Uploaded Success!'}, 200
        except FileNotFoundError:
            print("File Not Found!")
            return {'Upload Failed!'}, 500



@bp.route('/records', methods = ['GET'])
def get_records ():
    records = Record.get_records()
    return jsonify(records)

