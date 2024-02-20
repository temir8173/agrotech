from django.utils.translation import gettext as _

from base_front.models import Department


def layout_context(request):
    departments_with_services = Department.departments_with_services()

    menu_options = {
        '/events': _('menu_events'),
        '/services': {
            'name': _('menu_services'),
            'items': departments_with_services
        },
        '/projects': _('menu_projects'),
        '/partners': _('menu_partners'),
        '/store': _('menu_store'),
        # '/technologies': _('menu_technologies'),
        '/farmer_training': _('menu_farmer_training'),
    }

    return {
        'menu_options': menu_options,
        'current_path': request.path,
    }
