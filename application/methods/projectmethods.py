from application.models.project import Project
from application.models.target import Target
from application.utils.exceptions import CustomException
from application.utils.extensions import db


class ProjectMethods:
    def get_project_by_id(self, projectid, userid):
        existing_project = Project.query.filter(Project.projectid == projectid).first()
        if (existing_project.userid != userid):
            return None
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

    # Updates a project depending on parameters passed in
    def update_project(self, projectid, update_parameters, userid):
        existing_project = self.get_project_by_id(projectid, userid)
        if (existing_project == None):
            raise CustomException("Project does not exist", 400)

        if (existing_project.userid != userid):
            raise CustomException("User Id doesn't match", 400)
        

        if (update_parameters.get('projectname')):
            existing_project.projectname = update_parameters['projectname']
        
        if (update_parameters.get('numberurls')):
            existing_project.numberurls += update_parameters['numberurls']
        
        if (update_parameters.get('uptime')):
            existing_project.uptime = update_parameters['uptime']

        db.session.commit()


    def delete_project(self, projectid, userid):
        try:
            project = Project.query.filter_by(projectid=projectid).first()
            db.session.delete(project)
            db.session.commit()
        except Exception as e:
            print(e)
            raise CustomException("Delete failed", 400)

    def get_urls(self, projectid):
        project_targets = Target.query.filter(Target.projectid == projectid) 
        return project_targets

    def filter_links(self, targets):
        url_arr = []
        try:
            dict_targets = [target.to_dict() for target in targets]
            for target in dict_targets:
                url_arr.append(target['link'])
        except:
            pass

        urls = {
            'urls': url_arr
        }
        
        return urls
