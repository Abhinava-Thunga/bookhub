package com.bookhub.bookstore.controller;

import com.bookhub.bookstore.dto.ApiResponse;
import com.bookhub.bookstore.entity.CartItem;
import com.bookhub.bookstore.service.CartService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/cart")
@CrossOrigin
public class CartController {

    private final CartService service;

    public CartController(CartService service) {
        this.service = service;
    }

    @PostMapping("/{id}/{qty}")
    public ApiResponse<CartItem> add(@PathVariable Long id, @PathVariable int qty) {
        return new ApiResponse<>(true, "Added", service.addToCart(id, qty));
    }

    @GetMapping
    public List<CartItem> get() {
        return service.getCart();
    }
}
