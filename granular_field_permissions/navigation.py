"""Menu items."""

from nautobot.apps.ui import NavMenuAddButton, NavMenuGroup, NavMenuItem, NavMenuTab

items = (
    NavMenuItem(
        link="plugins:granular_field_permissions:granularfieldpermissionsexamplemodel_list",
        name="Granular Field Permissions",
        permissions=["granular_field_permissions.view_granularfieldpermissionsexamplemodel"],
        buttons=(
            NavMenuAddButton(
                link="plugins:granular_field_permissions:granularfieldpermissionsexamplemodel_add",
                permissions=["granular_field_permissions.add_granularfieldpermissionsexamplemodel"],
            ),
        ),
    ),
)

menu_items = (
    NavMenuTab(
        name="Apps",
        groups=(NavMenuGroup(name="Granular Field Permissions", items=tuple(items)),),
    ),
)
