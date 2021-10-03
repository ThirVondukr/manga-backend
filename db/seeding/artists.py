from faker import Faker

from db.models.manga import Manga, Author, AuthorRelationship, AuthorRelationshipType

_fake = Faker()


def create_manga_author(manga: Manga):
    author = Author(name=_fake.name())
    relationships = [
        AuthorRelationship(author=author, manga=manga, type=AuthorRelationshipType.artist),
        AuthorRelationship(author=author, manga=manga, type=AuthorRelationshipType.writer),
    ]
    return author, relationships
