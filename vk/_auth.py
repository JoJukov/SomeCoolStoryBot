import stdiomask
import os

class VkAuth:

    @staticmethod
    def fromPrompt():
        '''
        Gets login and password from input prompt
        '''

        login = input("Login: ")
        password = stdiomask.getpass("Password: ")

        return (login, password)

    @staticmethod
    def fromRaw(login, password):
        '''
        Provide login and password explicitly

        Parameters
        -----------------
        `login` : `str`
        `password` : `str`
        '''

        return (login, password)

    @staticmethod
    def fromEnv(login="VK_LOGIN", password="VK_PASSWORD"):
        '''
        Acquire login and password from environment variable

        Parameters
        -----------------
        `login` : `str`, optional
           login variable, default `VK_LOGIN`
        `password` : `str`, optional
           login variable, default `VK_PASSWORD`
        '''
        return (os.getenv(login), os.getenv(password))
