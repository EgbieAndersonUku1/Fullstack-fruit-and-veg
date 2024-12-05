
from category.models import AllDepartmentsModel


def get_all_departments(request):
    departments = AllDepartmentsModel.get_all_departments()
    return {
        "departments": departments
    }