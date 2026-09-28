package com.bookhub.bookstore.service;

import com.bookhub.bookstore.entity.Book;
import com.bookhub.bookstore.entity.CartItem;
import com.bookhub.bookstore.repository.BookRepository;
import com.bookhub.bookstore.repository.CartRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CartService {

    private final CartRepository cartRepo;
    private final BookRepository bookRepo;

    public CartService(CartRepository cartRepo, BookRepository bookRepo) {
        this.cartRepo = cartRepo;
        this.bookRepo = bookRepo;
    }

    public CartItem addToCart(Long id, int qty) {

        Book book = bookRepo.findById(id)
                .orElseThrow(() -> new RuntimeException("Book not found"));

        if (qty > book.getQuantity()) {
            throw new RuntimeException("Stock not available");
        }

        CartItem item = new CartItem();
        item.setBook(book);
        item.setQuantity(qty);

        return cartRepo.save(item);
    }

    public List<CartItem> getCart() {
        return cartRepo.findAll();
    }

    public void clearCart() {
        cartRepo.deleteAll();
    }
}
