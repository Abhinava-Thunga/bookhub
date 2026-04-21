package com.bookhub.bookstore.service;

import com.bookhub.bookstore.entity.Book;
import com.bookhub.bookstore.entity.CartItem;
import com.bookhub.bookstore.entity.Order;
import com.bookhub.bookstore.repository.BookRepository;
import com.bookhub.bookstore.repository.CartRepository;
import com.bookhub.bookstore.repository.OrderRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class OrderService {

    private final CartRepository cartRepo;
    private final BookRepository bookRepo;
    private final OrderRepository orderRepo;

    public OrderService(CartRepository cartRepo, BookRepository bookRepo, OrderRepository orderRepo) {
        this.cartRepo = cartRepo;
        this.bookRepo = bookRepo;
        this.orderRepo = orderRepo;
    }

    public Order placeOrder() {

        List<CartItem> cartItems = cartRepo.findAll();

        if (cartItems.isEmpty()) {
            throw new RuntimeException("Cart is empty");
        }

        double total = 0;

        // 🔥 VALIDATION + CALCULATION
        for (CartItem item : cartItems) {

            Book book = item.getBook();

            if (item.getQuantity() > book.getQuantity()) {
                throw new RuntimeException("Stock not available for " + book.getTitle());
            }

            total += item.getQuantity() * book.getPrice();
        }

        // 🔥 UPDATE STOCK
        for (CartItem item : cartItems) {

            Book book = item.getBook();

            int newQty = book.getQuantity() - item.getQuantity();
            book.setQuantity(newQty);

            bookRepo.save(book);
        }

        // 🔥 CLEAR CART FIRST (VERY IMPORTANT)
        cartRepo.deleteAll();

        // 🔥 OPTIONAL: DELETE BOOKS WITH 0 STOCK (SAFE NOW)
        List<Book> books = bookRepo.findAll();
        for (Book book : books) {
            if (book.getQuantity() == 0) {
                bookRepo.delete(book); // ✅ SAFE (cart already cleared)
            }
        }

        // 🔥 SAVE ORDER
        Order order = new Order();
        order.setTotalPrice(total);

        return orderRepo.save(order);
    }
}