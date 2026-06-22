from pyjd.endpoints import Action
from pyjd.jd_types import Context, MenuStructure


class UI(Action, endpoint="ui"):
    def get_menu(self, context: Context) -> MenuStructure:
        """Get the custom menu structure for the desired context."""

        params = [context.value]
        resp = self.action("/getMenu", params)
        return MenuStructure(**resp)

    def invoke_action(
        self,
        context: Context,
        action_id: int,
        link_ids: list[int],
        package_ids: list[int],
    ) -> str:
        """Invoke a menu action on our selection and get the results."""

        params = [context, action_id, link_ids, package_ids]
        return self.action("/invokeAction", params)
