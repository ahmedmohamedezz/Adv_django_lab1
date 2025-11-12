from django.db import models
from django.conf import settings


# constraints & properties used:
# db_index (Movie)
# related_name (Tag)
# choices (Rate)
# __str__ (all models)
# null (Rate)

# Relations
# (Movie, Tag) => M-M
# (Movie, User, Rate) => relation users-(rates)-movies + extra data
# (Moive, Link) => 1-1


class Movie(models.Model):
    # often search by title => set index on title
    title = models.CharField(max_length=255, db_index=True)
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50)
    movie_id = models.ManyToManyField(Movie, related_name="tags")

    def __str__(self):
        return self.name


class Rate(models.Model):
    # constraint: limit rate to be [1, 5]
    class RatingChoices(models.IntegerChoices):
        ONE = 1, "1"
        TWO = 2, "2"
        THREE = 3, "3"
        FOUR = 4, "4"
        FIVE = 5, "5"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
    rate = models.IntegerField(choices=RatingChoices.choices)

    def __str__(self):
        return f"user: {self.user_id}, movie: {self.movie_id}, rate: {self.rate}"


class Link(models.Model):
    imdb = models.CharField(max_length=255)
    movie = models.OneToOneField(Movie, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"movie: {self.movie} => link: {self.imdb}"
