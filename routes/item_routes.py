from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Post
from app import db

item_routes = Blueprint('items', __name__)

@item_routes.route('/', methods=['POST'])
@jwt_required()
def create_post():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    post = Post(title=title, content=content)
    db.session.add(post)
    db.session.commit()

    return jsonify({"message": "Post created successfully"}), 201

@item_routes.route('/', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    posts_list = [{"id": p.id, "title": p.title, "content": p.content} for p in posts]

    return jsonify(posts_list), 200

@item_routes.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)

    db.session.commit()
    return jsonify({"message": "Post updated successfully"}), 200

@item_routes.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully"}), 200
