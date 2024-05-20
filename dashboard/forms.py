from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, HTML, Submit, ButtonHolder
from django import forms
from user.models import User
from product.models import Product, ProductImage, ProductDetail, Brand, Category
from django.contrib.auth.hashers import make_password


class CreateUserForm(forms.ModelForm):
    firstName = forms.CharField(required=True)
    lastName = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "firstName",
            "lastName",
            "phone",
            "password",
            "address",
            "is_active",
            "is_staff",
            "is_superuser",
        ]
        widgets = {
            "password": forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML("<div class='row'>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("firstName", css_class="input-xlarge", attrs={"required": True}),
            HTML("</div>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("lastName", css_class="input-xlarge", attrs={"required": True}),
            HTML("</div>"),
            HTML("</div>"),
            # --*--
            HTML("<div class='row'>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("username", css_class="input-xlarge", attrs={"required": True}),
            HTML("</div>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("password", css_class="input-xlarge", attrs={"required": True}),
            HTML("</div>"),
            HTML("</div>"),
            # --*--
            HTML("<div class='row'>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("email", css_class="input-xlarge", attrs={"required": True}),
            HTML("</div>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("phone", css_class="input-xlarge", attrs={"required": True}),
            HTML("</div>"),
            HTML("</div>"),
            # --*--
            Field("address", css_class="input-xlarge"),
            Field("is_active", css_class="form-check-inline"),
            # --*--
            HTML("<div class='row'>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("is_staff", css_class="form-check-inline"),
            HTML("</div>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("is_superuser", css_class="form-check-inline"),
            HTML("</div>"),
            HTML("</div>"),
            ButtonHolder(
                Submit("create", "Tạo", css_class="button white w-100"),
            ),
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        data = self.cleaned_data
        fields = [
            "password",
            "username",
            "email",
            "firstName",
            "lastName",
            "phone",
            "address",
            "is_staff",
            "is_superuser",
            "is_active",
        ]

        for field in fields:
            setattr(user, field, data.get(field))

        if commit:
            user = User.objects.create_user(
                username=user.username,
                email=user.email,
                password=user.password,
                firstName=user.firstName,
                lastName=user.lastName,
                phone=user.phone,
                address=user.address,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                is_staff=user.is_staff,
            )
        return user


class EditUserForm(forms.ModelForm):
    firstName = forms.CharField(required=True)
    lastName = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "firstName",
            "lastName",
            "phone",
            "password",
            "address",
            "is_active",
            "is_staff",
            "is_superuser",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].disabled = True

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML("<div class='row'>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("firstName", css_class="input-xlarge", attrs={"required": True}),
            HTML("</div>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("lastName", css_class="input-xlarge", attrs={"required": True}),
            HTML("</div>"),
            HTML("</div>"),
            # --*--
            HTML("<div class='row'>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("username", css_class="input-xlarge", attrs={"required": True}),
            HTML("</div>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("password", css_class="input-xlarge", attrs={"required": True}),
            HTML("</div>"),
            HTML("</div>"),
            # --*--
            HTML("<div class='row'>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("email", css_class="input-xlarge", attrs={"required": True}),
            HTML("</div>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("phone", css_class="input-xlarge", attrs={"required": True}),
            HTML("</div>"),
            HTML("</div>"),
            # --*--
            Field("address", css_class="input-xlarge"),
            Field("is_active", css_class="form-check-inline"),
            # --*--
            HTML("<div class='row'>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("is_staff", css_class="form-check-inline"),
            HTML("</div>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("is_superuser", css_class="form-check-inline"),
            HTML("</div>"),
            HTML("</div>"),
            ButtonHolder(
                Submit("edit", "Chỉnh sửa", css_class="button white w-100"),
            ),
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.password = make_password(password, hasher="pbkdf2_sha256")
        if commit:
            user.save()
        return user


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'brand', 'categories', 'description', 'price', 'discount_price','slug','total_quantity']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),  # Better display for description
        }

    slug = forms.CharField(widget=forms.HiddenInput())
    total_quantity = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if not slug:  # Handle empty slug (likely on initial form display)
            slug = self.instance.slug if self.instance else None  # Get from existing object or default
        return slug

    def save(self, commit=True):
        product = super().save(commit=False)  # Don't save immediately

        # Calculate total quantity if details are provided
        total_quantity = 0
        for size, quantity in zip(self.data.getlist('sizes'), self.data.getlist('quantities')):
            if size and quantity:
                total_quantity += int(quantity)
        product.total_quantity = total_quantity

        if commit:
            product.save()
            self.save_m2m()  # Save ManyToManyField (categories)
        return product

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

class ProductDetailForm(forms.ModelForm):
    class Meta:
        model = ProductDetail
        fields = ['size', 'quantity']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']