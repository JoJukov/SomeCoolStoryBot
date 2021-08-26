import vk_api

class VkPoster:

    def __init__(self, auth, group_id):
        '''

        Parameters
        ------------------
        `auth`
            Auth data from `VkAuth`.
        `group_id` : `int`
            Id of the group to post in
        '''

        self._group_id = group_id

        vk_session = vk_api.VkApi(login=auth[0], password=auth[1])
        vk_session.auth()

        self._vk = vk_session.get_api()

    def post(self, message, photo):
        '''
        Parameters
        ------------------
        `message` : `str`
            Text for post
        `photo`
            Path to photo or file-like object

        Example
        -------------------
        Posting file from *url* to group with *id*

        ```python
        from vk import VkAuth, VkPoster
        poster = VkPoster(VKAuth.fromEnv(), id)
        im = requests.get(url, stream=True).raw
        p.post('Some text', im)
        ```
        '''

        self._vk.wall.post(
            owner_id = -self._group_id,
            message=message,
            attachments=self._uploadPhoto(photo),
            from_group = 1,
        )


    def _uploadPhoto(self, photo):
        resp = vk_api.upload.VkUpload(self._vk).photo_wall(photo, group_id=self._group_id)[0]

        # TODO: len(resp) == 0

        return f'photo{resp["owner_id"]}_{resp["id"]}'
