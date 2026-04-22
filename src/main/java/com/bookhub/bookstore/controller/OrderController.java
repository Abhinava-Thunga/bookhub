package com.bookhub.bookstore.controller;

import com.bookhub.bookstore.dto.ApiResponse;
import com.bookhub.bookstore.entity.Order;
import com.bookhub.bookstore.service.OrderService;

import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/orders")
@CrossOrigin
public class OrderController {

    private final OrderService service;

    public OrderController(OrderService service) {
        this.service = service;
    }

    // 🔥 PLACE ORDER
    @PostMapping("/{userId}")
    public ApiResponse<Order> placeOrder(@PathVariable String userId) {
        return new ApiResponse<>(true, "Order placed", service.placeOrder(userId));
    }

    // 🔥 GET HISTORY
    @GetMapping("/{userId}")
    public ApiResponse<List<Order>> getOrders(@PathVariable String userId) {
        return new ApiResponse<>(true, "Orders fetched", service.getOrdersByUser(userId));
    }
}