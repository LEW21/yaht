from __future__ import annotations

from typing import Union
from multidict import CIMultiDict
import aiohttp


def serialize(body):
	return TypedBytes('application/json', json.dumps(serialize(body).encode('utf-8')))


class Resource:
	def __init__(self, url):
		self._url = url

	def __str__(self):
		return self._url


class SessionBoundResource(Resource):
	def __init__(self, url, session: Session):
		super().__init__(url)
		self._session = session

	async def request(self, method: str, body = None, *, headers = None) -> HTTP2xx_Success:
		raw_body: TypedBytes = serialize(body) if body else None

		resp = await self._session._aiohttp_session.request(
			method,
			self.url,
			headers = CIMultiDict([
				*headers.items(), 
				*([('Content-Type', raw_body.type)] if raw_body is not None else []),
			]),
			data = raw_body.value if raw_body is not None else None,
		)

		response = responses[resp.status_code](resp.headers, resp.content)

		if not response.ok:
			raise response

		return response

	async def get(self, *, headers) -> HTTP2xx_Success:
		return await self.request('GET', headers = headers)

	async def post(self, data, *, headers) -> HTTP2xx_Success:
		return await self.request('POST', data, headers = headers)

	async def patch(self, data, *, headers) -> HTTP2xx_Success:
		return await self.request('PATCH', data, headers = headers)

	async def put(self, data, *, headers) -> HTTP2xx_Success:
		return await self.request('PUT', data, headers = headers)

	async def delete(self, *, headers) -> HTTP2xx_Success:
		return await self.request('DELETE', headers = headers)


class Session:
	def __init__(self):
		self._aiohttp_session = aiohttp.ClientSession()

	def __getitem__(self, url: Union[str, Resource]):
		return SessionBoundResource(str(url), self)
