package com.bookhub.bookstore.repository;

import com.bookhub.bookstore.entity.CartItem;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CartRepository extends JpaRepository<CartItem, Long> {

}
