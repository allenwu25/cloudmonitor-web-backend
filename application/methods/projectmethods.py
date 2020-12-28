from application.models.project import Project
from application.utils.exceptions import CustomException
from application.utils.extensions import db


class ProjectMethods:
    def get_project_by_id(self, projectid):
        existing_project = Project.query.filter(Project.projectid == projectid).first()
        return existing_project

    def get_project_by_name(self, userid, projectname):
        existing_project = Project.query \
        .filter(Project.userid == userid) \
        .filter(Project.projectname == projectname).first()
        return existing_project


    def create_project(self, userid, projectname):

        if (projectname == None):
            raise CustomException("No projectname parameter in body", 400)

        existing_project = self.get_project_by_name(userid, projectname)
        if (existing_project != None):
            raise CustomException("Project name already exists for user", 400)
        
        new_project = Project(
            userid = userid,
            projectname = projectname,
            numberurls = 0,
            uptime = 0
        )

        db.session.add(new_project)
        db.session.commit()
