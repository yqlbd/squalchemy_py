from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root@localhost:3306/py"
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(255))


with app.app_context():
    db.drop_all()
    db.create_all()


@app.route("/users")
def user_list():
    users = db.session.execute(
        db.select(User).order_by(User.username)).scalars()
    return {'result': 200}


@app.route("/users/create", methods=["GET"])
def user_create():
    username = request.args.get('username')
    email = request.args.get('email')
    user = User(
        username=username,
        email=email,
    )
    db.session.add(user)
    db.session.commit()
    return {'result': 200}


# @app.route("/user/<int:id>")
# def user_detail(id):
#     user = db.get_or_404(User, id)
#     return user


# @app.route("/user/<int:id>/delete", methods=["GET", "POST"])
# def user_delete(id):
#     user = db.get_or_404(User, id)

#     if request.method == "POST":
#         db.session.delete(user)
#         db.session.commit()
#         return redirect(url_for("user_list"))

#     return render_template("user/delete.html", user=user)


if __name__ == '__main__':
    app.run(debug=True)
