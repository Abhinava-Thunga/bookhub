package com.bookhub.bookstore.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private double totalPrice;

    @Column(nullable = false)
    private String userId; // 🔥 NEW

    public Order() {}

    public Long getId() {
        return id;
    }

    public double getTotalPrice() {
        return totalPrice;
    }

    public String getUserId() {   // 🔥 NEW
        return userId;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setTotalPrice(double totalPrice) {
        this.totalPrice = totalPrice;
    }

    public void setUserId(String userId) {   // 🔥 NEW
        this.userId = userId;
    }
}