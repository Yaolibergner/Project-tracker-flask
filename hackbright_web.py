"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def index():
    """Showing homepage"""

    projects = hackbright.list_project()

    students = hackbright.list_student()

    print(projects)

    return render_template('homepage.html', projects=projects, students=students)

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student """
    return render_template("student_search.html")


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    projects = hackbright.get_grades_by_github(github)
   
    html = render_template('student_info.html', first=first, last=last, github=github, projects=projects)

    return html

@app.route("/student-add-form")
def student_add_form():
    """Show form to add student."""

    return render_template('student_add.html')


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template('confirmation_add.html', first_name = first_name, last_name = last_name, github = github)

@app.route("/project-search")
def project_search():
    """Show the form to search for a project"""

    return render_template("project_search.html")

@app.route('/project')
def show_project():
    """Show project information."""

    title = request.args.get('project')
    project = hackbright.get_project_by_title(title)

    github_grade = hackbright.get_grades_by_title(title)

    return render_template("project.html", project=project, github_grade=github_grade)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
