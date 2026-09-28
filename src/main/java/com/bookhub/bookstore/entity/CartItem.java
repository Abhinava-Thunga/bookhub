package com.bookhub.bookstore.entity;

import jakarta.persistence.*;

@Entity
public class CartItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private int quantity;

    @ManyToOne
    @JoinColumn(name = "book_id")
    private Book book;

    public CartItem() {}

    public Long getId() {
        return id;
    }

    public int getQuantity() {
        return quantity;
    }

    public Book getBook() {
        return book;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setQuantity(int quantity) {
        this.quantity = quantity;
    }

    public void setBook(Book book) {
        this.book = book;
    }
}
