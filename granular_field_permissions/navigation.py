"""Menu items."""

from nautobot.apps.ui import NavMenuAddButton, NavMenuGroup, NavMenuItem, NavMenuTab

items = (
    NavMenuItem(
        link="plugins:granular_field_permissions:ContentTypeRuleSet_list",
        name="Granular Field Permissions",
        permissions=["granular_field_permissions.view_ContentTypeRuleSet"],
        buttons=(
            NavMenuAddButton(
                link="plugins:granular_field_permissions:ContentTypeRuleSet_add",
                permissions=["granular_field_permissions.add_ContentTypeRuleSet"],
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
