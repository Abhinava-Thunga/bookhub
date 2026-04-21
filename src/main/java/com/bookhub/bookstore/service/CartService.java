package com.bookhub.bookstore.service;

import com.bookhub.bookstore.entity.Book;
import com.bookhub.bookstore.entity.CartItem;
import com.bookhub.bookstore.repository.BookRepository;
import com.bookhub.bookstore.repository.CartRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class CartService {

    private final CartRepository cartRepo;
    private final BookRepository bookRepo;

    public CartService(CartRepository cartRepo, BookRepository bookRepo) {
        this.cartRepo = cartRepo;
        this.bookRepo = bookRepo;
    }

    public CartItem addToCart(Long bookId, int qty) {

        Book book = bookRepo.findById(bookId)
                .orElseThrow(() -> new RuntimeException("Book not found"));

        if (book.getQuantity() <= 0) {
            throw new RuntimeException("Book out of stock");
        }

        if (qty > book.getQuantity()) {
            throw new RuntimeException("Stock not available");
        }

        // 🔥 CHECK IF ITEM ALREADY EXISTS
        List<CartItem> items = cartRepo.findAll();

        for (CartItem item : items) {
            if (item.getBook().getId().equals(bookId)) {

                int newQty = item.getQuantity() + qty;

                if (newQty > book.getQuantity()) {
                    throw new RuntimeException("Stock not available");
                }

                item.setQuantity(newQty);
                return cartRepo.save(item);
            }
        }

        // ✅ CREATE NEW IF NOT EXISTS
        CartItem newItem = new CartItem();
        newItem.setBook(book); // ✅ CORRECT (managed entity)
        newItem.setQuantity(qty);

        return cartRepo.save(newItem);
    }

    public List<CartItem> getCart() {
        return cartRepo.findAll();
    }

    public void clearCart() {
        cartRepo.deleteAll();
    }
}