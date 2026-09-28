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

    public Order placeOrder(String userId) {

        List<CartItem> items = cartRepo.findAll();

        if (items.isEmpty()) {
            throw new RuntimeException("Cart is empty");
        }

        double total = 0;

        for (CartItem item : items) {

            Book book = item.getBook();

            if (item.getQuantity() > book.getQuantity()) {
                throw new RuntimeException("Stock not available");
            }

            total += item.getQuantity() * book.getPrice();

            book.setQuantity(book.getQuantity() - item.getQuantity());
            bookRepo.save(book);
        }

        cartRepo.deleteAll();

        Order order = new Order();
        order.setTotalPrice(total);
        order.setUserId(userId);

        return orderRepo.save(order);
    }

    public List<Order> getOrdersByUser(String userId) {
        return orderRepo.findByUserId(userId);
    }
}
