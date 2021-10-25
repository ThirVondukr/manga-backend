import pytest

from db.models.manga import Manga


@pytest.mark.asyncio
async def test_can_retrieve_manga_by_id(session, http_client):
    manga = Manga(title="title", title_slug="title")
    session.add(manga)
    await session.commit()
    await session.refresh(manga)

    query = """
    query($mangaId: UUID!) {
        getMangaById(mangaId: $mangaId) {
            id
        }
    }
    """
    variables = {"mangaId": str(manga.id)}
    result = await http_client.post("/graphql/", json={"query": query, "variables": variables})
    result_json = result.json()
    assert result_json.get("errors") is None
    assert result_json["data"]["getMangaById"]["id"] == str(manga.id)
