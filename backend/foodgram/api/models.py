from django.db import models
from users.models import User
from django.core.validators import MinValueValidator, RegexValidator
from django.db.models import UniqueConstraint


class Ingredient(models.Model):
    name = models.CharField('Название продукта',
                            max_length=200)
    measurement_unit = models.CharField('Единица измерения',
                                        max_length=200)
    
    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField('Название',
                            max_length=200,
                            unique=True)
    color = models.CharField('Цвет в HEX',
                             max_length=7,
                             unique=True,
                             validators=[
                                 RegexValidator(
                                     regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                                     message='Введите значение цвета в формате HEX')])
    slug = models.CharField('Уникальный слаг',
                            max_length=200,
                            unique=True,
                            db_index=True)
    
    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientsInRecipe',
                                         related_name='recipes')
    tags = models.ManyToManyField(Tag,
                                  related_name='recipes')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes')
    name = models.CharField('Название', max_length=200)
    image = models.ImageField('Картинка с блюдом',
                              upload_to='images/')
    text = models.TextField('Описание')
    cooking_time = models.IntegerField('Время приготовления в минутах')

    def __str__(self) -> str:
        return self.name


class IngredientsInRecipe(models.Model):
    '''Модель для связи рецепта и ингредиентов.'''
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        'Колличество',
        validators=[
            MinValueValidator(
                1, 'Колличество ингредиента в рецептне не может быть менее 1.'
            )
        ]
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique ingredients recipe')
        ]


class Favorite(models.Model):
    '''Избранные рецепты.'''
    user = models.ForeignKey(
        User,
        related_name='Favorite_Recipe',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='Favorite_Recipe',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'recipe'],
                             name='unique_favorite')
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='cart')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='cart')
    
    class Meta:
        ordering = ['-id']
        verbose_name = 'Shopping list'
        verbose_name_plural = 'Shopping lists'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_cart_user')
        ]