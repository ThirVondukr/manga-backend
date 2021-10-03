import random

from faker import Faker

from db.models.manga import Manga, MangaInfo

_fake = Faker()


def create_manga_info(manga: Manga) -> MangaInfo:
    manga_info = MangaInfo(
        lang="en",
        title=manga.title,
        description="\n".join(_fake.texts(nb_texts=random.randint(3, 7))),
        manga=manga,
    )
    return manga_info
