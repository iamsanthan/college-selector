from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from firstweb.consumers import ChatConsumer
from channels.security.websocket import AllowedHostsOriginValidator,OriginValidator

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r"^chat/(?P<username>[\w.@+-]+)",ChatConsumer),
                ]
            )
        )
    )
})