from __future__ import annotations

from src.core.base_actions import PageActions
from src.page_objects.cofee.groups_list_po import GroupsListPage


class GroupsListActions(PageActions):
    def __init__(self, driver, settings=None):
        super().__init__(driver, settings)
        self.page = GroupsListPage(driver, self.settings)

    def go_to_groups_tab(self) -> None:
        self.tap(self.page.find_tab_groups())
        self._wait().until(lambda _: self.page.is_loaded(timeout=2))

    def wait_for_group_card(self, group_name: str, timeout: int | None = None) -> bool:
        return self.page.is_group_card_visible(group_name, timeout=timeout)
