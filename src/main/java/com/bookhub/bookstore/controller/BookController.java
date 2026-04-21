package com.bookhub.bookstore.controller;

import com.bookhub.bookstore.dto.ApiResponse;
import com.bookhub.bookstore.entity.Book;
import com.bookhub.bookstore.service.BookService;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/books")
@CrossOrigin
public class BookController {

    private final BookService service;

    public BookController(BookService service) {
        this.service = service;
    }

    // ✅ GET ALL BOOKS
    @GetMapping
    public ApiResponse<List<Book>> getBooks() {
        return new ApiResponse<>(true, "Books fetched successfully", service.getAllBooks());
    }

    // ✅ ADD BOOK
    @PostMapping
    public ApiResponse<Book> addBook(@RequestBody Book book) {
        return new ApiResponse<>(true, "Book added successfully", service.saveBook(book));
    }

    // ✅ UPDATE BOOK
    @PutMapping("/{id}")
    public ApiResponse<Book> updateBook(@PathVariable Long id, @RequestBody Book book) {
        return new ApiResponse<>(true, "Book updated successfully", service.updateBook(id, book));
    }

    // ✅ DELETE BOOK
    @DeleteMapping("/{id}")
    public ApiResponse<String> deleteBook(@PathVariable Long id) {
        service.deleteBook(id);
        return new ApiResponse<>(true, "Book deleted successfully", null);
    }
}