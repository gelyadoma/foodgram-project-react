from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer, UserCreateSerializer
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Follow

from .models import Ingredient, Tag, Recipe, IngredientInRecipe, Favorite, ShoppingCart

User = get_user_model()


class CreateUserSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
            )
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True},
        }


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
            )
        
    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientInRecipe.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class RecipeGetSerializer(serializers.ModelSerializer):
    '''Сериализатор для модели Recipe.
 Для GET запросов к эндпоинтам /recipe/ и /recipe/id/.
    '''
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer()
    ingredients = IngredientInRecipeSerializer(
        source='IngredientsInRecipe',
        many=True,
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False

        return Favorite.objects.filter(recipe=obj, user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request.user.is_anonymous:
            return False

        return ShoppingCart.objects.filter(
            recipe=obj, user=request.user
        ).exists()


class RecipePostSerializer(serializers.ModelSerializer):
    author = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientInRecipeSerializer(
        source='IngredientsInRecipe',
        many=True,
    )
    image = Base64ImageField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    @staticmethod
    def create_ingredients(recipe, ingredients):
        ingredients_list = []
        for ingredient in ingredients:
            current_ingredient = ingredient['ingredient']['id']
            current_amount = ingredient.get('amount')
            ingredients_list.append(
                IngredientInRecipe(
                    recipe=recipe,
                    ingredient=current_ingredient,
                    amount=current_amount
                )
            )
        IngredientInRecipe.objects.bulk_create(ingredients_list)

    def validate(self, data):
        ingredients_list = []
        ingredients_in_recipe = data.get('IngredientsInRecipe')
        for ingredient in ingredients_in_recipe:
            if ingredient.get('amount') < 0:
                raise serializers.ValidationError(
                    'Убедитесь, что значение'
                    'количества ингредиента больше 0')
            ingredients_list.append(ingredient['ingredient']['id'])
        if len(ingredients_list) > len(set(ingredients_list)):
            raise serializers.ValidationError('Ингредиенты должны '
                                              'быть уникальными')
        return data

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('IngredientsInRecipe')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data, author=author)
        recipe.tags.add(*tags)
        self.save_ingredients(recipe, ingredients)

        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        IngredientInRecipe.objects.filter(recipe=instance).delete()
        self.create_ingredients(
            validated_data.get('ingredients'), instance
            )
        return instance

    def to_representation(self, instance):
        serializer = RecipeGetSerializer(
            instance,
            context={'request': self.context.get('request')}
        )
        return serializer.data

# class RecipesSerializer(serializers.ModelSerializer):
#     author = UserSerializer(read_only=True)
#     tags = TagSerializer(many=True, read_only=True)
#     ingredients = IngredientInRecipeSerializer(many=True, read_only=True,
#                                                source='IngredientInRecipe_set')
#     is_favorited = serializers.SerializerMethodField()
#     is_in_shopping_cart = serializers.SerializerMethodField()
#     image = Base64ImageField()

#     class Meta:
#         model = Recipe
#         fields = (
#             'id',
#             'tags',
#             'author',
#             'ingredients',
#             'is_favorited',
#             'is_in_shopping_cart',
#             'name',
#             'image',
#             'text',
#             'cooking_time')

#     def validate(self, data):
#         ingredients = self.initial_data.get('ingredients')
#         if not ingredients:
#             raise serializers.ValidationError({
#                 'ingredients': 'Нужен хоть один ингредиент для рецепта'})
#         ingredient_list = []
#         for ingredient_item in ingredients:
#             ingredient = get_object_or_404(Ingredient,
#                                            id=ingredient_item['id'])
#             if ingredient in ingredient_list:
#                 raise serializers.ValidationError('Ингредиенты должны '
#                                                   'быть уникальными')
#             ingredient_list.append(ingredient)
#             if int(ingredient_item['amount']) < 0:
#                 raise serializers.ValidationError({
#                     'ingredients': ('Убедитесь, что значение количества '
#                                     'ингредиента больше 0')
#                 })
#         data['ingredients'] = ingredients
#         return data

#     def create_ingredients(self, ingredients, recipe):
#         ingredients_list = []
#         for ingredient in ingredients:
#             current_ingredient = ingredient['ingredient']['id']
#             current_amount = ingredient.get('amount')
#             ingredients_list.append(
#                 IngredientInRecipe(
#                     recipe=recipe,
#                     ingredient=current_ingredient,
#                     amount=current_amount
#                 )
#             )
#         IngredientInRecipe.objects.bulk_create(ingredients_list)

#     def create(self, validated_data):
#         image = validated_data.pop('image')
#         ingredients_data = validated_data.pop('ingredients')
#         recipe = Recipe.objects.create(image=image, **validated_data)
#         tags_data = self.initial_data.get('tags')
#         recipe.tags.set(tags_data)
#         self.create_ingredients(ingredients_data, recipe)
#         return recipe
    
#     def update(self, instance, validated_data):
#         instance.image = validated_data.get('image', instance.image)
#         instance.name = validated_data.get('name', instance.name)
#         instance.text = validated_data.get('text', instance.text)
#         instance.cooking_time = validated_data.get(
#             'cooking_time', instance.cooking_time
#         )
#         instance.tags.clear()
#         tags_data = self.initial_data.get('tags')
#         instance.tags.set(tags_data)
#         IngredientInRecipe.objects.filter(recipe=instance).all().delete()
#         self.create_ingredients(
#             validated_data.get('ingredients'), instance
#             )
#         instance.save()
#         return instance

#     def get_is_favorited(self, obj):
#         user = self.context['request'].user
#         if user.is_anonymous:
#             return False
#         return Favorite.objects.filter(user=user, recipe=obj.id).exists()

#     def get_is_in_shopping_cart(self, obj):
#         user = self.context['request'].user
#         if user.is_anonymous:
#             return False
#         return ShoppingCart.objects.filter(user=user, recipe=obj.id).exists()


class CropRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return CropRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()
