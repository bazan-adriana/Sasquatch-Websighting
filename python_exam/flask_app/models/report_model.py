from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model


class Report:
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.what = data['what']
        self.sasquatches = data['sasquatches']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        


#  =============    CREATE    ============
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO reports (location, what, sasquatches, date, user_id)
            VALUES (%(location)s,%(what)s,%(sasquatches)s,%(date)s,%(user_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    
#  ===========  READ ALL  =============
    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM reports
                JOIN users
                ON reports.user_id = users.id;
            """
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        all_reports = []
        if results:
            for row in results:
                # create each report
                this_report = cls(row)       # instantiate a report
            # create the user for this report
                user_data = {                # prepare the dict for the user constructor
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at'],
                    **row
                }
# now we can make a user
                this_user = user_model.User(user_data)
            # add new attribute
                this_report.planner = this_user
                all_reports.append(this_report)
        return all_reports

#  ============    READ ONE   ==================
    @classmethod
    def get_by_id(cls, data):
        query = """
            SELECT * FROM reports
            JOIN users
            ON reports.user_id = users.id
            WHERE reports.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        print(results)
        if results:
            # init the report
            this_report = cls(results[0])
# init the user and attach the report
            row = results[0]
            user_data = {
                **row,
                'id': row['users.id'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            # create a User obj here
            this_user = user_model.User(user_data)
            this_report.planner = this_user    # adding a new attribute to the report
            return this_report
        return False


#  ===============    UPDATE   ==================
    @classmethod
    def update(cls, data):
        query = """
            UPDATE reports
            SET
            location = %(location)s,
            what = %(what)s,
            date = %(date)s,
            sasquatches = %(sasquatches)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)




#  ===============    DELETE   ===========================
    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM reports
        Where id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)





#  ===================  VALIDATOR  =========================
    @staticmethod
    def validator(form_data):
        is_valid = True

        if len(form_data['location']) < 1:
            is_valid = False
            flash("All fields required", 'form_validate')

        if len(form_data['what']) < 1:
            is_valid = False
            flash("All fields required", 'form_validate')

        if len(form_data['sasquatches']) < 1:
            is_valid = False
            flash("All fields required", 'form_validate')

        if len(form_data['date']) < 1:
            is_valid = False
            flash("All fields required", 'form_validate')

        return is_valid
    
    
