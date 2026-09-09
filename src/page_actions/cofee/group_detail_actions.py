from __future__ import annotations

from src.core.base_actions import PageActions
from src.page_objects.cofee.group_detail_po import GroupDetailPage


class GroupDetailActions(PageActions):
    def __init__(self, driver, settings=None):
        super().__init__(driver, settings)
        self.page = GroupDetailPage(driver, self.settings)

    def wait_for_loaded(self, timeout: int | None = None) -> None:
        self._wait(timeout).until(lambda _: self.page.is_loaded(timeout=2))

    def dismiss_share_prompt_if_present(self) -> None:
        if self.page.is_share_later_visible(timeout=3):
            self.tap(self.page.find_btn_share_later())
