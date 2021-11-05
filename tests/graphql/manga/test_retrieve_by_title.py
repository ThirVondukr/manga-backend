import pytest


@pytest.mark.asyncio
async def test_returns_none_if_not_found(http_client):
    query = """
    query($titleSlug: String!) {
        getMangaByTitleSlug(titleSlug: $titleSlug) {
            id
        }
    }
    """
    variables = {"titleSlug": "title-slug"}
    result = await http_client.post("/graphql/", json={"query": query, "variables": variables})
    manga = result.json()["data"]["getMangaByTitleSlug"]
    assert manga is None


@pytest.mark.asyncio
async def test_can_retrieve_by_title(seed_manga, http_client):
    query = """
    query($titleSlug: String!) {
        getMangaByTitleSlug(titleSlug: $titleSlug) {
            id
            title
            titleSlug
        }
    }
    """
    variables = {"titleSlug": seed_manga.title_slug}
    result = await http_client.post("/graphql/", json={"query": query, "variables": variables})
    manga = result.json()["data"]["getMangaByTitleSlug"]
    assert manga is not None
    assert manga["id"] == str(seed_manga.id)
