from flask import Blueprint, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth

auth_google_bp = Blueprint("auth_google", __name__, url_prefix="/auth")
oauth = OAuth()

def init_google(app):
    oauth.init_app(app)
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        access_token_url="https://oauth2.googleapis.com/token",
        authorize_url="https://accounts.google.com/o/oauth2/v2/auth",
        client_kwargs={"scope": "openid email profile"},
        jwks_uri="https://www.googleapis.com/oauth2/v3/certs"
    )

@auth_google_bp.route("/login")
def login():
    redirect_uri = url_for("auth_google.authorize", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_google_bp.route("/authorize")
def authorize():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)
    session["user"] = {
        "sub": user_info.get("sub"),
        "email": user_info.get("email"),
        "name": user_info.get("name"),
        "picture": user_info.get("picture")
    }
    session["token"] = token
    return redirect("/")

@auth_google_bp.route("/me")
def me():
    user = session.get("user")
    if not user:
        return jsonify({"error": "No user logged in"}), 401
    return jsonify(user)

@auth_google_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")

