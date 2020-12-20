import pathlib
from enum import Enum
from typing import Optional

import youtube_dl
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import (
    presence_of_element_located)
from selenium.webdriver.support.wait import WebDriverWait

USER = 'user@email.com'
PASSWORD = 'password'


class Courses(Enum):
    REAPRENDIZAGEM = 'Reaprendizagem Criativa'
    CRICRICRI = 'CriCriCri'
    TECNICAS = 'Técnicas de Criatividade'
    DESCONSTRUINDO = 'Desconstruindo Apresentações'


BASE_URL = 'https://www.keeplearning.school/'
LOGIN_URL = BASE_URL + 'login'
COURSE_URL = {
    Courses.REAPRENDIZAGEM: 'turma/reaprendizagem-criativa-turma-zero',
    Courses.CRICRICRI: 'turma/turma-2020',
    Courses.TECNICAS: 'turma/tecnicas-de-criatividade-gravidade-zero',
    Courses.DESCONSTRUINDO: 'turma/turma-1-desconstruindo-apresentacoes',
}
for k, v in COURSE_URL.items():
    COURSE_URL[k] = BASE_URL + v

COURSES_PATH = pathlib.Path('courses')


def main():
    with webdriver.Firefox() as driver:

        # TODO: get course to be downloaded from command line args;

        create_downloaded_courses_dir()

        # TODO: if course param is None, call download_course() for each course;

        course = Courses.CRICRICRI
        # course = Courses.REAPRENDIZAGEM
        # course = Courses.TECNICAS
        # course = Courses.DESCONSTRUINDO

        download_course(driver, course)


def download_course(driver: WebDriver, course: Courses) -> None:
    driver.get(COURSE_URL[course])

    if driver.current_url == LOGIN_URL:
        login(driver)

    course_path = create_course_dir(str(course.value))

    modules = get_modules(driver)
    for module in modules:
        title = get_module_title(module)
        print(f'Downloading "{title}" module...')
        module_path = create_module_dir(course_path, modules.index(module) + 1,
                                        title)

        lessons = get_lessons(module)

        for lesson in lessons:
            print(f'Downloading "{lesson.text}" lesson...')
            download_lesson(driver, lesson, module_path)

        print(f'"{title}" module download completed.', end='\n\n')


def download_lesson(driver: WebDriver,
                    lesson: WebElement,
                    module_path: pathlib.Path) -> None:
    lesson_url = lesson.get_attribute('href')

    course_page = driver.current_window_handle

    driver.execute_script('window.open()')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(lesson_url)

    youtube_url = get_youtube_url(driver)
    if youtube_url is not None:

        # BUG: the output option is not working; fix it;
        output_path = module_path / '%(title)s.%(ext)s'
        ydl_opts = {
            'output': str(output_path),
            'retries': 10,
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
        except youtube_dl.utils.DownloadError as e:
            print(e)

    driver.close()
    driver.switch_to.window(course_page)


def get_youtube_url(driver: WebDriver) -> Optional[str]:
    wait = WebDriverWait(driver, 10)
    try:
        element = wait.until(presence_of_element_located((By.ID, 'ytplayer')))
        return element.get_attribute('src')
    except TimeoutException:
        print('Could not find youtube embedded video for this lesson')


def get_lessons(module: WebElement) -> list[WebElement]:
    return module.find_elements(By.XPATH, './/*[@class="course__lesson-item"]')


def create_module_dir(course_path: pathlib.Path,
                      index: int,
                      title: str) -> pathlib.Path:
    dir_name = str(index) + ' - ' + title
    for char in r'\/:*?"<>|':
        dir_name = dir_name.replace(char, '')
    module_path = course_path / dir_name
    module_path.mkdir(exist_ok=True)
    return module_path


def get_module_title(module: WebElement) -> str:
    title = module.find_element(By.XPATH,
                                './/*[@class="course__title text-center"]')
    return title.text


def get_modules(driver: WebDriver) -> list[WebElement]:
    wait = WebDriverWait(driver, 10)
    modules = wait.until(presence_of_element_located((By.CLASS_NAME, 'course')))
    return modules.find_elements(By.XPATH, '//*[@class="course__item"]')


def create_course_dir(course_name: str) -> pathlib.Path:
    path = COURSES_PATH / course_name
    path.mkdir(exist_ok=True)
    return path


def login(driver: WebDriver) -> None:
    wait = WebDriverWait(driver, 10)

    email_input = wait.until(presence_of_element_located((By.ID, 'user_login')))
    email_input.send_keys(USER)

    password_input = wait.until(presence_of_element_located((By.ID,
                                                             'user_password')))
    password_input.send_keys(PASSWORD)

    login_button = wait.until(presence_of_element_located(
        (By.XPATH, '//*[@value="Login"]')))
    login_button.click()


def create_downloaded_courses_dir() -> None:
    path = COURSES_PATH
    path.mkdir(exist_ok=True)


if __name__ == '__main__':
    main()
