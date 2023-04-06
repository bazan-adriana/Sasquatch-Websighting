from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.report_model import Report


#  ================== Add a New Report!  CREATE page    - VIEW
@app.route('/reports/new')
def new_report():
    return render_template("report_new.html")


#  ===================  CREATE  - ACTION  method (POST)
@app.route('/reports/create', methods=['POST'])
def create_report():
    print(f"-------{request.form}---------")
#  validate the model
    if not Report.validator(request.form):
        return redirect("/reports/new")
    report_data = {
        **request.form,
        'user_id': session['user_id']
    }
    Report.create(report_data)
    return redirect('/dashboard')


#  ============    UPDATE  - EDIT PAGE  ========
@app.route('/reports/<int:id>/edit')
def edit_report(id):

    data = {
        "id": id
    }
    this_report = Report.get_by_id(data)
    return render_template("report_edit.html",
                            this_report = this_report)
    
    
#  ===================  UPDATE   - ACTION  method (POST)
@app.route('/reports/<int:id>/update', methods=['POST'])
def update_report(id):
    #  validate the model
    if not Report.validator(request.form):
        return redirect(f"/reports/{id}/edit")
    
    data = {
        'id' : id,
        **request.form
    }
    
    Report.update(data)
    return redirect('/dashboard')


#  =============  READ ONE  show   ============
@app.route("/reports/<int:id>")
def show_one_report(id):
    this_report = Report.get_by_id({'id': id})
    return render_template("report_one.html",
                            this_report = this_report)



#  =================    DELETE     ============
@app.route('/reports/<int:id>/delete')
def delete_report(id):
    Report.delete({'id' : id})
    return redirect('/dashboard')
