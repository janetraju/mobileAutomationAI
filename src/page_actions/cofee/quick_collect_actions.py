"""Quick Collect payment-request interactions for CoFee."""

from __future__ import annotations

from appium.webdriver.webdriver import WebDriver
from selenium.common.exceptions import TimeoutException

from src.core.page_actions import PageActions
from src.page_objects.cofee.quick_collect_po import QuickCollectPo


class QuickCollectActions(PageActions):
    """Business logic for creating a payment request via Quick Collect."""

    def __init__(self, driver: WebDriver) -> None:
        self._qc_po = QuickCollectPo(driver)
        super().__init__(driver, self._qc_po)

    def _type_into_field_at_index(self, index: int, text: str) -> None:
        """Type char-by-char into the EditText at `index` (Flutter re-renders on input)."""
        fields = self._driver.find_elements(*self._qc_po.loc_edittext_field())
        self.tap(fields[index])
        for char in text:
            fields = self._driver.find_elements(*self._qc_po.loc_edittext_field())
            fields[index].send_keys(char)

    def select_member_from_group(self, member_name: str) -> None:
        """Choose 'From Group Members' and select the given member."""
        from_group = self.wait_for_element_visible(self._qc_po.loc_from_group_members(), timeout=10)
        self.tap(from_group)
        checkbox = self.wait_for_element_visible(
            self._qc_po.loc_member_checkbox(member_name), timeout=10
        )
        self.tap(checkbox)
        add_button = self.wait_for_element_visible(self._qc_po.loc_add_members(), timeout=10)
        self.tap(add_button)

    def enter_amount_and_note(self, amount: int, note: str) -> None:
        """Enter a custom amount and required note on the amount-entry screen."""
        self.wait_for_element_visible(self._qc_po.loc_enter_amount_title(), timeout=10)
        fields = self._driver.find_elements(*self._qc_po.loc_edittext_field())
        if len(fields) < 2:
            raise TimeoutException("Expected amount and note EditText fields, found fewer")
        self._type_into_field_at_index(0, str(amount))
        self._type_into_field_at_index(1, note)
        self.hide_keyboard()

    def submit_payment_link(self) -> None:
        """Tap Send Payment Link and wait for the success confirmation."""
        send_button = self.wait_for_element_visible(self._qc_po.loc_send_payment_link(), timeout=10)
        self.tap(send_button)
        self.wait_for_element_visible(self._qc_po.loc_success_message(), timeout=15)

    def return_to_group_detail(self) -> None:
        """Tap Go Back on the success screen."""
        go_back = self.wait_for_element_visible(self._qc_po.loc_go_back(), timeout=10)
        self.tap(go_back)

    def create_payment_request(self, member_name: str, amount: int, note: str) -> None:
        """Full Quick Collect flow: select member, enter amount/note, submit, return."""
        self.select_member_from_group(member_name)
        self.enter_amount_and_note(amount, note)
        self.submit_payment_link()
        self.return_to_group_detail()
