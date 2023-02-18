from django.test import TestCase
from django.urls import resolve, reverse

from apps.center import views

UUID = "ed1dc140-adf6-11ed-afa1-0242ac120002"


class CenterUrlsToViews(TestCase):
    def test_does_center_home_point_to_correct_view(self):
        view = resolve(reverse("center_home"))
        self.assertIs(view.func, views.center_home)

    def test_does_center_list_point_to_correct_view(self):
        view = resolve(reverse("center_list"))
        self.assertIs(view.func, views.center_list)

    def test_does_center_detail_point_to_correct_view(self):
        view = resolve(reverse("center_detail", kwargs={"pk": UUID}))
        self.assertIs(view.func, views.center_detail)

    def test_does_center_create_point_to_correct_view(self):
        view = resolve(reverse("center_create"))
        self.assertIs(view.func, views.center_create)

    def test_does_center_update_info_point_to_correct_view(self):
        view = resolve(reverse("center_update_info", kwargs={"pk": UUID}))
        self.assertIs(view.func, views.center_update_info)

    def test_does_center_update_others_point_to_correct_view(self):
        view = resolve(reverse("center_update_others", kwargs={"pk": UUID}))
        self.assertIs(view.func, views.center_update_others)

    def test_does_center_update_image_point_to_correct_view(self):
        view = resolve(reverse("center_update_image", kwargs={"pk": UUID}))
        self.assertIs(view.func, views.center_update_image)

    def test_does_center_delete_point_to_correct_view(self):
        view = resolve(reverse("center_delete", kwargs={"pk": UUID}))
        self.assertIs(view.func, views.center_delete)

    def test_does_center_reinsert_point_to_correct_view(self):
        view = resolve(reverse("center_reinsert", kwargs={"pk": UUID}))
        self.assertIs(view.func, views.center_reinsert)

    def test_does_center_add_responsible_point_to_correct_view(self):
        view = resolve(reverse("center_add_responsible", kwargs={"pk": UUID}))
        self.assertIs(view.func, views.center_add_responsible)

    def test_does_center_del_responsible_point_to_correct_view(self):
        view = resolve(reverse("center_del_responsible", kwargs={"pk": 1}))
        self.assertIs(view.func, views.center_del_responsible)
