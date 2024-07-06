import aiohttp
import asyncio


class Requester:

    sess = None

    @classmethod
    async def request(cls, url, method, params=None, data=None, json=None, **kwargs):

        if json is None:
            response = await cls.sess.request(url=url, method=method, params=params, data=data)
        else:
            response = await cls.sess.request(url=url, method=method, params=params, json=json)
        return await response.text()

    @classmethod
    def get_sem(cls):
        return asyncio.Semaphore(30)

    @classmethod
    def init_sess(cls):
        cls.sess = aiohttp.ClientSession()

    @classmethod
    async def sess_close(cls):
        await cls.sess.close()




