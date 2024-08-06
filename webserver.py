"""
## Прототип сайта.
"""


from dataclasses import dataclass
from flask import render_template, url_for, Flask, request
from mysql.connector import connect, Error


prototype: Flask = Flask(__name__)


@dataclass
class User(object):
    """
    #### Прототип пользовательского шаблона.

    Включает в себя следующие свойства:

    username: принимает строковый аргумент.
    login: принимает строковый аргумент.
    userage: принимает целочисленный аргумент.
    boolanswer: принимает логический аргумент.
    """
    username: str
    login: str
    userage: int
    boolanswer: bool


def database_connection(user_object: User | tuple[str, str] | None, mode: str = "write") -> None | bool | tuple[any]:
    """
    Функция для подключки к БД и записи в неё объекта пользователя.
    """
    try:
        with connect(host="localhost", user="root", password="pituhon", database="protobase") as db:
            with db.cursor() as cursor:
                cursor.execute("SELECT * FROM userstable;")
                if mode == "select":
                    return cursor.fetchall()
                for i, row in enumerate(cursor.fetchall()):
                    if not (row.count(row[1]) > 1 and row.count(row[2]) > 1):
                        if mode == "write" and i == 0:
                            cursor.execute(
    f"INSERT INTO userstable(username, login, userage, boolanswer) VALUES ('{user_object.username}', '{user_object.login}', {user_object.userage}, {user_object.boolanswer})"
                            )
                        elif mode == "read":
                            return True
                    else:
                        if mode == "read":
                            return False
            db.commit()
    except Error as e:
        print(f"FAIL!!!:\n{e}")


@prototype.route("/", methods=["GET"])
@prototype.route("/main", methods=["GET"])
@prototype.route("/main/<string:username>", methods=["GET"])
def main_handler(username: str = "NN") -> str:
    """
    #### Обработчик главной страницы.
    """
    page: str = ""
    with open("templates\main.html", "r", encoding="UTF-8") as file:
        page = file.read()
        with open("templates\main.html", "w", encoding="UTF-8") as file:
            file.write(page.replace("username", username))
    return render_template("main.html", users=database_connection(None, "select"))


@prototype.route("/reg", methods=["GET", "POST"])
def registration_handler() -> str:
    """
    #### Обработчик страницы для регистрации.
    """
    if request.method == "POST":
        boolanswer: bool = False
        if request.form["boolanswer"]:
            boolanswer = True
        user: User = User(request.form["username"], request.form["login"], request.form["userage"], boolanswer)
        database_connection(user)
        return main_handler(user.username)
    return render_template("register.html")


@prototype.route("/ent", methods=["GET", "POST"])
def enter_handler() -> str:
    """
    #### Обработчик входной странички.
    """
    if request.method == "POST":
        username: str = request.form["username"]
        login: str = request.form["login"]
        user: tuple[str, str] = (username, login)
        result: bool = database_connection(user, "read")
        if result:
            return main_handler(user[0])
    return render_template("enter.html")


def run_protosite(do_debug: bool = False) -> None:
    """
    Эта функция запускает сервер.
    :param do_debug: принимает логическое значение.
    """
    prototype.run("localhost", 7000, debug=do_debug)


if __name__ == "__main__":
    run_protosite(True)
