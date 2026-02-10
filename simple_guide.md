# Simple Merchant Dashboard - Beginner's Guide
## Perfect for Your First Month Internship at PayU

---

## What You'll Build

A basic web app where you can:
- Add merchants
- View all merchants in a list
- Edit merchant info
- Delete merchants
- See transactions for each merchant

**No complicated stuff** - just pure Django basics! ✨

---

echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc



## Step 1: Setup (Day 1)

### Install Python and Create Project

```bash
# Check Python version (need 3.8+)
python --version

# Create project folder
mkdir merchant_dashboard
cd merchant_dashboard

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install Django
pip install django

# Create Django project
django-admin startproject myproject .

# Create app
python manage.py startapp merchants

# Run it to check everything works
python manage.py runserver
# Visit: http://127.0.0.1:8000
```

### Project Structure
```
merchant_dashboard/
├── myproject/          # Project settings
│   ├── settings.py
│   └── urls.py
├── merchants/          # Your app
│   ├── models.py       # Database tables
│   ├── views.py        # Logic
│   ├── urls.py         # Routes (you'll create this)
│   └── templates/      # HTML files (you'll create this)
├── manage.py
└── db.sqlite3         # Database (created later)
```

---

## Step 2: Configure Settings (Day 1)

Edit `myproject/settings.py`:

```python
# Find INSTALLED_APPS and add your app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'merchants',  # Add this line
]

# Scroll down and find TEMPLATES, add this to DIRS:
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Add this
        'APP_DIRS': True,
        # ... rest stays same
    },
]
```

---

## Step 3: Create Database Models (Day 2)

Edit `merchants/models.py`:

```python
from django.db import models

class Merchant(models.Model):
    """Merchant information"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    
    business_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.business_name
    
    class Meta:
        ordering = ['-created_at']


class Transaction(models.Model):
    """Transaction records"""
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]
    
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='transactions')
    transaction_id = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.transaction_id} - ₹{self.amount}"
    
    class Meta:
        ordering = ['-created_at']
```

### Create Database

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations (creates tables)
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Enter username, email, password
```

---

## Step 4: Register Models in Admin (Day 2)

Edit `merchants/admin.py`:

```python
from django.contrib import admin
from .models import Merchant, Transaction

@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'email', 'phone', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['business_name', 'email']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'merchant', 'amount', 'status', 'created_at']
    list_filter = ['status']
```

**Test it**: Run `python manage.py runserver` and visit http://127.0.0.1:8000/admin

---

## Step 5: Create Forms (Day 3)

Create `merchants/forms.py`:

```python
from django import forms
from .models import Merchant

class MerchantForm(forms.ModelForm):
    class Meta:
        model = Merchant
        fields = ['business_name', 'contact_person', 'email', 'phone', 'status']
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '10'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

from .models import Transaction

