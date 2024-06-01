from django.db import models

# Create your models here.

class User_Reg(models.Model):
    User_Id = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Address = models.TextField(max_length=200)
    Phone_No = models.CharField(max_length=50)
    State = models.CharField(max_length=100)
    District = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    Password = models.CharField(max_length=15)
    User_Type = models.IntegerField(default=2)



class Farmer_Reg(models.Model):
    Farmer_Id = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Address = models.TextField(max_length=200)
    Phone_No = models.CharField(max_length=50)
    State = models.CharField(max_length=100)
    District = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    Password = models.CharField(max_length=15)
    Id_Proof = models.ImageField(upload_to='Id_Proof/', null=True, blank=True)
    Status = models.BooleanField(default=False)
    User_Type = models.IntegerField(default=3)
    def __str__(self):
        return str(self.Farmer_Id)

class FarmHouse_Reg(models.Model):
    FarmHouse_Id = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Address = models.TextField(max_length=200)
    Phone_No = models.CharField(max_length=50)
    State = models.CharField(max_length=100)
    District = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    Password = models.CharField(max_length=15)
    Id_Proof = models.ImageField(upload_to='Id_Proof/', null=True, blank=True)
    Status = models.BooleanField(default=False)
    User_Type = models.IntegerField(default=4)
    def __str__(self):
        return str(self.FarmHouse_Id)


class Category(models.Model):
    Category_Id = models.AutoField(primary_key=True)
    Category_Name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.Category_Name)

class Product(models.Model):
    Product_Id = models.AutoField(primary_key=True)
    Categories = models.ForeignKey('Category',on_delete=models.CASCADE,to_field='Category_Id')
    Name = models.CharField(max_length=255)
    Description = models.TextField(blank=True)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Image = models.ImageField(upload_to='Product_Images/', blank=True, null=True)
    Farmer_Id = models.ForeignKey('Farmer_Reg',on_delete=models.CASCADE,to_field='Farmer_Id')

    def __str__(self):
        return str(self.Product_Id)

class cart(models.Model):
    cart_id=models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User_Reg',on_delete=models.CASCADE,to_field='User_Id')
    status=models.BooleanField(default=True)
    count=models.IntegerField(default=0)
    def __str__(self):
        return str(self.cart_id)

class cart_items(models.Model):
    item_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey('Product',on_delete=models.CASCADE,to_field='Product_Id')
    qty = models.IntegerField(default=1,choices=[(1,1),(2,2),(3,3),(4,4),(5,5)])
    carts_id = models.ForeignKey('cart',on_delete=models.CASCADE,to_field='cart_id')
    user_id = models.ForeignKey('User_Reg',on_delete=models.CASCADE,to_field='User_Id')
    farmers_id = models.ForeignKey('Farmer_Reg',on_delete=models.CASCADE,to_field='Farmer_Id')

class orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    cart_item_id = models.ForeignKey('cart_items',on_delete=models.CASCADE,to_field='item_id')
    user_id = models.ForeignKey('User_Reg', on_delete=models.CASCADE, to_field='User_Id')
    total_product_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date=models.DateField(auto_now_add=False,blank=True,null=True)
    pickup_date = models.DateField(auto_now_add=False)
    pickup_status = models.BooleanField(default=False)
    deliver_status = models.BooleanField(default=False)
    agents_id = models.ForeignKey('delivery_agent',on_delete=models.CASCADE,to_field='agent_id')


    def __str__(self):
        return str(self.order_id)

class delivery_agent(models.Model):
    agent_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    id_proof = models.ImageField(upload_to='agent_id/', blank=True, null=True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    usertype = models.IntegerField(default=5)
    available = models.BooleanField(default=True)

    def __str__(self):
        return str(self.agent_id)

class govt_policies(models.Model):
    policy_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User_Reg',on_delete=models.CASCADE,to_field='User_Id')
    caption = models.CharField(max_length=100)
    image = models.FileField(upload_to='Policies/', null=True, blank=True)
    uploaded_on=models.DateField(auto_now_add=True)
    lastdate=models.DateField(auto_now_add=False)

    def __str__(self):
        return str(self.policy_id)
class tip_category(models.Model):
    tip_cat_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category

class tips(models.Model):
    tip_id = models.AutoField(primary_key=True)
    category = models.ForeignKey('tip_category',on_delete=models.CASCADE,to_field='tip_cat_id')
    image = models.ImageField(upload_to='image/', null=True, blank=True)
    farmhouse = models.ForeignKey('FarmHouse_Reg', on_delete=models.CASCADE, to_field='FarmHouse_Id')
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.tip_id)

class rental_product(models.Model):
    machine_id = models.AutoField(primary_key=True)
    categories = models.ForeignKey('rental_category',on_delete=models.CASCADE,to_field='category_id')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='machinery_images/', blank=True, null=True)
    farmhouse_id = models.ForeignKey('FarmHouse_Reg',on_delete=models.CASCADE,to_field='FarmHouse_Id')

    def __str__(self):
        return str(self.machine_id)

class rental_category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name


class rental_request(models.Model):
    req_id = models.AutoField(primary_key=True)
    no_of_days= models.IntegerField()
    machine_id = models.ForeignKey('rental_product', on_delete=models.CASCADE, to_field='machine_id')
    farmer_id = models.ForeignKey('Farmer_Reg', on_delete=models.CASCADE, to_field='Farmer_Id')
    farmhouse_id = models.ForeignKey('FarmHouse_Reg', on_delete=models.CASCADE, to_field='FarmHouse_Id')
    requested_on = models.DateField(auto_now_add=True)
    req_status = models.BooleanField(default=True)
    rental_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.req_id)