from __future__ import annotations

from src.core.base_actions import PageActions
from src.page_objects.cofee.add_member_po import AddMemberPage


class AddMemberActions(PageActions):
    def __init__(self, driver, settings=None):
        super().__init__(driver, settings)
        self.page = AddMemberPage(driver, self.settings)

    def wait_for_select_members_modal(self, timeout: int | None = None) -> None:
        self._wait(timeout).until(lambda _: self.page.is_select_members_modal_visible(timeout=2))

    def tap_manually(self) -> None:
        self.tap(self.page.find_btn_manually())

    def wait_for_add_member_screen(self, timeout: int | None = None) -> None:
        self._wait(timeout).until(lambda _: self.page.is_add_member_screen_visible(timeout=2))

    def enter_name(self, name: str) -> None:
        self.type_text(self.page.find_input_name(), name)

    def enter_mobile(self, mobile: str) -> None:
        self.type_text(self.page.find_input_mobile(), mobile)

    def tap_add(self) -> None:
        self.tap(self.page.find_btn_add())
