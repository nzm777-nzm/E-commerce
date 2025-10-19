## 📖 Project Overview

**Simple Shoe E-Commerce** is a web application that allows users to browse, search, and buy shoes online.  
It features user authentication, a shopping cart system, payment gateway integration, and a Django admin dashboard for managing products and orders.  

This project demonstrates full-stack development using **Python (Django)** and **MySQL**, with a clean UI built using **HTML, CSS, and Bootstrap/TailwindCSS**.

---

## 🌟 Features

✅ User Registration, Login & Logout  
✅ Product Listing with Images, Brand, and Price  
✅ Add to Cart / Remove from Cart  
✅ Checkout and Order Summary  
✅ Razorpay Payment Gateway Integration 💳  
✅ Admin Dashboard for Product Management  
✅ Responsive UI for all devices  
✅ Search & Filter options for shoes  

---

## 🧰 Tech Stack

| Category | Technologies |
|-----------|--------------|
| **Frontend** | HTML, CSS, Bootstrap / TailwindCSS |
| **Backend** | Django (Python) |
| **Database** | MySQL |
| **Payment** | Razorpay API |
| **Version Control** | Git, GitHub |
| **IDE** | VS Code |

---

## ⚙️ Installation & Setup Guide

Follow the steps below to run this project locally 👇  

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/nzm777-nzm/simple-shoe-ecommerce.git
cd simple-shoe-ecommerce

2️⃣ Create a Virtual Environment

python -m venv env
env\Scripts\activate   # for Windows
# or
source env/bin/activate   # for Mac/Linux

3️⃣ Install Required Packages

pip install -r requirements.txt

4️⃣ Configure the Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shoe_ecommerce',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

5️⃣ Apply Migrations

python manage.py makemigrations
python manage.py migrate

6️⃣ Create Superuser (for admin access)
python manage.py createsuperuser

7️⃣ Run the Development Server
python manage.py runserver

Page

	
	
🚀 Future Enhancements

⭐ Product Review & Rating System

👤 User Profile & Order History

🎟️ Coupon & Discount Feature

🤖 AI-based Shoe Recommendations

🌐 React Frontend Integration

🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to fork the repo and submit a pull request 🚀


👨‍💻 Author

Nazeem PM

📍 Kerala, India

📧 nazeempm7@gmail.com

🌐 portfolio: https://nzm-portfolio.vercel.app/


🔗Linkedin:https://www.linkedin.com/in/nazeem-pm-a9423032a


💻 GitHub: http://github.com/nzm777-nzm





