from django.shortcuts import get_object_or_404
from rest_framework import renderers, status
from rest_framework.response import Response

from catalog.models import RealEstate


class FavoriteMixin:
    """Добавление и удаление объекта в избранное"""

    def add_object(self, request, *args, **kwargs):
        """Добавляет объект"""
        try:
            real_estate = get_object_or_404(RealEstate, id=kwargs['pk'])
        except ValueError:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )
        model = kwargs['model']
        user = request.user
        if model.objects.filter(user=user, real_estate=real_estate).exists():
            return Response(
                {'errors': 'Такой объект уже есть'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        model.objects.create(user=user, real_estate=real_estate)
        return Response(status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_object(request, *args, **kwargs):
        """Удаляет объект"""
        real_estate = get_object_or_404(RealEstate, id=kwargs['pk'])
        model = kwargs['model']
        user = request.user
        if not model.objects.filter(
            user=user, real_estate=real_estate
        ).exists():
            return Response(
                {'errors': 'Такого объекта нет'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        model.objects.get(user=user, real_estate=real_estate).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StaffBrowsableAPIMixin:
    def get_renderers(self):
        # explicitly set renderer to JSONRenderer (the default for non
        # staff users)
        rends = [renderers.JSONRenderer]
        if self.request.user.is_staff:
            # staff users see browsable API
            rends.append(renderers.BrowsableAPIRenderer)
        return [renderer() for renderer in rends]
