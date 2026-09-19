from app.agent.router import RequestRouter


def test_router_examples():
    router = RequestRouter()
    assert router.route("Where is my order O10025?") == ("delivery", "track_order")
    assert router.route("What tools manage orders?") == ("system", "system_search")
    assert router.route("What is the shipping policy?") == ("knowledge", "knowledge_search")
