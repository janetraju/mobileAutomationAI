from __future__ import annotations

from src.core.base_actions import PageActions
from src.page_objects.cofee.home_po import HomePage


class HomeActions(PageActions):
    def __init__(self, driver, settings=None):
        super().__init__(driver, settings)
        self.page = HomePage(driver, self.settings)

    def wait_for_home(self, timeout: int | None = None) -> None:
        self._wait(timeout).until(lambda _: self.page.is_loaded(timeout=2))

    def tap_add_new(self) -> None:
        self.tap(self.page.find_btn_add_new())
