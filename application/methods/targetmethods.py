from application.models.target import Target
from application.methods.projectmethods import ProjectMethods
from application.utils.exceptions import CustomException
from application.utils.extensions import db


class TargetMethods:
    # Gets target by id
    def get_target_by_id(self, targetid):
        existing_target = Target.query.filter(Target.urlid == targetid).first()
        return existing_target

    # Creates a new target for a given project, given target_info
    def create_target(self, projectid, userid, target_info):

        # Project based on projectid should exist
        existing_project = ProjectMethods().get_project_by_id(projectid, userid)
        if (existing_project == None):
            raise CustomException("Project does not exist", 400)
        
        # User can only create target for a project they own
        if (existing_project.userid != userid):
            raise CustomException("Userid does not match project's userid", 403)
        
        try:
            link = target_info['link']
            testtype = target_info['testtype']
            requestheaders = target_info.get('requestheaders')
            requestbody = target_info.get('requestbody')
            requesttype = target_info.get('requesttype')
        except:
            raise CustomException("Invalid json body parameters", 400)

        try:
            # Create a new target based on request body json
            new_target = Target(
                projectid = projectid,
                link = link,
                testtype = testtype,
                numsuccess = 0,
                numfailure = 0,
                requestheaders = requestheaders,
                requestbody = requestbody,
                requesttype = requesttype
            )

            # Optional parameters
            if (requestheaders): new_target.requestheaders = requestheaders
            if (requestbody): new_target.requestheaders = requestbody
            if (requesttype): new_target.requestheaders = requesttype


            db.session.add(new_target)
            db.session.commit()

            return new_target

        except:
            raise CustomException("Invalid json body parameters", 400)


    # Updates fields for a target
    def update_target(self, projectid, userid, targetid, target_update_info):
        # Project based on projectid should exist
        existing_project = ProjectMethods().get_project_by_id(projectid, userid)
        if (existing_project == None):
            raise CustomException("Project does not exist", 400)

        # User can only update target for a project they own
        if (existing_project.userid != userid):
            raise CustomException("Userid does not match project's userid", 403)
        
        try:
            # Get update parameters from request body json
            link = target_update_info.get('link')
            testtype = target_update_info.get('testtype')
            requestheaders = target_update_info.get('requestheaders')
            requestbody = target_update_info.get('requestbody')
            requesttype = target_update_info.get('requesttype')

        except:
            raise CustomException("Invalid request json parameters", 400)

        # Target ID should correspond to a valid target
        existing_target = self.get_target_by_id(targetid)
        if (existing_target == None):
            raise CustomException("Target based on target id does not exist", 400)
        
        # Update fields of existing target record
        if (link): existing_target.link = link
        if (testtype): existing_target.testtype = testtype
        if (requestheaders): existing_target.requestheaders = requestheaders
        if (requestbody): existing_target.requestbody = requestbody
        if (requesttype): existing_target.requesttype = requesttype

        db.session.commit()

    def delete_target(self, projectid, userid, targetid):
        # Project based on projectid should exist
        existing_project = ProjectMethods().get_project_by_id(projectid, userid)
        if (existing_project == None):
            raise CustomException("Project does not exist", 400)

        # User can only update target for a project they own
        if (existing_project.userid != userid):
            raise CustomException("Userid does not match project's userid", 403)
        
        try:
            Target.query.filter_by(urlid=targetid).delete()
            db.session.commit()
        except:
            raise CustomException("Error when deleting", 400)
    