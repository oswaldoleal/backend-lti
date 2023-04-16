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

    lti_user_id = models.UUIDField(
        primary_key=True,
        help_text='User sub as referred by the LTI platform',
    )

    name = models.CharField(
        max_length=50,
        blank=True,
        help_text='User name in LTI platform',
    )

    email = models.EmailField(
        null=True,
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

    def is_student(self) -> bool:
        return self.check_role(self.roles, self.STUDENT_ROLES)

    def is_instructor(self) -> bool:
        return self.check_role(self.roles, self.INSTRUCTOR_ROLES)

    def check_role(self, roles, role_set) -> bool:
        return any([role in role_set for role in roles])
