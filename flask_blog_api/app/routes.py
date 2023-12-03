from flask import Blueprint, abort

app_router = Blueprint("app_router", __name__)


@app_router.post("/login")
def login():
    return "login"


@app_router.post("/logout")
def logout():
    return "logout"


@app_router.post("/register")
def register():
    return "register"


@app_router.post("/posts/create")
def create_post():
    return "create_post"


@app_router.get("/posts")
def get_all_posts():
    return "get_all_posts"


@app_router.get("/posts/<post_id>")
def get_single_post(post_id):
    return f"get_single_post: {post_id}"


@app_router.post("/posts/<post_id>/comment")
def add_comment(post_id):
    return f"add_comment: {post_id}"
