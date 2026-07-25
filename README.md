# 📚 BookHub - Online Book Store System

BookHub is a full-stack online bookstore web application developed using **Java Spring Boot**, **MySQL**, **HTML**, **CSS**, and **JavaScript**. It allows users to browse books, manage their cart, place orders, and view order history, while administrators can manage books and inventory through an admin dashboard.

## 🚀 Features

### 👤 User Features
- Browse available books
- View book details (title, author, price, stock, image)
- Add books to cart
- Update quantities
- Place orders
- Automatic stock validation
- View order history

### 🛠️ Admin Features
- Add new books
- Delete books
- Manage inventory
- Upload book images (URL or device)
- Automatic removal of books when stock reaches zero

## ⚙️ Tech Stack

### Backend
- Java 21
- Spring Boot
- Spring Data JPA
- Hibernate

### Frontend
- HTML5
- CSS3
- JavaScript
- Fetch API

### Database
- MySQL

### Tools
- IntelliJ IDEA
- Maven
- Postman
- VS Code

## 📂 Project Structure

```
BookHub
│
├── backend
│   ├── Controller
│   ├── Service
│   ├── Repository
│   ├── Model
│   └── DTO
│
├── frontend
│   ├── index.html
│   ├── admin.html
│   ├── css
│   ├── js
│   └── images
│
└── database
    └── MySQL
```

## 📌 Modules

- Book Management
- Cart Management
- Order Processing
- Order History
- Admin Dashboard

## 🔥 Key Functionalities

- RESTful APIs using Spring Boot
- CRUD Operations
- Real-time Stock Validation
- Automatic Stock Reduction
- Responsive User Interface
- Image Upload Support
- Order History Tracking

## 🖥️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/bookhub.git
cd bookhub
```

### Backend

1. Configure MySQL database.
2. Update `application.properties`.

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/bookhub
spring.datasource.username=root
spring.datasource.password=your_password
```

3. Run the application.

```bash
mvn spring-boot:run
```

### Frontend

Open `index.html` in your browser or serve using Live Server.

## 📷 Screenshots

- Home Page
- Shopping Cart
- Order History
- Admin Dashboard

(Add screenshots here)

## 📈 Future Enhancements

- User Authentication (Login/Register)
- Payment Gateway Integration
- Book Search & Filters
- Wishlist
- Recommendation System
- Email Notifications
- Cloud Deployment
- React-based Frontend
- Mobile Application

## 👨‍💻 Authors

- Abhinava Thunga K N
- Swastik Vinayak Hegde
- Nagaraj Shripad Bhat

## 🎓 Academic Project

Mini Project submitted to:

**Presidency University**  
Department of Information Science & Engineering

---

⭐ If you like this project, don't forget to give it a star!
