from selenium.webdriver.common.by import By
from model.project import Project


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def open_project_page(self):
        wd = self.app.wd
        wd.find_element(By.LINK_TEXT, "Manage").click()
        wd.find_element(By.LINK_TEXT, "Manage Projects").click()

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        wd.find_element(By.NAME, field_name).click()
        wd.find_element(By.NAME, field_name).clear()
        wd.find_element(By.NAME, field_name).send_keys(text)

    def fill_project_form(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.name)
        self.change_field_value("description", project.description)

    def create_project(self, new_project):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element(By.XPATH, "//input[@value='Create New Project']").click()
        self.fill_project_form(new_project)
        wd.find_element(By.XPATH, "//input[@value='Add Project']").click()
        self.project_cache = None

    project_cache = None

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_project_page()
            self.project_cache = []
            proj_table = wd.find_element(By.XPATH, "//table[3]/tbody")
            rows = proj_table.find_elements(By.TAG_NAME, "tr")[2:]
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                name = cells[0].find_element(By.TAG_NAME, "a").get_attribute("text")
                description = cells[4].text
                self.project_cache.append(Project(name=name, description=description))
        return list(self.project_cache)

    def delete_project_by_name(self, name):
        wd = self.app.wd
        self.open_project_page()
        wd.find_element(By.LINK_TEXT, name).click()
        wd.find_element(By.XPATH, "//input[@value='Delete Project']").click()
        wd.find_element(By.XPATH, "//input[@value='Delete Project']").click()
        self.project_cache = None
