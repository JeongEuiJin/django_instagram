from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver

User = get_user_model()

class FirstPageTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(1)

    def tearDown(self):
        self.browser.quit()

    def test_root_rul_redirect_to_post_list(self):
        self.browser.get(self.live_server_url)
        post_list_url = reverse('post:post_list')
        self.assertEqual(
            self.live_server_url+ post_list_url,
            self.browser.current_url
        )

    def test_not_authenticated_user_redirect_to_login_view(self):
        urls = [
            '/member/profile/edit/',
            '/post/create/',

        ]
        for url in urls:
            self.browser.get(self.live_server_url + url)
            self.assertEqual(
                self.live_server_url+'member/login/',
                self.browser.current_url,
            )

    def test_not_authenticated_user_can_view_login_form(self):
        self.browser.get(self.live_server_url)
        form_login = self.browser.find_element
        test_username='username'
        test_password='password'

        input_username = form_login.find_element_by_id('id_username')
        input_password = form_login.find_element_by_id('id_password')
        input_password = form_login.find_element_by_id('id_password')
        button_submit = form_login.find_element_by_tag_name('button')


    def test_not_authenticated_user_can_login(self):
        test_username = 'username'
        test_password = 'password'
        User.objects.create_user(
            username=test_username,
            password=test_password,
        )

        self.browser.get(self.live_server_url)
        form_login = self.browser.find_element_by_id()


        input_username = form_login.find_element_by_id('id_username')
        input_password = form_login.find_element_by_id('id_password')
        button_submit = form_login.find_element_by_tag_name('button')

        input_username.send_keys(test_username)
        input_password.send_keys(test_password)
        button_submit.click()
