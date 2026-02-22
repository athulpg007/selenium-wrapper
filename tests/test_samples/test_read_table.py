import time

from elements import read_table


class TestReadTable:
    def test_read_table(self, browser):
        browser.navigate("https://practicetestautomation.com/practice-test-table/")
        browser.click(read_table.lang_java)
        time.sleep(3)
