from django.utils.translation import gettext as _


def layout_context(request):
    menu_options = {
        '/events': _('menu_events'),
        '/consulting': _('menu_consulting'),
        '/services': _('menu_services'),
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
