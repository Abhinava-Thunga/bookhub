package com.bookhub.bookstore.controller;

import com.bookhub.bookstore.dto.ApiResponse;
import com.bookhub.bookstore.entity.CartItem;
import com.bookhub.bookstore.service.CartService;
import org.springframework.http.ResponseEntity;
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

    @PostMapping("/{bookId}/{qty}")
    public CartItem addToCart(@PathVariable Long bookId, @PathVariable int qty) {
        return service.addToCart(bookId, qty);
    }

    @GetMapping
    public List<CartItem> getCart() {
        return service.getCart();


    }
}