from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'amount', 'status']
        widgets = {
            'transaction_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. TXN12345'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
```

---

## Step 6: Create Views (Day 3-4)

Edit `merchants/views.py`:

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Merchant, Transaction
from .forms import MerchantForm

@login_required
def merchant_list(request):
    """Show all merchants"""
    merchants = Merchant.objects.all()
    return render(request, 'merchants/merchant_list.html', {'merchants': merchants})

@login_required
def merchant_create(request):
    """Add new merchant"""
    if request.method == 'POST':
        form = MerchantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('merchant_list')
    else:
        form = MerchantForm()
    return render(request, 'merchants/merchant_form.html', {'form': form, 'title': 'Add Merchant'})

@login_required
def merchant_detail(request, pk):
    """View merchant and their transactions"""
    merchant = get_object_or_404(Merchant, pk=pk)
    transactions = merchant.transactions.all()
    return render(request, 'merchants/merchant_detail.html', {
        'merchant': merchant,
        'transactions': transactions
    })

@login_required
def merchant_update(request, pk):
    """Edit merchant"""
    merchant = get_object_or_404(Merchant, pk=pk)
    if request.method == 'POST':
        form = MerchantForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            return redirect('merchant_detail', pk=pk)
    else:
        form = MerchantForm(instance=merchant)
    return render(request, 'merchants/merchant_form.html', {
        'form': form,
        'title': 'Edit Merchant',
        'merchant': merchant
    })

@login_required
def merchant_delete(request, pk):
    """Delete merchant"""
    merchant = get_object_or_404(Merchant, pk=pk)
    if request.method == 'POST':
        merchant.delete()
        return redirect('merchant_list')
    return render(request, 'merchants/merchant_confirm_delete.html', {'merchant': merchant})
@login_required
def transaction_create(request, pk):
    # Fetch the specific merchant using the ID from the URL
    merchant = get_object_or_404(Merchant, pk=pk)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            # commit=False creates the object but doesn't save to DB yet
            transaction = form.save(commit=False)
            # Manually link the transaction to our merchant
            transaction.merchant = merchant
            transaction.save() # Now save it to the database
            return redirect('merchant_detail', pk=pk)
    else:
        form = TransactionForm()
        
    return render(request, 'merchants/transaction_form.html', {
        'form': form, 
        'merchant': merchant
    })
```

---

## Step 7: Setup URLs (Day 4)

Create `merchants/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.merchant_list, name='merchant_list'),
    path('add/', views.merchant_create, name='merchant_create'),
    path('<int:pk>/', views.merchant_detail, name='merchant_detail'),
    path('<int:pk>/edit/', views.merchant_update, name='merchant_update'),
    path('<int:pk>/delete/', views.merchant_delete, name='merchant_delete'),
    path('<int:pk>/add-transaction/', views.add_transaction, name='add_transaction'),
]
```

Edit `myproject/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('merchants/', include('merchants.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # For login/logout
    path('', lambda request: redirect('merchant_list')),  # Redirect home to merchant list
]
```

---

## Step 8: Create Templates (Day 5-7)

### Create folder structure:
```bash
mkdir -p merchants/templates/merchants
mkdir -p templates/registration
```

### Base Template

Create `merchants/templates/base.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Merchant Dashboard{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'merchant_list' %}">
                <i class="bi bi-shop"></i> Merchant Dashboard
            </a>
            {% if user.is_authenticated %}
            <div class="d-flex">
                <span class="navbar-text text-white me-3">
                    Hello, {{ user.username }}
                </span>
                <a href="{% url 'logout' %}" class="btn btn-outline-light btn-sm">Logout</a>
            </div>
            {% endif %}
        </div>
    </nav>

    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### Login Template

Create `templates/registration/login.html`:

```html
{% extends 'base.html' %}

{% block title %}Login{% endblock %}

{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-4">
        <div class="card shadow">
            <div class="card-body">
                <h3 class="text-center mb-4">Login</h3>
                <form method="post">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label class="form-label">Username</label>
                        <input type="text" name="username" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" name="password" class="form-control" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Login</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Merchant List Template

Create `merchants/templates/merchants/merchant_list.html`:

```html
{% extends 'base.html' %}

{% block title %}Merchants{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2><i class="bi bi-people"></i> Merchants</h2>
    <a href="{% url 'merchant_create' %}" class="btn btn-primary">
        <i class="bi bi-plus-circle"></i> Add Merchant
    </a>
</div>

<div class="card shadow-sm">
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-hover">
                <thead class="table-light">
                    <tr>
                        <th>Business Name</th>
                        <th>Contact Person</th>
                        <th>Email</th>
                        <th>Phone</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for merchant in merchants %}
                    <tr>
                        <td><strong>{{ merchant.business_name }}</strong></td>
                        <td>{{ merchant.contact_person }}</td>
                        <td>{{ merchant.email }}</td>
                        <td>{{ merchant.phone }}</td>
                        <td>
                            {% if merchant.status == 'active' %}
                                <span class="badge bg-success">Active</span>
                            {% else %}
                                <span class="badge bg-secondary">Inactive</span>
                            {% endif %}
                        </td>
                        <td>
                            <a href="{% url 'merchant_detail' merchant.pk %}" class="btn btn-sm btn-info">
                                <i class="bi bi-eye"></i> View
                            </a>
                            <a href="{% url 'merchant_update' merchant.pk %}" class="btn btn-sm btn-warning">
                                <i class="bi bi-pencil"></i> Edit
                            </a>
                            <a href="{% url 'merchant_delete' merchant.pk %}" class="btn btn-sm btn-danger">
                                <i class="bi bi-trash"></i> Delete
                            </a>
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="6" class="text-center py-4">
                            No merchants found. <a href="{% url 'merchant_create' %}">Add your first merchant</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
```

### Merchant Form Template

Create `merchants/templates/merchants/merchant_form.html`:

```html
{% extends 'base.html' %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card shadow-sm">
            <div class="card-header bg-primary text-white">
                <h4 class="mb-0">{{ title }}</h4>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    
                    <div class="mb-3">
                        <label class="form-label">Business Name *</label>
                        {{ form.business_name }}
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Contact Person *</label>
                        {{ form.contact_person }}
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Email *</label>
                        {{ form.email }}
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Phone (10 digits) *</label>
                        {{ form.phone }}
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">Status</label>
                        {{ form.status }}
                    </div>
                    
                    <div class="d-flex gap-2">
                        <button type="submit" class="btn btn-success">
                            <i class="bi bi-check-circle"></i> Save
                        </button>
                        <a href="{% url 'merchant_list' %}" class="btn btn-secondary">
                            <i class="bi bi-x-circle"></i> Cancel
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Merchant Detail Template

Create `merchants/templates/merchants/merchant_detail.html`:

```html
{% extends 'base.html' %}

{% block title %}{{ merchant.business_name }}{% endblock %}

{% block content %}
<div class="mb-3">
    <a href="{% url 'merchant_list' %}" class="btn btn-sm btn-secondary">
        <i class="bi bi-arrow-left"></i> Back to List
    </a>
</div>

<div class="row">
    <div class="col-md-4">
        <div class="card shadow-sm mb-4">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0"><i class="bi bi-building"></i> Merchant Details</h5>
            </div>
            <div class="card-body">
                <table class="table table-sm">
                    <tr>
                        <th>Business Name:</th>
                        <td>{{ merchant.business_name }}</td>
                    </tr>
                    <tr>
                        <th>Contact Person:</th>
                        <td>{{ merchant.contact_person }}</td>
                    </tr>
                    <tr>
                        <th>Email:</th>
                        <td>{{ merchant.email }}</td>
                    </tr>
                    <tr>
                        <th>Phone:</th>
                        <td>{{ merchant.phone }}</td>
                    </tr>
                    <tr>
                        <th>Status:</th>
                        <td>
                            {% if merchant.status == 'active' %}
                                <span class="badge bg-success">Active</span>
                            {% else %}
                                <span class="badge bg-secondary">Inactive</span>
                            {% endif %}
                        </td>
                    </tr>
                    <tr>
                        <th>Created:</th>
                        <td>{{ merchant.created_at|date:"M d, Y" }}</td>
                    </tr>
                </table>
                <div class="d-flex gap-2">
                    <a href="{% url 'merchant_update' merchant.pk %}" class="btn btn-sm btn-warning">
                        <i class="bi bi-pencil"></i> Edit
                    </a>
                    <a href="{% url 'merchant_delete' merchant.pk %}" class="btn btn-sm btn-danger">
                        <i class="bi bi-trash"></i> Delete
                    </a>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-8">
        <div class="card shadow-sm">
            <div class="card-header bg-info text-white">
                <h5 class="mb-0"><i class="bi bi-receipt"></i> Transactions</h5>
                    <a href="{% url 'add_transaction' merchant.pk %}" class="btn btn-sm btn-success">
    + Add New Transaction
</a>
            </div>
            <div class="card-body">
                {% if transactions %}
                <div class="table-responsive">
                    <table class="table table-sm table-hover">
                        <thead class="table-light">
                            <tr>
                                <th>Transaction ID</th>
                                <th>Amount</th>
                                <th>Status</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for txn in transactions %}
                            <tr>
                                <td><code>{{ txn.transaction_id }}</code></td>
                                <td><strong>₹{{ txn.amount }}</strong></td>
                                <td>
                                    {% if txn.status == 'success' %}
                                        <span class="badge bg-success">Success</span>
                                    {% elif txn.status == 'pending' %}
                                        <span class="badge bg-warning">Pending</span>
                                    {% else %}
                                        <span class="badge bg-danger">Failed</span>
                                    {% endif %}
                                </td>
                                <td>{{ txn.created_at|date:"M d, Y H:i" }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                {% else %}
                <p class="text-muted text-center py-4">No transactions yet</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Delete Confirmation Template

Create `merchants/templates/merchants/merchant_confirm_delete.html`:

```html
{% extends 'base.html' %}

{% block title %}Delete Merchant{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-5">
        <div class="card shadow-sm">
            <div class="card-header bg-danger text-white">
                <h5 class="mb-0"><i class="bi bi-exclamation-triangle"></i> Confirm Delete</h5>
            </div>
            <div class="card-body">
                <p>Are you sure you want to delete <strong>{{ merchant.business_name }}</strong>?</p>
                <p class="text-danger">This action cannot be undone!</p>
                
                <form method="post">
                    {% csrf_token %}
                    <div class="d-flex gap-2">
                        <button type="submit" class="btn btn-danger">
                            <i class="bi bi-trash"></i> Yes, Delete
                        </button>
                        <a href="{% url 'merchant_detail' merchant.pk %}" class="btn btn-secondary">
                            <i class="bi bi-x-circle"></i> Cancel
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```
``` html
{% extends 'base.html' %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card shadow">
            <div class="card-header bg-success text-white">
                <h4>Add Transaction for {{ merchant.business_name }}</h4>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <div class="mt-3">
                        <button type="submit" class="btn btn-primary">Save Transaction</button>
                        <a href="{% url 'merchant_detail' merchant.pk %}" class="btn btn-secondary">Cancel</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}

---
# UPDATE TRANSACTION
@login_required
def transaction_update(request, pk):
    # Fetch the transaction by its primary key
    transaction = get_object_or_404(Transaction, pk=pk)
    # We need the merchant's ID to redirect back to their page later
    merchant_id = transaction.merchant.id 

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('merchant_detail', pk=merchant_id)
    else:
        form = TransactionForm(instance=transaction)
    
    return render(request, 'merchants/transaction_form.html', {
        'form': form, 
        'title': 'Edit Transaction',
        'merchant': transaction.merchant
    })

# DELETE TRANSACTION
@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    merchant_id = transaction.merchant.id
    
    if request.method == 'POST':
        transaction.delete()
        return redirect('merchant_detail', pk=merchant_id)
    
    return render(request, 'merchants/transaction_confirm_delete.html', {'transaction': transaction})


-----
{% extends 'base.html' %}

{% block content %}
<div class="card shadow-sm border-danger">
    <div class="card-body">
        <h3>Delete Transaction?</h3>
        <p>Are you sure you want to delete transaction <strong>{{ transaction.transaction_id }}</strong> 
           amounting to <strong>₹{{ transaction.amount }}</strong>?</p>
        <form method="post">
            {% csrf_token %}
            <button type="submit" class="btn btn-danger">Confirm Delete</button>
            <a href="{% url 'merchant_detail' transaction.merchant.id %}" class="btn btn-secondary">Cancel</a>
        </form>
    </div>
</div>
{% endblock %}

-----

<tbody>
    {% for txn in transactions %}
    <tr>
        <td><code>{{ txn.transaction_id }}</code></td>
        <td><strong>₹{{ txn.amount }}</strong></td>
        <td>...status badge...</td>
        <td>
            <a href="{% url 'transaction_update' txn.pk %}" class="btn btn-sm btn-outline-warning">
                <i class="bi bi-pencil"></i>
            </a>
            <a href="{% url 'transaction_delete' txn.pk %}" class="btn btn-sm btn-outline-danger">
                <i class="bi bi-trash"></i>
            </a>
        </td>
    </tr>
    {% endfor %}
</tbody>


path('transaction/<int:pk>/edit/', views.transaction_update, name='transaction_update'),
path('transaction/<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),


```
---

## Step 9: Configure Login Settings (Day 7)

Edit `myproject/settings.py` - add at the bottom:

```python
# Login settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'merchant_list'
LOGOUT_REDIRECT_URL = 'login'
```

---

```python
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'amount', 'status'] # We skip 'merchant' because we'll auto-assign it
        widgets = {
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(choices=Transaction.STATUS_CHOICES, attrs={'class': 'form-select'}),
        }
```
---

## Step 10: Add Sample Data (Day 7)

Create some test data using Django shell:

```bash
python manage.py shell
```

```python
from merchant.models import Merchant, Transaction
from decimal import Decimal

# Create merchants
m1 = Merchant.objects.create(
    business_name="TechStore India",
    contact_person="Rahul Kumar",
    email="rahul@techstore.com",
    phone="9876543210",
    status="active"
)

m2 = Merchant.objects.create(
    business_name="FoodieDelight",
    contact_person="Priya Sharma",
    email="priya@foodie.com",
    phone="9876543211",
    status="active"
)

# Create transactions
Transaction.objects.create(
    merchant=m1,
    transaction_id="TXN001",
    amount=Decimal("5000.00"),
    status="success"
)

Transaction.objects.create(
    merchant=m1,
    transaction_id="TXN002",
    amount=Decimal("3000.00"),
    status="pending"
)

Transaction.objects.create(
    merchant=m2,
    transaction_id="TXN003",
    amount=Decimal("1500.00"),
    status="success"
)

print("Sample data created!")
exit()
```

---

## Step 11: Run and Test! (Day 7)

```bash
# Start server
python manage.py runserver

# Visit in browser:
# http://127.0.0.1:8000
# Login with your superuser credentials
```

---

## Complete File Structure

```
merchant_dashboard/
├── myproject/
│   ├── __init__.py
│   ├── settings.py          ✅ Modified
│   ├── urls.py              ✅ Modified
│   └── wsgi.py
├── merchants/
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html                           ✅ Created
│   │   └── merchants/
│   │       ├── merchant_list.html              ✅ Created
│   │       ├── merchant_form.html              ✅ Created
│   │       ├── merchant_detail.html            ✅ Created
│   │       └── merchant_confirm_delete.html    ✅ Created
│   ├── __init__.py
│   ├── admin.py            ✅ Modified
│   ├── models.py           ✅ Modified
│   ├── views.py            ✅ Modified
│   ├── urls.py             ✅ Created
│   └── forms.py            ✅ Created
├── templates/
│   └── registration/
│       └── login.html      ✅ Created
├── manage.py
└── db.sqlite3              ✅ Created after migrations
```

---

## Testing Checklist

✅ Can login with superuser  
✅ Can see merchant list  
✅ Can add new merchant  
✅ Can view merchant details  
✅ Can edit merchant  
✅ Can delete merchant  
✅ Can see transactions for each merchant  
✅ Logout works  

---

## Common Errors & Solutions

### Error: "TemplateDoesNotExist"
**Solution**: Check template paths and folder names match exactly

### Error: "NoReverseMatch"
**Solution**: Check URL names in urls.py match the ones used in templates

### Error: "Merchant matching query does not exist"
**Solution**: Make sure you created sample data

### Error: Can't login
**Solution**: Did you create a superuser? Run `python manage.py createsuperuser`

---

## What to Show Your Manager

1. **Demo the working app** - Show CRUD operations
2. **Explain the code** - Walk through models, views, templates
3. **Discuss what you learned**:
   - Django MVT pattern
   - Database relationships (ForeignKey)
   - Forms and validation
   - Template inheritance
   - URL routing

---

## Week-by-Week Plan

### Week 1: Setup & Models
- Day 1-2: Setup project, create models
- Day 3: Django admin, add sample data
- Day 4-5: Learn Django basics (tutorial)

### Week 2: Views & URLs
- Day 1-2: Create views
- Day 3-4: Setup URLs
- Day 5: Test everything

### Week 3: Templates
- Day 1-2: Base template & login
- Day 3-4: List and form templates
- Day 5: Detail and delete templates

### Week 4: Polish & Present
- Day 1-2: Add styling, fix bugs
- Day 3-4: Add more sample data, test
- Day 5: Prepare demo, documentation

---

## Next Steps After This Project

Once you're comfortable with this:
1. Add search functionality
2. Add pagination
3. Add transaction creation form
4. Add filters (by status, date)
5. Export to CSV

---

**You've got this! 🚀**

Start with Step 1 and go one step at a time. Don't rush - understanding is more important than speed. Good luck with your internship!
