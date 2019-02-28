import asyncio
import aiohttp

from algoliasearch.http.transporter import Response, Request


class RequesterAsync(object):

    @asyncio.coroutine
    def send(self, request):
        # type: (Request) -> Response  # noqa: E501

        connector = aiohttp.TCPConnector(use_dns_cache=False)

        session = aiohttp.ClientSession(connector=connector,
                                        timeout=request.connect_timeout)

        request = session.request(
            method=request.verb, url=request.url,
            headers=request.headers,
            data=request.data_as_string,
            timeout=request.timeout,
        )

        try:
            response = yield from request
            json = yield from response.json()
        except asyncio.TimeoutError as e:
            return Response(error_message=str(e),
                            is_timed_out_error=True)
        # @todo Check if there is an Request Exception here.
        finally:
            yield from session.close()

        return Response(
            response.status,
            json,
            response.reason
        )
