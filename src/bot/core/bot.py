import os
import random
import string
from dataclasses import dataclass

import requests


@dataclass
class URLs:
    """
    Class stores urls
    """

    signup_user_url: str = 'http://localhost:8000/api/users/register/'
    login_user_url: str = 'http://localhost:8000/api/users/login/'
    posts_url: str = 'http://localhost:8000/api/posts/post/'


@dataclass
class UsersData:
    """
    Class stores files paths
    """

    usernames: str = '../assets/usernames.txt'
    first_names: str = '../assets/first_names.txt'
    last_names: str = '../assets/last_names.txt'
    emails: str = '../assets/emails.txt'
    phones: str = '../assets/phones.txt'


class Bot(UsersData, URLs):
    """
    Class for demonstrate API functionalities
    """

    @classmethod
    def read_config(cls) -> list:
        """
        Method reads config file and getting counts of objects to create
        :return: list - objects count
        """

        users_count = cls._get_max_numbers_of_chosen_object(0)
        posts_count = cls._get_max_numbers_of_chosen_object(1)
        likes_count = cls._get_max_numbers_of_chosen_object(2)
        return [users_count, posts_count, likes_count]

    @classmethod
    def register_user(cls) -> None:
        """
        Method creates user
        :return: None
        """

        data = cls._initialize_user_data()
        requests.post(cls.signup_user_url, data=data)

    @classmethod
    def login_user(cls) -> list:
        """
        Method login user and returns access token
        :return: list - users access tokens
        """

        access_tokens = []
        with open('../users/registered.csv', 'r') as file:
            lines = file.readlines()
            usernames = [line.split(',')[0] for line in lines]
            passwords = [line.split(',')[-1] for line in lines]
            for username, password in zip(usernames, passwords):
                response = requests.post(
                    cls.login_user_url,
                    data={
                        'username': username,
                        'password': password
                    }
                )
                tokens = response.json()
                access_tokens.append(tokens.get('access'))

        return access_tokens

    @classmethod
    def create_post(cls, access_token: str) -> None:
        """
        Method creates post with user by access token
        :param access_token: str - user's access token
        :return: None
        """

        characters = string.ascii_letters + string.digits + string.punctuation
        title = ''.join(random.choice(characters) for i in range(16))
        text = ''.join(random.choice(characters) for i in range(64))
        requests.post(
            cls.posts_url, data={'title': title, 'text': text},
            headers={'Authorization': f'Bearer {access_token}'}
        )

    @classmethod
    def get_posts(cls) -> list:
        """
        Method gets posts list and returns posts ids list
        :return: list - posts ids
        """

        response = requests.get(cls.posts_url)
        posts = response.json()
        posts_ids = [post.get('id') for post in posts]
        return posts_ids

    @classmethod
    def like_posts_randomly(cls, access_token: str, post_ids: list, likes: int):
        """
        Method randomly likes post with id from post_ids list
        :param access_token: str - user's access token
        :param post_ids: list - posts ids
        :param likes: int - likes count from config
        :return:
        """

        for i in range(likes):
            chosen_id = random.choice(post_ids)
            url = f'http://localhost:8000/api/posts/{chosen_id}/like/'
            requests.post(
                url, headers={'Authorization': f'Bearer {access_token}'}
            )

    @classmethod
    def _initialize_user_data(cls) -> dict:
        """
        Method initializing dict with user fields for registration
        :return: dict - user fields
        """

        password = cls._generate_password()
        data = {
            'username': cls._get_random_element(cls.usernames),
            'email': cls._get_random_element(cls.emails),
            'first_name': cls._get_random_element(cls.first_names),
            'last_name': cls._get_random_element(cls.last_names),
            'phone': cls._get_random_element(cls.phones),
            'password': password,
            'password2': password,
        }
        cls._save_registered_user_into_file(data)

        return data

    @staticmethod
    def _read_file(file_path: str) -> list:
        """
        Method reads files and returns list of lines
        :param file_path: str - path to file
        :return: list - lines from file
        """

        with open(file_path, 'r') as file:
            lines = file.readlines()

        return lines

    @classmethod
    def _get_random_element(cls, data_field: str) -> str:
        """
        Method chooses random element from user data list
        :param data_field: str - file path to user data
        :return: str - user data element from list
        """

        data_list = cls._read_file(data_field)
        return random.choice(data_list).replace('\n', '')

    @staticmethod
    def _generate_password() -> str:
        """
        Method generates random string to use in password for user registration
        :return: str - password string
        """

        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(8))
        return password.replace(',', '')

    @classmethod
    def _get_max_numbers_of_chosen_object(cls, choice_index: int) -> int:
        """
        Method returns count of users, posts or likes
        :param choice_index: int - (users=0, posts=1, likes=2)
        :return: int - count of chosen object
        """

        choice = cls._read_file('../config.csv')[choice_index]
        return int(choice.split(',')[1].replace('\n', ''))

    @staticmethod
    def _save_registered_user_into_file(user_data: dict) -> None:
        """
        Method saves user registration data to file
        :param user_data: dict - fields of registration
        :return: None
        """
        file_name = '../users/registered.csv'
        data = user_data.values()

        if os.path.exists(file_name):
            mode = 'a'
        else:
            mode = 'w'

        with open(file_name, mode) as file:
            file.write(','.join(data) + '\n')


class Run(Bot):
    @classmethod
    def start_process(cls):
        users, posts, likes = cls.read_config()
        for i in range(users):
            cls.register_user()

        access_tokens = cls.login_user()
        for access_token in access_tokens:
            posts_to_create = random.randint(1, posts)
            for posts_count in range(posts_to_create):
                cls.create_post(access_token)

            posts_ids = cls.get_posts()
            cls.like_posts_randomly(access_token, posts_ids, likes)


Run().start_process()
