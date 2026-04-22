package com.bookhub.bookstore.controller;

import com.bookhub.bookstore.dto.ApiResponse;
import com.bookhub.bookstore.entity.Book;
import com.bookhub.bookstore.service.BookService;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.util.List;

@RestController
@RequestMapping("/books")
@CrossOrigin
public class BookController {

    private final BookService service;

    public BookController(BookService service) {
        this.service = service;
    }

    @GetMapping
    public ApiResponse<List<Book>> getBooks() {
        return new ApiResponse<>(true, "Books fetched", service.getAllBooks());
    }

    @PostMapping
    public ApiResponse<Book> addBook(@RequestBody Book book) {
        return new ApiResponse<>(true, "Book added", service.saveBook(book));
    }

    @DeleteMapping("/{id}")
    public ApiResponse<String> deleteBook(@PathVariable Long id) {
        service.deleteBook(id);
        return new ApiResponse<>(true, "Book deleted", null);
    }

    // 🔥 IMAGE UPLOAD API
    @PostMapping("/upload")
    public String uploadImage(@RequestParam("file") MultipartFile file) throws Exception {

        String folder = "uploads/";
        File dir = new File(folder);
        if (!dir.exists()) dir.mkdirs();

        String fileName = System.currentTimeMillis() + "_" + file.getOriginalFilename();
        String path = folder + fileName;

        file.transferTo(new File(path));

        return "http://localhost:8080/" + path;
    }
}