from django import forms
from .models import User_Reg, Farmer_Reg, FarmHouse_Reg, Category, Product, delivery_agent, govt_policies \
    , tip_category, tips, rental_product, rental_category, rental_request


class User_RegForm(forms.ModelForm):
    Password = forms.CharField(widget=forms.PasswordInput, max_length=15, min_length=5)
    Address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    class Meta():
        model = User_Reg
        fields = ('First_Name','Last_Name','Email','Address','Phone_No','Password',)


class Farmer_RegForm(forms.ModelForm):
    Password = forms.CharField(widget=forms.PasswordInput, max_length=15, min_length=5)
    Address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    class Meta():
        model = Farmer_Reg
        fields = ('Farmer_Id','First_Name','Last_Name','Email','Address','Phone_No','Password','Id_Proof',)

class FarmHouse_RegForm(forms.ModelForm):
    Password = forms.CharField(widget=forms.PasswordInput, max_length=15, min_length=5)
    Address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    class Meta():
        model = FarmHouse_Reg
        fields = ('FarmHouse_Id','First_Name','Last_Name','Email','Address','Phone_No','Password','Id_Proof',)


class LoginForm(forms.ModelForm):
    Password = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=5)
    class Meta():
        model = User_Reg
        fields = ('Email','Password',)

class Add_CategoryForm(forms.ModelForm):
    class Meta():
        model = Category
        fields = ('Category_Name',)

class Edit_CategoryForm(forms.ModelForm):
    class Meta():
        model = Category
        fields = ('Category_Name',)

class Edit_UserProfile_Form(forms.ModelForm):
    Password = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=5)
    Address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta():
         model= User_Reg
         fields=('First_Name','Last_Name','Address','Phone_No','Password',)

class Edit_FarmerProfile_Form(forms.ModelForm):
    Password = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=5)
    Address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta():
         model= Farmer_Reg
         fields=('First_Name','Last_Name','Address','Phone_No','Password','Id_Proof')

class Edit_FarmHouseProfile_Form(forms.ModelForm):
    Password = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=5)
    Address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta():
         model= FarmHouse_Reg
         fields=('First_Name','Last_Name','Address','Phone_No','Password','Id_Proof')

class Add_ProductsForm(forms.ModelForm):
    Description=forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    class Meta():
         model= Product
         fields=('Categories','Name','Description','Price','Image')

class Edit_ProductsForm(forms.ModelForm):
    description=forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    class Meta():
        model = Product
        fields = ('Categories', 'Name', 'Description', 'Price', 'Image')

class Deliveryagentform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=5)
    class Meta():
         model= delivery_agent
         fields=('name','email','password',)

class edit_agentform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, max_length=12, min_length=5)

    class Meta():
        model = delivery_agent
        fields = ('name', 'email', 'password',)


class addDeliveryAgentForm(forms.ModelForm):
    class Meta():
        model = delivery_agent
        fields = ('name','email','id_proof')


class add_policyform(forms.ModelForm):
    caption=forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    lastdate=forms.DateField(widget=forms.DateInput(format=('%d-%m-%Y'), attrs={'type': 'date'}),)
    class Meta():

        model = govt_policies
        fields = ('caption','lastdate','image',)


class edit_policyform(forms.ModelForm):
    caption = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    lastdate = forms.DateField(widget=forms.DateInput(format=('%d-%m-%Y'), attrs={'type': 'date'}),)
    class Meta():
        model=govt_policies
        fields = ('caption','lastdate','image',)


class add_catform(forms.ModelForm):
    class Meta():
        model = tip_category
        fields = ('category',)

class edit_categoryForm(forms.ModelForm):
    class Meta():
        model = tip_category
        fields = ('category',)


class add_tipsform(forms.ModelForm):
    description=forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta():
         model= tips
         fields=('category','image','description',)

class edit_tipsform(forms.ModelForm):
    class Meta():
        model = tips
        fields=('category','image','description',)

class add_machineryform(forms.ModelForm):
    description=forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    class Meta():
         model= rental_product
         fields = ('categories', 'name', 'description', 'price', 'image')
class edit_machineryform(forms.ModelForm):
    description=forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    class Meta():
        model = rental_product
        fields = ('categories', 'name', 'description', 'price', 'image')
class add_machine_categoryform(forms.ModelForm):
    class Meta():
        model = rental_category
        fields = ('category_name',)

class edit_machine_categoryform(forms.ModelForm):
    class Meta():
        model = rental_category
        fields = ('category_name',)

class Request_form(forms.ModelForm):
    class Meta():
        model = rental_request
        fields = ('no_of_days',)

