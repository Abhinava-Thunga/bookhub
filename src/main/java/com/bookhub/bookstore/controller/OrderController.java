package com.bookhub.bookstore.controller;

import com.bookhub.bookstore.dto.ApiResponse;
import com.bookhub.bookstore.entity.Order;
import com.bookhub.bookstore.service.OrderService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/orders")
@CrossOrigin
public class OrderController {

    private final OrderService service;

    public OrderController(OrderService service) {
        this.service = service;
    }

    @PostMapping
    public ApiResponse<Order> placeOrder() {
        Order order = service.placeOrder();
        return new ApiResponse<>(true, "Order placed successfully", order);
    }
}