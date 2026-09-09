from __future__ import annotations

from src.core.base_actions import PageActions
from src.page_objects.cofee.create_group_po import CreateGroupPage


class CreateGroupActions(PageActions):
    def __init__(self, driver, settings=None):
        super().__init__(driver, settings)
        self.page = CreateGroupPage(driver, self.settings)

    def wait_for_form(self, timeout: int | None = None) -> None:
        self._wait(timeout).until(lambda _: self.page.is_loaded(timeout=2))

    def enter_group_name(self, name: str) -> None:
        self.type_text(self.page.find_input_group_name(), name)
        self.hide_keyboard()

    def enter_amount(self, amount: str) -> None:
        self.type_text(self.page.find_input_amount(), amount)
        self.hide_keyboard()

    def enter_member_amount(self, amount: str) -> None:
        # The member row (and its amount field) sits inside a Flutter
        # ListView -- confirmed live to sometimes not be attached to the
        # accessibility tree until scrolled into view, even with only one
        # member. scroll_until_visible is a no-op swipe if it's already on
        # screen.
        by, value = self.page.loc_input_member_amount()
        element = self.scroll_until_visible(by, value)
        self.type_text(element, amount)
        self.hide_keyboard()

    def accept_default_fee_collection_day(self) -> None:
        self.tap(self.page.find_btn_fee_collection_day())
        self.tap(self.page.find_btn_apply())

    def tap_save(self) -> None:
        self.tap(self.page.find_btn_save())
