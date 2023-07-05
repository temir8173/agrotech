from django.utils.translation import gettext as _


def layout_context(request):
    menu_options = {
        '/events': _('menu_events'),
        '/services': _('menu_services'),
        '/projects': _('menu_projects'),
        '/partners': _('menu_partners'),
        '/technologies': _('menu_technologies'),
        '/farmer_training': _('menu_farmer_training'),
    }

    return {
        'menu_options': menu_options,
        'current_path': request.path,
    }
