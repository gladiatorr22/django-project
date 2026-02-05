# Simplified Product Requirements Document
## Basic Merchant Dashboard - Internship Project (Month 1)

---

## 1. Project Overview

A simple internal dashboard for PayU to manage merchant profiles and view their basic transaction records. This is a **learning project** focused on understanding Django fundamentals.

**Timeline**: 1 Month (Internship Project)  
**Complexity**: Beginner-friendly CRUD application

---

## 2. Core Features (MVP)

### 2.1 What You'll Build

1. **Merchant Management (CRUD)**
   - Add new merchant
   - View all merchants in a table
   - Edit merchant details
   - Delete merchant

2. **Transaction Records (Read-Only)**
   - View transactions for each merchant
   - Simple filtering by status

3. **Basic Admin Login**
   - Simple username/password login
   - Only admins can access (no merchant login needed)

---

## 3. Simplified Requirements

### Feature 1: Merchant List Page
- Show all merchants in a table
- Columns: Business Name, Email, Phone, Status, Actions
- "Add New Merchant" button at top
- Edit and Delete buttons for each merchant

### Feature 2: Add/Edit Merchant Form
- Business Name (required)
- Contact Person Name (required)
- Email (required)
- Phone Number (10 digits)
- Status: Active/Inactive dropdown
- Save button

### Feature 3: View Merchant Transactions
- Click on merchant to see their transactions
- Show: Transaction ID, Amount, Date, Status
- Simple table, no fancy filters needed

---

## 4. Data Models (Simple)

### Merchant Model
```
- business_name
- contact_person
- email
- phone
- status (Active/Inactive)
- created_at (auto)
```

### Transaction Model
```
- merchant (linked to Merchant)
- transaction_id (auto-generated)
- amount
- status (Success/Failed/Pending)
- created_at (auto)
```

---

## 5. Pages You Need

1. **Login Page** - Simple login form
2. **Merchant List** - Table with all merchants
3. **Add Merchant** - Form to create new merchant
4. **Edit Merchant** - Form to update merchant
5. **View Merchant** - Show merchant details + their transactions

---

## 6. What's NOT Included (Keep It Simple!)

❌ No user groups/permissions (only admin exists)  
❌ No payment method toggles  
❌ No bank account management  
❌ No complex dashboards with charts  
❌ No merchant login (admin only)  
❌ No filters/search (optional if time permits)  
❌ No API endpoints  

---

## 7. Tech Stack (Minimal)

- **Backend**: Django 4.2
- **Database**: SQLite (default)
- **Frontend**: Django Templates + Bootstrap 5 (CDN)
- **No extra packages** needed initially

---

## 8. Success Criteria

✅ Can add, view, edit, and delete merchants  
✅ Can see transactions for each merchant  
✅ Basic styling with Bootstrap  
✅ Admin can login/logout  
✅ Code is clean and well-commented  

---

## 9. Learning Outcomes

By the end of this project, you'll understand:
- Django MVT (Model-View-Template) architecture
- Django ORM (database operations)
- Django Forms
- Template inheritance
- URL routing
- Basic authentication

---

**Perfect for**: First month internship, Learning Django basics  
**Time Required**: 2-3 weeks (with learning time)  
**Difficulty**: ⭐⭐☆☆☆ (Beginner)
