from django.db import models


class LTIUser(models.Model):

    ADMIN_ROLES = [
        'person#Administrator',
        'person#SysAdmin',
    ]

    INSTRUCTOR_ROLES = [
        'person#Instructor',
        'membership#Instructor',
    ]

    STUDENT_ROLES = [
        'person#Student',
        'membership#Learner',
    ]

    id = models.BigIntegerField(
        primary_key=True,
        auto_created=True,
        help_text='LTI User ID',
    )

    lti_user_id = models.UUIDField(
        help_text='User sub as refered by the LTI platform',
    )

    name = models.CharField(
        max_length=50,
        blank=True,
        help_text='User name in LTI platform',
    )

    email = models.EmailField(
        unique=True,
        help_text='User email in the LTI platform',
    )

    def is_authenticated(self) -> bool:
        return True

    @property
    def roles(self):
        return self._roles
    
    @roles.setter
    def roles(self, values):
        self._roles = []
        for role in values:
            self._roles.append(role.split('/')[-1])

    def is_admin(self) -> bool:
        return self.check_role(self.roles, self.ADMIN_ROLES)

    def check_role(self, roles, role_set) -> bool:
        return any([role in role_set for role in roles])