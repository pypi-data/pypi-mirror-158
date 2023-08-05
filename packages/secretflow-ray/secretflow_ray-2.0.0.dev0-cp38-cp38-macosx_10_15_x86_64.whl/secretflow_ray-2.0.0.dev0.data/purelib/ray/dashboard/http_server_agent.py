import asyncio
import logging

from distutils.version import LooseVersion

import ray.dashboard.optional_utils as dashboard_optional_utils

from ray.dashboard.optional_deps import aiohttp, aiohttp_cors, hdrs

logger = logging.getLogger(__name__)
routes = dashboard_optional_utils.ClassMethodRouteTable


class HttpServerAgent:
    def __init__(self, ip, listen_port):
        self.ip = ip
        self.listen_port = listen_port
        self.http_host = None
        self.http_port = None
        self.http_session = None
        self.runner = None

        # Create a http session for all modules.
        # aiohttp<4.0.0 uses a 'loop' variable, aiohttp>=4.0.0 doesn't anymore
        if LooseVersion(aiohttp.__version__) < LooseVersion("4.0.0"):
            self.http_session = aiohttp.ClientSession(loop=asyncio.get_event_loop())
        else:
            self.http_session = aiohttp.ClientSession()

    async def start(self, modules):
        # Bind routes for every module so that each module
        # can use decorator-style routes.
        for c in modules:
            dashboard_optional_utils.ClassMethodRouteTable.bind(c)

        app = aiohttp.web.Application()
        app.add_routes(routes=routes.bound_routes())

        # Enable CORS on all routes.
        cors = aiohttp_cors.setup(
            app,
            defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True,
                    expose_headers="*",
                    allow_methods="*",
                    allow_headers=("Content-Type", "X-Header"),
                )
            },
        )
        for route in list(app.router.routes()):
            cors.add(route)

        self.runner = aiohttp.web.AppRunner(app)
        await self.runner.setup()
        site = aiohttp.web.TCPSite(
            self.runner,
            "127.0.0.1" if self.ip == "127.0.0.1" else "0.0.0.0",
            self.listen_port,
        )
        await site.start()
        self.http_host, self.http_port, *_ = site._server.sockets[0].getsockname()
        logger.info(
            "Dashboard agent http address: %s:%s", self.http_host, self.http_port
        )

        # Dump registered http routes.
        dump_routes = [r for r in app.router.routes() if r.method != hdrs.METH_HEAD]
        for r in dump_routes:
            logger.info(r)
        logger.info("Registered %s routes.", len(dump_routes))

    async def cleanup(self):
        # Wait for finish signal.
        await self.runner.cleanup()
