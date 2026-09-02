from pathlib import Path

from django import forms

from catalog.models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


def words_validator(value):
    value_lower = value.casefold()

    for word in FORBIDDEN_WORDS:
        if word in value_lower:
            raise forms.ValidationError(
                f"Использование слова '{word}' запрещено."
            )


def price_validator(value):
    if value < 0:
        raise forms.ValidationError("Стоимость не может быть меньше 0.")

MAX_IMAGE_SIZE = 5 * 1024 * 1024

ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
}

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
}

def image_validator(value):

    if not value:
        return

    if value.size > MAX_IMAGE_SIZE:
        raise forms.ValidationError("Размер изображения не должен превышать 5 МБ.")

    extension = Path(value.name).suffix.lower()

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        raise forms.ValidationError("Изображение должно быть JPEG или PNG формата.")

    content_type = getattr(value, "content_type", None)

    if content_type and content_type not in ALLOWED_IMAGE_TYPES:
        raise forms.ValidationError("Содержимое изображения должно быть JPEG или PNG формата.")

class ProductForm(forms.ModelForm):

    def clean_name(self):
        name = self.cleaned_data["name"]
        words_validator(name)
        return name

    def clean_description(self):
        description = self.cleaned_data["description"]
        words_validator(description)
        return description

    def clean_price(self):
        price = self.cleaned_data["price"]
        price_validator(price)
        return price

    def clean_image(self):
        image = self.cleaned_data.get("image")
        image_validator(image)
        return image

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for filed in self.fields.values():
            filed.widget.attrs["class"] = "form-control"

        self.fields["category"].widget.attrs["class"] = "form-select"

        self.fields["name"].widget.attrs["placeholder"] = "Введите название продукта"

        self.fields["description"].widget.attrs.update(
            {
                "placeholder": "Введите описание продукта",
                "rows": 5,
            }
        )

        self.fields["price"].widget.attrs["placeholder"] = "Введите цену продукта"

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "image",
            "category",
            "price",
        ]
