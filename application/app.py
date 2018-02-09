from flask import request, render_template, jsonify, url_for, redirect, g
from .models import User
from index import app, db
from sqlalchemy.exc import IntegrityError
from .utils.auth import generate_token, requires_auth, verify_token
from protocolscrap import getProtocolScrap

ALLOWED_EXTENSIONS = set(['txt', 'htm', 'html'])

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#end point
@app.route("/caps_api/protocolscrapper",  methods = ['GET', 'POST'])
def protocol_scrapper():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'protocol_file' not in request.files:
            return jsonify(error=True, message='No protocol_file part'), 400
        file = request.files['protocol_file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return jsonify(error=True, message='No selected file'), 400
        if file and allowed_file(file.filename):
            array_dict=getProtocolScrap(file)
            return jsonify({"protocoldata":array_dict})

@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
    return render_template('index.html')


@app.route("/caps_api/user", methods=["GET"])
@requires_auth
def get_user():
    return jsonify(result=g.current_user)


@app.route("/caps_api/create_user", methods=["POST"])
def create_user():
    incoming = request.get_json()
    user = User(
        email=incoming["email"],
        password=incoming["password"]
    )
    db.session.add(user)

    try:
        db.session.commit()
    except IntegrityError:
        return jsonify(message="User with that email already exists"), 409

    new_user = User.query.filter_by(email=incoming["email"]).first()

    return jsonify(
        id=user.id,
        token=generate_token(new_user)
    )


@app.route("/caps_api/get_token", methods=["POST"])
def get_token():
    incoming = request.get_json()
    user = User.get_user_with_email_and_password(incoming["email"], incoming["password"])
    if user:
        return jsonify(token=generate_token(user))

    return jsonify(error=True), 403


@app.route("/caps_api/is_token_valid", methods=["POST"])
def is_token_valid():
    incoming = request.get_json()
    is_valid = verify_token(incoming["token"])

    if is_valid:
        return jsonify(token_is_valid=True)
    else:
        return jsonify(token_is_valid=False), 403
