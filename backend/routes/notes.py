from flask import Blueprint, request, session, jsonify
from models import db, Note

notes_bp = Blueprint("notes", __name__)

def current_user_id():
    return session.get("user_id")

@notes_bp.route("/", methods=["GET"])
def list_notes():
    if not current_user_id():
        return jsonify({"error": "Unauthorized"}), 401

    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 5))

    notes = Note.query.filter_by(user_id=current_user_id()).paginate(page=page, per_page=per_page)
    return jsonify([{"id": n.id, "title": n.title, "content": n.content} for n in notes.items])

@notes_bp.route("/", methods=["POST"])
def create_note():
    if not current_user_id():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    note = Note(title=data["title"], content=data["content"], user_id=current_user_id())
    db.session.add(note)
    db.session.commit()
    return jsonify({"id": note.id, "title": note.title}), 201

@notes_bp.route("/<int:id>", methods=["PATCH"])
def update_note(id):
    if not current_user_id():
        return jsonify({"error": "Unauthorized"}), 401

    note = Note.query.filter_by(id=id, user_id=current_user_id()).first_or_404()
    data = request.json
    note.title = data.get("title", note.title)
    note.content = data.get("content", note.content)
    db.session.commit()
    return jsonify({"message": "Note updated"}), 200

@notes_bp.route("/<int:id>", methods=["DELETE"])
def delete_note(id):
    if not current_user_id():
        return jsonify({"error": "Unauthorized"}), 401

    note = Note.query.filter_by(id=id, user_id=current_user_id()).first_or_404()
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted"}), 200
