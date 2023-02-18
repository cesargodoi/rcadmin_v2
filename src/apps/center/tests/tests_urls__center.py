from django.test import TestCase
from django.urls import reverse

UUID = "ed1dc140-adf6-11ed-afa1-0242ac120002"


class CenterUrlsTest(TestCase):
    def test_center_home_url_is_correct(self):
        self.assertEqual(reverse("center_home"), "/center/")

    def test_center_list_url_is_correct(self):
        self.assertEqual(reverse("center_list"), "/center/list")

    def test_center_detail_url_is_correct(self):
        center_detail = reverse("center_detail", kwargs={"pk": UUID})
        result = f"/center/{UUID}/detail/"
        self.assertEqual(center_detail, result)

    def test_center_create_url_is_correct(self):
        self.assertEqual(reverse("center_create"), "/center/create/")

    def test_center_update_info_url_is_correct(self):
        center_update_info = reverse("center_update_info", kwargs={"pk": UUID})
        result = f"/center/{UUID}/update_info/"
        self.assertEqual(center_update_info, result)

    def test_center_update_others_url_is_correct(self):
        center_update_others = reverse(
            "center_update_others", kwargs={"pk": UUID}
        )
        result = f"/center/{UUID}/update_others/"
        self.assertEqual(center_update_others, result)

    def test_center_update_image_url_is_correct(self):
        center_update_image = reverse(
            "center_update_image", kwargs={"pk": UUID}
        )
        result = f"/center/{UUID}/update_image/"
        self.assertEqual(center_update_image, result)

    def test_center_delete_url_is_correct(self):
        center_delete = reverse("center_delete", kwargs={"pk": UUID})
        result = f"/center/{UUID}/delete/"
        self.assertEqual(center_delete, result)

    def test_center_reinsert_url_is_correct(self):
        center_reinsert = reverse("center_reinsert", kwargs={"pk": UUID})
        result = f"/center/{UUID}/reinsert/"
        self.assertEqual(center_reinsert, result)

    def test_center_add_responsible_url_is_correct(self):
        center_add_responsible = reverse(
            "center_add_responsible", kwargs={"pk": UUID}
        )
        result = f"/center/{UUID}/add_responsible/"
        self.assertEqual(center_add_responsible, result)

    def test_center_del_responsible_url_is_correct(self):
        center_del_responsible = reverse(
            "center_del_responsible", kwargs={"pk": 1}
        )
        result = "/center/1/del_responsible/"
        self.assertEqual(center_del_responsible, result)
